import logging
import importlib
import multiprocessing
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, TimeoutError

from django.db import transaction
from django.db.models import Q, Count, F
from django.utils.timezone import now
from django_async_manager.models import Task, TASK_REGISTRY

logger = logging.getLogger("django_async_manager.worker")


class TimeoutException(Exception):
    """Raised when a task exceeds its allowed execution time."""

    pass


def _execute_task_in_process(func_path, args, kwargs):
    """
    Helper function executed IN THE CHILD PROCESS.
    Imports the module, finds the original function, and executes it.
    """
    try:
        module_name, func_name = func_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        target_func_or_decorator = getattr(module, func_name)

        if hasattr(target_func_or_decorator, "__wrapped__"):
            func_to_run = target_func_or_decorator.__wrapped__
        else:
            func_to_run = target_func_or_decorator
            logger.warning(
                f"Running function {func_path} which might not be decorated as expected."
            )

        if func_to_run is None or not callable(func_to_run):
            error_msg = f"Function {func_path} is not callable"
            logger.error(error_msg)
            raise TypeError(error_msg)

        return func_to_run(*args, **kwargs)
    except Exception as e:
        logger.debug(f"Exception in child process for {func_path}: {e}", exc_info=True)
        raise e


def execute_task(func_path: str, args, kwargs, timeout: int, use_threads=False):
    """
    Submits the task execution (defined by func_path) to either a ThreadPoolExecutor or ProcessPoolExecutor.
    Handles timeouts and exceptions from the child process.

    Args:
        func_path: The import path to the function to execute
        args: Positional arguments to pass to the function
        kwargs: Keyword arguments to pass to the function
        timeout: Maximum execution time in seconds
        use_threads: If True, use ThreadPoolExecutor, otherwise use ProcessPoolExecutor
    """
    try:
        module_name, func_name = func_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        if not hasattr(module, func_name):
            raise AttributeError(
                f"Function {func_name} not found in module {module_name}"
            )

        func = getattr(module, func_name)
        if func is None or not callable(func):
            raise TypeError(
                f"Function {func_name} in module {module_name} is not callable"
            )
    except (ValueError, ImportError, AttributeError, TypeError) as e:
        logger.error(
            f"Invalid function path or function not found: {func_path}. Error: {e}"
        )
        raise ValueError(
            f"Invalid function path or function not found: {func_path}. Error: {e}"
        )

    executor_class = ThreadPoolExecutor if use_threads else ProcessPoolExecutor

    with executor_class(max_workers=1) as executor:
        future = executor.submit(_execute_task_in_process, func_path, args, kwargs)
        try:
            start_time = time.time()
            result = future.result(timeout=timeout)
            execution_time = time.time() - start_time
            logger.debug(f"Task {func_path} completed in {execution_time:.2f} seconds")
            return result
        except TimeoutError:
            execution_time = time.time() - start_time
            logger.warning(
                f"Task {func_path} exceeded timeout of {timeout} seconds (ran for {execution_time:.2f} seconds)"
            )
            raise TimeoutException(
                f"Task {func_path} exceeded timeout of {timeout} seconds (ran for {execution_time:.2f} seconds)"
            )
        except Exception as e:
            logger.error(f"Task {func_path} failed with exception: {e}")
            raise e


class TaskWorker:
    """Worker for fetching and executing tasks"""

    def __init__(self, worker_id: str, queue: str = "default", use_threads=True):
        self.worker_id = worker_id
        self.queue = queue
        self.use_threads = use_threads

    def process_task(self) -> None:
        from django_async_manager.utils import with_database_lock_handling

        task = None

        @with_database_lock_handling(
            max_retries=3, logger_name="django_async_manager.worker"
        )
        def _acquire_task():
            nonlocal task
            with transaction.atomic():
                task_qs = (
                    Task.objects.filter(status="pending", queue=self.queue)
                    .annotate(
                        total_dependencies=Count("dependencies"),
                        completed_dependencies=Count(
                            "dependencies",
                            filter=Q(dependencies__status="completed"),
                        ),
                    )
                    .filter(
                        Q(total_dependencies=0)
                        | Q(total_dependencies=F("completed_dependencies"))
                    )
                    .filter(Q(scheduled_at__isnull=True) | Q(scheduled_at__lte=now()))
                    .order_by("-priority", "created_at")
                )

                task = task_qs.select_for_update(skip_locked=True).first()
                if not task:
                    return False

                if not task.worker_id:
                    task.worker_id = self.worker_id

                task.status = "in_progress"
                task.started_at = now()
                task.attempts = F("attempts") + 1
                task.save(
                    update_fields=["status", "started_at", "worker_id", "attempts"]
                )
                return True

        if not _acquire_task():
            return

        if not task:
            logger.debug("No task acquired after lock attempts.")
            return

        try:
            task.refresh_from_db()
        except Task.DoesNotExist:
            logger.warning(f"Task {task.id} disappeared before execution could start.")
            return

        try:
            if "." in task.name:
                func_path = task.name
            else:
                func_path = TASK_REGISTRY.get(task.name)

            if not func_path:
                error_msg = f"Task function '{task.name}' has not been registered."
                logger.error(error_msg)
                task.mark_as_failed(error_msg)
                return

            if "." not in func_path:
                error_msg = f"Invalid function path format: {func_path}"
                logger.error(error_msg)
                task.mark_as_failed(error_msg)
                return

            args = task.arguments.get("args", [])
            kwargs = task.arguments.get("kwargs", {})

            execute_task(
                func_path, args, kwargs, task.timeout, use_threads=self.use_threads
            )

            task.mark_as_completed()
            logger.info(f"Task {task.id} ({task.name}) completed successfully.")

        except TimeoutException as te:
            logger.warning(
                f"TimeoutException: Task {task.id} ({task.name}) exceeded time limit."
            )
            task.refresh_from_db()
            if task.autoretry and task.can_retry():
                logger.info(f"Scheduling retry for timed-out task {task.id}")
                task.schedule_retry(str(te))
            else:
                logger.error(
                    f"Marking timed-out task {task.id} as failed (no retries left or autoretry=False)."
                )
                task.mark_as_failed(str(te))
        except Exception as e:
            logger.exception(
                f"Exception during task execution {task.id} ({task.name}): {e}"
            )
            try:
                task.refresh_from_db()
                if task.autoretry and task.can_retry():
                    logger.info(f"Scheduling retry for failed task {task.id}")
                    task.schedule_retry(str(e))
                else:
                    logger.error(
                        f"Marking task {task.id} as failed (no retries left or autoretry=False). Error: {e}"
                    )
                    task.mark_as_failed(str(e))
            except Task.DoesNotExist:
                logger.error(
                    f"Task {task.id} disappeared after failing, cannot update status."
                )
            except Exception as update_err:
                logger.error(
                    f"Failed to update status for failed task {task.id}. Error: {update_err}",
                    exc_info=True,
                )

    def run(self) -> None:
        """Continuous processing of tasks."""
        while True:
            try:
                self.process_task()
            except Exception:
                logger.exception(
                    f"Worker {self.worker_id} encountered critical error in process_task loop. Restarting loop."
                )
            time.sleep(2)


class WorkerManager:
    """Manages multiple workers, supporting both threading and multiprocessing for the manager loop."""

    def __init__(self, num_workers=1, queue="default", use_threads=True):
        self.num_workers = num_workers
        self.queue = queue

        self.use_threads = use_threads
        self.workers = []

    def start_workers(self) -> None:
        """Start worker runners (either threads or processes)."""
        logger.info(
            f"Starting {self.num_workers} worker managers (each running TaskWorker loop) using {'threads' if self.use_threads else 'processes'} for queue '{self.queue}'."
        )
        for i in range(self.num_workers):
            worker_id = f"worker-{self.queue}-{i + 1}"

            worker_instance = TaskWorker(
                worker_id=worker_id, queue=self.queue, use_threads=self.use_threads
            )

            if self.use_threads:
                thread = threading.Thread(
                    target=worker_instance.run, name=worker_id, daemon=True
                )
                thread.start()
                self.workers.append(thread)
                logger.info(f"Started worker {worker_id} in a new thread.")
            else:
                process = multiprocessing.Process(
                    target=worker_instance.run, name=worker_id
                )
                process.start()
                self.workers.append(process)
                logger.info(f"Started worker {worker_id} in a new process.")

    def join_workers(self) -> None:
        """Wait for all worker runners (threads or processes) to complete."""
        logger.info(f"Waiting for {len(self.workers)} worker managers to finish...")
        for worker_runner in self.workers:
            worker_runner.join()
        logger.info("All worker managers have finished.")

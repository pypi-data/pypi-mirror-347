import threading


from typing import Callable
from cobweb.base import Queue
from abc import ABC, abstractmethod


class Scheduler(ABC, threading.Thread):

    __WORKING_ITEMS__ = {}
    __LAUNCHER_FUNC__ = ["_reset", "_scheduler", "_insert", "_refresh", "_delete"]

    def __init__(
            self,
            task,
            project,
            stop: threading.Event,
            pause: threading.Event,
            new: Queue,
            todo: Queue,
            done: Queue,
            upload: Queue,
            callback_register: Callable
    ):
        super().__init__()
        self.task = task
        self.project = project
        from cobweb import setting

        self.task_model = setting.TASK_MODEL
        self.seed_reset_seconds = setting.SEED_RESET_SECONDS
        self.scheduler_wait_seconds = setting.SCHEDULER_WAIT_SECONDS
        self.new_queue_wait_seconds = setting.NEW_QUEUE_WAIT_SECONDS
        self.done_queue_wait_seconds = setting.DONE_QUEUE_WAIT_SECONDS
        self.todo_queue_full_wait_seconds = setting.TODO_QUEUE_FULL_WAIT_SECONDS
        self.before_scheduler_wait_seconds = setting.BEFORE_SCHEDULER_WAIT_SECONDS

        self.todo_queue_size = setting.TODO_QUEUE_SIZE
        self.new_queue_max_size = setting.NEW_QUEUE_MAX_SIZE
        self.done_queue_max_size = setting.DONE_QUEUE_MAX_SIZE
        self.upload_queue_max_size = setting.UPLOAD_QUEUE_MAX_SIZE

        self.stop = stop
        self.pause = pause

        self.new = new
        self.todo = todo
        self.done = done
        self.upload = upload

        self.callback_register = callback_register
        self.lock = threading.Lock()

    def is_empty(self):
        return all(queue.empty() for queue in (self.new, self.todo, self.done, self.upload))

    def set_working_items(self, item_info: dict = None):
        if not item_info:
            return
        with self.lock:
            self.__WORKING_ITEMS__.update(item_info)

    def get_working_items(self) -> dict:
        with self.lock:
            return self.__WORKING_ITEMS__.copy()

    def remove_working_items(self, items: list[str] = None):
        if not items:
            return
        for _ in range(5):
            with self.lock:
                for item in items:
                    self.__WORKING_ITEMS__.pop(item, None)
                return True
            time.sleep(1)

    def get_working_items_count(self) -> int:
        with self.lock:
            return len(self.__WORKING_ITEMS__)

    def clear_working_items(self):
        with self.lock:
            self.__WORKING_ITEMS__.clear()

    @abstractmethod
    def reset(self):
        ...

    @abstractmethod
    def schedule(self):
        ...

    @abstractmethod
    def insert(self):
        ...

    @abstractmethod
    def refresh(self):
        ...

    @abstractmethod
    def delete(self):
        ...



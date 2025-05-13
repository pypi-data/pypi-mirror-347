import os
import time
import threading
from typing import Callable
from cobweb.db import RedisDB, ApiDB
from cobweb.utils import check_pause
from cobweb.base import Queue, Seed, logger
from cobweb.constant import LogTemplate
from .scheduler import Scheduler
use_api = bool(os.getenv("REDIS_API_HOST", 0))


class RedisScheduler(Scheduler):

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
        super().__init__(task, project, stop, pause, new, todo, done, upload, callback_register)
        self.todo_key = f"{{{project}:{task}}}:todo"
        self.done_key = f"{{{project}:{task}}}:done"
        self.fail_key = f"{{{project}:{task}}}:fail"
        self.heartbeat_key = f"heartbeat:{project}_{task}"
        self.speed_control_key = f"speed_control:{project}_{task}"
        self.reset_lock_key = f"lock:reset:{project}_{task}"
        self.db = ApiDB() if use_api else RedisDB()

    def reset(self):
        """
        检查过期种子，重新添加到redis缓存中
        """
        while not self.stop.is_set():
            if self.db.lock(self.reset_lock_key, t=60):

                _min = -int(time.time()) + self.seed_reset_seconds
                self.db.members(self.todo_key, 0, _min=_min, _max="(0")
                self.db.delete(self.reset_lock_key)

            time.sleep(60)

    @check_pause
    def schedule(self):
        """
        调度任务，获取redis队列种子，同时添加到doing字典中
        """
        if not self.db.zcount(self.todo_key, 0, "(1000"):
            time.sleep(self.scheduler_wait_seconds)
            return

        if self.todo.length >= self.todo_queue_size:
            time.sleep(self.todo_queue_full_wait_seconds)
            return

        members = self.db.members(
            self.todo_key, int(time.time()),
            count=self.todo_queue_size,
            _min=0, _max="(1000"
        )

        logger.debug(f"Retrieved {len(members)} seeds from Redis.")

        seeds, item_info = list(), dict()
        for member, priority in members:
            seed = Seed(member, priority=priority)
            item_info[seed.to_string] = seed.params.priority
            seeds.append(seed)

        self.set_working_items(item_info)
        self.todo.push(seeds)

    @check_pause
    def insert(self):
        """
        添加新种子到redis队列中
        """
        seeds, delete_seeds = dict(), set()
        for seed, new_seed in self.new.iter_items(limit=self.new_queue_max_size):
            seeds[new_seed.to_string] = new_seed.params.priority
            delete_seeds.add(seed)

        self.db.zadd(self.todo_key, seeds, nx=True)
        self.done.push(delete_seeds)

        if self.new.length < self.new_queue_max_size:
            time.sleep(self.scheduler_wait_seconds)

    @check_pause
    def refresh(self):
        """
        刷新doing种子过期时间，防止reset重新消费
        """
        if item_info := self.get_working_items():
            refresh_time = int(time.time())
            seed_info = {k: -refresh_time - v / 1000 for k, v in item_info.items()}
            self.db.zadd(self.todo_key, seed_info, xx=True)
            self.set_working_items(seed_info)
        time.sleep(20)

    @check_pause
    def delete(self):
        """
        删除队列种子，根据状态添加至成功或失败队列，移除doing字典种子索引
        """
        seeds = [seed for seed in self.done.iter_items(limit=self.done_queue_max_size)]
        items = [seed.to_string for seed in seeds]

        if self.remove_working_items(items):
            self.db.zrem(self.todo_key, *items)
        else:
            self.done.push(seeds)

        if self.done.length < self.done_queue_max_size:
            time.sleep(self.done_queue_wait_seconds)

    def run(self):
        start_time = int(time.time())

        for func in [self.reset, self.insert, self.delete, self.refresh, self.schedule]:
            self.callback_register(func, tag="scheduler")

        while not self.stop.is_set():
            working_count = self.get_working_items_count()
            memory_count = self.db.zcount(self.todo_key, "-inf", "(0")
            todo_count = self.db.zcount(self.todo_key, 0, "(1000")
            all_count = self.db.zcard(self.todo_key)

            if self.pause.is_set():
                execute_time = int(time.time()) - start_time
                if not self.task_model and execute_time > self.before_scheduler_wait_seconds:
                    logger.info("Done! ready to close thread...")
                    self.stop.set()
                elif todo_count:
                    logger.info(
                        f"Recovery {self.task} task run！Todo seeds count: {todo_count}, queue length: {all_count}")
                    self.pause.clear()
                else:
                    logger.info("Pause! waiting for resume...")

            elif self.is_empty():

                if all_count:
                    logger.info(f"Todo seeds count: {todo_count}, queue length: {all_count}")
                    self.pause.clear()
                else:
                    count = 0
                    for _ in range(3):
                        if not all_count:
                            count += 1
                            time.sleep(5)
                            logger.info("Checking count...")
                        else:
                            break
                    if count >= 3:
                        logger.info("Todo queue is empty! Pause set...")
                        self.clear_working_items()
                        self.pause.set()

            else:
                logger.info(LogTemplate.launcher_pro_polling.format(
                    task=self.task,
                    doing_len=working_count,
                    todo_len=self.todo.length,
                    done_len=self.done.length,
                    redis_seed_count=all_count,
                    redis_todo_len=todo_count,
                    redis_doing_len=memory_count,
                    upload_len=self.upload.length,
                ))

            time.sleep(30)

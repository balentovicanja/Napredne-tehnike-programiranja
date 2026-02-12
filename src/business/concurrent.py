from __future__ import annotations

"""
- konkurentno programiranje za background zadatke
- omogućuje izvršavanje autosave i izračun statistike
"""

import threading
import time
from typing import Callable, Any
from enum import Enum
from abc import ABC, abstractmethod


class TaskPriority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1


class BackgroundTask(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def should_run(self) -> bool:
        pass


class AutoSaveTask(BackgroundTask):
    
    def __init__(self, manager: Any, interval: int = 30):
        self.manager = manager
        self.interval = interval
        self._last_save = time.time()
    
    def execute(self) -> None:
        """Sprema sve transakcije."""
        transactions = self.manager.get_all_transactions()
        self.manager.storage.save(transactions)
        self._last_save = time.time()
        print(f"✓ Autosave: {len(transactions)} transakcija spremljeno")
    
    def should_run(self) -> bool:
        """Provjerava trebali li se pokrenuti."""
        return time.time() - self._last_save >= self.interval


class StatisticsTask(BackgroundTask):
    
    def __init__(self, manager: Any, interval: int = 5):
        self.manager = manager
        self.interval = interval
        self._last_calc = time.time()
        self.last_stats = None
    
    def execute(self) -> None:
        """Izračunava statistiku."""
        self.last_stats = self.manager.calculate_stats()
        self._last_calc = time.time()
        print(f"✓ Statistika ažurirana: Bilanca = {self.last_stats.balance}")
    
    def should_run(self) -> bool:
        """Provjerava trebali li se pokrenuti."""
        return time.time() - self._last_calc >= self.interval


class BackgroundWorker(threading.Thread):
    
    def __init__(
        self,
        interval: int = 1,
        daemon: bool = True,
        name: str = "BackgroundWorker"
    ):
        
        super().__init__(daemon=daemon, name=name)
        self.interval = interval
        self.tasks: list[BackgroundTask] = []
        self._running = False
        self._lock = threading.Lock()
    
    def add_task(self, task: BackgroundTask) -> None:
        with self._lock:
            self.tasks.append(task)
            print(f"Dodano: {task.__class__.__name__}")
    
    def remove_task(self, task_type: type) -> None:
        with self._lock:
            self.tasks = [t for t in self.tasks if not isinstance(t, task_type)]
    
    def run(self) -> None:
        self._running = True
        print(f"✓ {self.name} je pokrenut")
        
        while self._running:
            try:
                with self._lock:
                    for task in self.tasks:
                        if task.should_run():
                            task.execute()
                
                time.sleep(self.interval)
            
            except Exception as e:
                print(f"✗ Greška u {self.name}: {e}")
                time.sleep(self.interval)
    
    def stop(self) -> None:
        self._running = False
        print(f"✓ {self.name} je zaustavljen")
    
    def is_running(self) -> bool:
        return self._running


def create_task_executor(
    on_complete: Callable[..., None] | None = None,
    on_error: Callable[[Exception], None] | None = None
) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> threading.Thread:
            def task() -> None:
                try:
                    result = func(*args, **kwargs)
                    if on_complete:
                        on_complete(result)
                except Exception as e:
                    if on_error:
                        on_error(e)
                    else:
                        raise
            
            thread = threading.Thread(target=task, daemon=True)
            thread.start()
            return thread
        
        return wrapper
    
    return decorator

"""
Micro-Stacking Module
Manages parallel AI task execution with intelligent stacking
"""

import asyncio
import logging
from typing import List, Dict, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MicroTask:
    """Represents a single micro task in the stack"""
    id: str
    function: Callable
    args: tuple
    kwargs: dict
    priority: TaskPriority = TaskPriority.MEDIUM
    timeout: int = 300
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class MicroStacker:
    """
    Manages micro-stacked AI tasks for parallel execution.
    Optimizes task distribution and execution order.
    """
    
    def __init__(self, max_depth: int = 5, parallel_tasks: int = 3):
        """
        Initialize micro stacker.
        
        Args:
            max_depth: Maximum stack depth for task batching
            parallel_tasks: Number of tasks to run in parallel
        """
        self.max_depth = max_depth
        self.parallel_tasks = parallel_tasks
        self.task_queue: List[MicroTask] = []
        self.completed_tasks: Dict[str, Any] = {}
        self.executor = ThreadPoolExecutor(max_workers=parallel_tasks)
        
    def add_task(self, task: MicroTask):
        """Add a task to the micro stack"""
        self.task_queue.append(task)
        logger.info(f"Added task {task.id} with priority {task.priority.name}")
        
    def _sort_tasks(self) -> List[MicroTask]:
        """Sort tasks by priority and dependencies"""
        # First, sort by priority
        sorted_tasks = sorted(
            self.task_queue,
            key=lambda t: t.priority.value,
            reverse=True
        )
        
        # Then, resolve dependencies
        resolved = []
        unresolved = sorted_tasks.copy()
        
        while unresolved:
            made_progress = False
            for task in unresolved[:]:
                # Check if all dependencies are resolved
                deps_met = all(dep in [t.id for t in resolved] for dep in task.dependencies)
                
                if deps_met:
                    resolved.append(task)
                    unresolved.remove(task)
                    made_progress = True
            
            if not made_progress and unresolved:
                # Circular dependency or missing dependency - add anyway
                logger.warning(f"Dependency issue with tasks: {[t.id for t in unresolved]}")
                resolved.extend(unresolved)
                break
        
        return resolved
    
    def execute_stack(self) -> Dict[str, Any]:
        """
        Execute all tasks in the micro stack.
        
        Returns:
            Dictionary of task results
        """
        if not self.task_queue:
            logger.warning("No tasks in queue to execute")
            return {}
        
        sorted_tasks = self._sort_tasks()
        results = {}
        
        # Process tasks in batches
        for i in range(0, len(sorted_tasks), self.parallel_tasks):
            batch = sorted_tasks[i:i + self.parallel_tasks]
            batch_results = self._execute_batch(batch)
            results.update(batch_results)
            self.completed_tasks.update(batch_results)
        
        # Clear queue after execution
        self.task_queue.clear()
        
        logger.info(f"Executed {len(results)} tasks successfully")
        return results
    
    def _execute_batch(self, batch: List[MicroTask]) -> Dict[str, Any]:
        """Execute a batch of tasks in parallel"""
        futures = {}
        
        for task in batch:
            future = self.executor.submit(
                self._execute_task,
                task
            )
            futures[future] = task
        
        results = {}
        for future in as_completed(futures, timeout=max(t.timeout for t in batch)):
            task = futures[future]
            try:
                result = future.result()
                results[task.id] = result
                logger.info(f"Task {task.id} completed successfully")
            except Exception as e:
                logger.error(f"Task {task.id} failed: {str(e)}")
                results[task.id] = {"error": str(e)}
        
        return results
    
    def _execute_task(self, task: MicroTask) -> Any:
        """Execute a single task"""
        try:
            # Pass dependency results if needed
            if task.dependencies:
                dep_results = {
                    dep_id: self.completed_tasks.get(dep_id)
                    for dep_id in task.dependencies
                }
                task.kwargs['dependency_results'] = dep_results
            
            return task.function(*task.args, **task.kwargs)
        except Exception as e:
            logger.error(f"Error executing task {task.id}: {str(e)}")
            raise
    
    def create_ai_pipeline(self, steps: List[Dict[str, Any]]) -> List[MicroTask]:
        """
        Create a pipeline of AI tasks.
        
        Args:
            steps: List of step configurations
            
        Returns:
            List of created MicroTask objects
        """
        tasks = []
        prev_task_id = None
        
        for idx, step in enumerate(steps):
            task = MicroTask(
                id=f"task_{idx}_{step.get('name', 'unnamed')}",
                function=step['function'],
                args=step.get('args', ()),
                kwargs=step.get('kwargs', {}),
                priority=TaskPriority[step.get('priority', 'MEDIUM')],
                dependencies=[prev_task_id] if prev_task_id else []
            )
            tasks.append(task)
            self.add_task(task)
            prev_task_id = task.id
        
        return tasks
    
    def shutdown(self):
        """Shutdown the executor"""
        self.executor.shutdown(wait=True)

from datetime import date
from typing import List, Optional, Dict, Any
from auth import session
from entities import Task, TaskType, TaskStatus
from models import db


class TaskManager:
    @staticmethod
    def create_task(
        title: str,
        description: str,
        deadline: Optional[date] = None,
        assigned_user_id: Optional[str] = None,
    ) -> tuple[bool, str, Optional[Task]]:
        if not title:
            return False, "Title is required", None

        if not session.is_logged_in():
            return False, "User must be logged in to create tasks", None

        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            assigned_user_id=assigned_user_id,
            task_type=TaskType.TASK,
        )

        db.add_task(task)
        return True, "Task created successfully", task

    @staticmethod
    def create_subtask(
        parent_task_id: str,
        title: str,
        description: str,
        deadline: Optional[date] = None,
    ) -> tuple[bool, str, Optional[Task]]:
        if not title:
            return False, "Title is required", None

        if not session.is_logged_in():
            return False, "User must be logged in to create subtasks", None

        parent_task = db.get_task(parent_task_id)
        if not parent_task:
            return False, "Parent task not found", None

        subtask = Task(
            title=title,
            description=description,
            deadline=deadline,
            task_type=TaskType.SUBTASK,
            parent_id=parent_task_id,
        )

        db.add_task(subtask)
        return True, "Subtask created successfully", subtask

    @staticmethod
    def create_story(
        title: str, description: str, task_ids: List[str] = None
    ) -> tuple[bool, str, Optional[Task]]:
        if not title:
            return False, "Title is required", None

        if not session.is_logged_in():
            return False, "User must be logged in to create stories", None

        story = Task(title=title, description=description, task_type=TaskType.STORY)

        db.add_task(story)

        if task_ids:
            for task_id in task_ids:
                task = db.get_task(task_id)
                if task:
                    task.parent_id = story.id
                    task.update_timestamp()

        return True, "Story created successfully", story

    @staticmethod
    def get_user_tasks() -> List[Task]:
        if not session.is_logged_in():
            return []

        current_user = session.get_current_user()
        return db.get_tasks_by_user(current_user.id)

    @staticmethod
    def update_task(
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[date] = None,
        status: Optional[TaskStatus] = None,
        assigned_user_id: Optional[str] = None,
    ) -> tuple[bool, str, Optional[Task]]:
        if not session.is_logged_in():
            return False, "User must be logged in to update tasks", None

        task = db.get_task(task_id)
        if not task:
            return False, "Task not found", None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if deadline is not None:
            task.deadline = deadline
        if status is not None:
            task.status = status
        if assigned_user_id is not None:
            task.assigned_user_id = assigned_user_id

        task.update_timestamp()
        return True, "Task updated successfully", task

    @staticmethod
    def delete_task(task_id: str) -> tuple[bool, str]:
        if not session.is_logged_in():
            return False, "User must be logged in to delete tasks", None

        task = db.get_task(task_id)
        if not task:
            return False, "Task not found", None

        # Delete all subtasks and tasks within this task/story
        dependent_tasks = db.get_tasks_by_parent(task_id)
        for dependent_task in dependent_tasks:
            db.delete_task(dependent_task.id)

        db.delete_task(task_id)
        return True, "Task deleted successfully"

    @staticmethod
    def move_task(task_id: str, new_parent_id: Optional[str]) -> tuple[bool, str]:
        if not session.is_logged_in():
            return False, "User must be logged in to move tasks", None

        task = db.get_task(task_id)
        if not task:
            return False, "Task not found", None

        if new_parent_id:
            new_parent = db.get_task(new_parent_id)
            if not new_parent:
                return False, "New parent task not found", None

            # Check for circular dependencies
            current = new_parent
            while current:
                if current.id == task_id:
                    return (
                        False,
                        "Cannot move task into itself or its descendants",
                        None,
                    )
                current = db.get_task(current.parent_id) if current.parent_id else None

        task.parent_id = new_parent_id
        task.update_timestamp()
        return True, "Task moved successfully"

    @staticmethod
    def get_user_workload(user_id: str) -> Dict[str, Any]:
        user = db.get_user(user_id)
        if not user:
            return {}

        user_tasks = db.get_tasks_by_user(user_id)

        workload = {
            "user_id": user_id,
            "username": user.username,
            "total_tasks": len(user_tasks),
            "tasks_by_status": {},
            "upcoming_deadlines": [],
            "overdue_tasks": [],
        }

        today = date.today()

        for task in user_tasks:
            status = task.status.value
            workload["tasks_by_status"][status] = (
                workload["tasks_by_status"].get(status, 0) + 1
            )

            if task.deadline:
                if task.deadline < today and task.status != TaskStatus.COMPLETED:
                    workload["overdue_tasks"].append(
                        {
                            "task_id": task.id,
                            "title": task.title,
                            "deadline": task.deadline.isoformat(),
                            "days_overdue": (today - task.deadline).days,
                        }
                    )
                elif task.deadline >= today and task.status != TaskStatus.COMPLETED:
                    workload["upcoming_deadlines"].append(
                        {
                            "task_id": task.id,
                            "title": task.title,
                            "deadline": task.deadline.isoformat(),
                            "days_until": (task.deadline - today).days,
                        }
                    )

        # Sort deadlines
        workload["upcoming_deadlines"].sort(key=lambda x: x["days_until"])
        workload["overdue_tasks"].sort(key=lambda x: x["days_overdue"], reverse=True)

        return workload

    @staticmethod
    def get_task_hierarchy(task_id: str) -> Dict[str, Any]:
        task = db.get_task(task_id)
        if not task:
            return {}

        hierarchy = {
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "type": task.task_type.value,
                "status": task.status.value,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                "assigned_user_id": task.assigned_user_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
            },
            "subtasks": [],
            "parent": None,
        }

        # Get subtasks
        subtasks = db.get_tasks_by_parent(task_id)
        for subtask in subtasks:
            hierarchy["subtasks"].append(TaskManager.get_task_hierarchy(subtask.id))

        # Get parent
        if task.parent_id:
            parent = db.get_task(task.parent_id)
            if parent:
                hierarchy["parent"] = {
                    "id": parent.id,
                    "title": parent.title,
                    "type": parent.task_type.value,
                }

        return hierarchy

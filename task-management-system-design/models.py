from typing import List, Optional
from abc import ABC, abstractmethod
from entities import User, Task, Project


class DatabaseInterface(ABC):
    """Abstract interface for database backends"""

    @abstractmethod
    def add_user(self, user: User):
        """Add a user to the database"""
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    def add_task(self, task: Task):
        """Add a task to the database"""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        pass

    @abstractmethod
    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        """Get all tasks for a user"""
        pass

    @abstractmethod
    def get_tasks_by_parent(self, parent_id: str) -> List[Task]:
        """Get child tasks/subtasks"""
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        pass

    @abstractmethod
    def delete_task(self, task_id: str):
        """Delete a task"""
        pass

    @abstractmethod
    def add_project(self, project: Project):
        """Add a project"""
        pass

    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        pass


class Database(DatabaseInterface):
    """In-memory database implementation"""

    def __init__(self):
        self.users: dict[str, User] = {}
        self.tasks: dict[str, Task] = {}
        self.projects: dict[str, Project] = {}

    def add_user(self, user: User):
        self.users[user.id] = user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def add_task(self, task: Task):
        self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def get_tasks_by_user(self, user_id: str) -> List[Task]:
        return [
            task for task in self.tasks.values() if task.assigned_user_id == user_id
        ]

    def get_tasks_by_parent(self, parent_id: str) -> List[Task]:
        return [task for task in self.tasks.values() if task.parent_id == parent_id]

    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def delete_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]

    def add_project(self, project: Project):
        self.projects[project.id] = project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)


# Global database instance - can be easily swapped with other implementations
db: DatabaseInterface = Database()

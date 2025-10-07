from datetime import datetime, date
from enum import Enum
from typing import Optional
from dataclasses import dataclass, field
import uuid


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    TASK = "task"
    SUBTASK = "subtask"
    STORY = "story"


@dataclass
class User:
    """User entity with domain-specific behavior"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def set_password(self, password: str):
        """Set password with hashing"""
        self.password_hash = self._hash_password(password)

    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return self.password_hash == self._hash_password(password)

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        import hashlib

        return hashlib.sha256(password.encode()).hexdigest()

    def validate(self) -> tuple[bool, str]:
        """Validate user data"""
        if not self.username:
            return False, "Username is required"
        if not self.email:
            return False, "Email is required"
        if not self.password_hash:
            return False, "Password is required"
        if len(self.username) < 3:
            return False, "Username must be at least 3 characters"
        if "@" not in self.email:
            return False, "Invalid email format"
        return True, "Valid user"


@dataclass
class Task:
    """Task entity with domain-specific behavior"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    task_type: TaskType = TaskType.TASK
    status: TaskStatus = TaskStatus.PENDING
    deadline: Optional[date] = None
    assigned_user_id: Optional[str] = None
    parent_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_timestamp(self):
        """Update the timestamp"""
        self.updated_at = datetime.now()

    def can_have_children(self) -> bool:
        """Check if task can have subtasks"""
        return self.task_type in [TaskType.TASK, TaskType.STORY]

    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.deadline:
            return False
        return date.today() > self.deadline

    def validate(self) -> tuple[bool, str]:
        """Validate task data"""
        if not self.title:
            return False, "Title is required"
        if len(self.title) > 100:
            return False, "Title must be less than 100 characters"
        if self.deadline and self.deadline < date.today():
            return False, "Deadline cannot be in the past"
        return True, "Valid task"


@dataclass
class Project:
    """Project entity with domain-specific behavior"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = ""

    def validate(self) -> tuple[bool, str]:
        """Validate project data"""
        if not self.name:
            return False, "Project name is required"
        if len(self.name) > 50:
            return False, "Project name must be less than 50 characters"
        if not self.created_by:
            return False, "Project creator is required"
        return True, "Valid project"

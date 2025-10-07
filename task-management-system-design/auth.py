from typing import Optional
from models import User, db


class AuthService:
    @staticmethod
    def register_user(
        username: str, email: str, password: str
    ) -> tuple[bool, str, Optional[User]]:
        if not username or not email or not password:
            return False, "All fields are required", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters long", None

        if db.get_user_by_username(username):
            return False, "Username already exists", None

        if db.get_user_by_email(email):
            return False, "Email already exists", None

        user = User(username=username, email=email)
        user.set_password(password)
        db.add_user(user)

        return True, "User registered successfully", user

    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str, Optional[User]]:
        if not username or not password:
            return False, "Username and password are required", None

        user = db.get_user_by_username(username)
        if not user:
            return False, "Invalid username or password", None

        if not user.check_password(password):
            return False, "Invalid username or password", None

        return True, "Login successful", user

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        return db.get_user(user_id)


class SessionManager:

    def __init__(self):
        self.current_user: Optional[User] = None

    def login(self, user: User):
        self.current_user = user

    def logout(self):
        self.current_user = None

    def get_current_user(self) -> Optional[User]:
        return self.current_user

    def is_logged_in(self) -> bool:
        return self.current_user is not None


# Global session manager
session = SessionManager()

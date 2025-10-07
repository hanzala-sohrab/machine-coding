from datetime import datetime
from entities import TaskStatus
from auth import AuthService, session
from task_manager import TaskManager
from models import db


class TaskManagementCLI:
    def __init__(self):
        self.running = True

    def print_header(self):
        print("\n" + "=" * 50)
        print("      TASK MANAGEMENT SYSTEM")
        print("=" * 50)

    def print_menu(self):
        current_user = session.get_current_user()
        if current_user:
            print(f"\nLogged in as: {current_user.username}")
            print("\nMain Menu:")
            print("1. View my tasks")
            print("2. Create new task")
            print("3. Create subtask")
            print("4. Create story")
            print("5. Update task")
            print("6. Delete task")
            print("7. Move task")
            print("8. View task hierarchy")
            print("9. View user workload")
            print("10. Logout")
            print("0. Exit")
        else:
            print("\nMain Menu:")
            print("1. Register")
            print("2. Login")
            print("0. Exit")

    def register(self):
        print("\n--- Register New User ---")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        success, message, user = AuthService.register_user(username, email, password)
        if success:
            print(f"✓ {message}")
            session.login(user)
            print(f"Welcome, {user.username}!")
        else:
            print(f"✗ {message}")

    def login(self):
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        success, message, user = AuthService.login_user(username, password)
        if success:
            print(f"✓ {message}")
            session.login(user)
            print(f"Welcome back, {user.username}!")
        else:
            print(f"✗ {message}")

    def view_tasks(self):
        print("\n--- My Tasks ---")
        tasks = TaskManager.get_user_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for i, task in enumerate(tasks, 1):
            deadline_str = f" (Due: {task.deadline})" if task.deadline else ""
            print(
                f"{i}. {task.title}{deadline_str}"
            )
            print(f"   Status: {task.status.value}")
            if task.description:
                print(f"   Description: {task.description}")
            print()

    def create_task(self):
        print("\n--- Create New Task ---")
        title = input("Title: ").strip()
        if not title:
            print("✗ Title is required")
            return

        description = input("Description (optional): ").strip()

        deadline_str = input("Deadline (YYYY-MM-DD, optional): ").strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                print("✗ Invalid date format. Use YYYY-MM-DD")
                return

        current_user = session.get_current_user()
        success, message, task = TaskManager.create_task(
            title, description, deadline, current_user.id
        )

        if success:
            print(f"✓ {message}")
            print(f"Task ID: {task.id}")
        else:
            print(f"✗ {message}")

    def create_subtask(self):
        print("\n--- Create Subtask ---")
        parent_id = input("Parent Task ID: ").strip()

        parent_task = db.get_task(parent_id)
        if not parent_task:
            print("✗ Parent task not found")
            return

        title = input("Title: ").strip()
        if not title:
            print("✗ Title is required")
            return

        description = input("Description (optional): ").strip()

        deadline_str = input("Deadline (YYYY-MM-DD, optional): ").strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                print("✗ Invalid date format. Use YYYY-MM-DD")
                return

        success, message, subtask = TaskManager.create_subtask(
            parent_id, title, description, deadline
        )

        if success:
            print(f"✓ {message}")
            print(f"Subtask ID: {subtask.id}")
        else:
            print(f"✗ {message}")

    def create_story(self):
        print("\n--- Create Story ---")
        title = input("Title: ").strip()
        if not title:
            print("✗ Title is required")
            return

        description = input("Description (optional): ").strip()

        task_ids_str = input(
            "Task IDs to include (comma-separated, optional): "
        ).strip()
        task_ids = []
        if task_ids_str:
            task_ids = [tid.strip() for tid in task_ids_str.split(",")]

        success, message, story = TaskManager.create_story(title, description, task_ids)

        if success:
            print(f"✓ {message}")
            print(f"Story ID: {story.id}")
        else:
            print(f"✗ {message}")

    def update_task(self):
        print("\n--- Update Task ---")
        task_id = input("Task ID: ").strip()

        task = db.get_task(task_id)
        if not task:
            print("✗ Task not found")
            return

        print(f"Current task: {task.title}")
        print(f"Current status: {task.status.value}")
        print(f"Current description: {task.description}")
        print(f"Current deadline: {task.deadline}")

        title = input(f"New title (leave blank to keep '{task.title}'): ").strip()
        description = input(f"New description (leave blank to keep current): ").strip()

        status_str = input(
            f"New status (pending/in_progress/completed/cancelled, leave blank to keep '{task.status.value}'): "
        ).strip()
        status = None
        if status_str:
            try:
                status = TaskStatus(status_str)
            except ValueError:
                print("✗ Invalid status")
                return

        deadline_str = input(
            f"New deadline (YYYY-MM-DD, leave blank to keep {task.deadline}): "
        ).strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                print("✗ Invalid date format. Use YYYY-MM-DD")
                return

        success, message, updated_task = TaskManager.update_task(
            task_id,
            title if title else None,
            description if description else None,
            deadline,
            status,
        )

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")

    def delete_task(self):
        print("\n--- Delete Task ---")
        task_id = input("Task ID: ").strip()

        task = db.get_task(task_id)
        if not task:
            print("✗ Task not found")
            return

        confirm = (
            input(f"Are you sure you want to delete '{task.title}'? (y/N): ")
            .strip()
            .lower()
        )
        if confirm != "y":
            print("Deletion cancelled")
            return

        success, message = TaskManager.delete_task(task_id)

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")

    def move_task(self):
        print("\n--- Move Task ---")
        task_id = input("Task ID to move: ").strip()

        task = db.get_task(task_id)
        if not task:
            print("✗ Task not found")
            return

        new_parent_id = input(
            "New parent ID (leave blank to make it a root task): "
        ).strip()
        new_parent_id = new_parent_id if new_parent_id else None

        success, message = TaskManager.move_task(task_id, new_parent_id)

        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")

    def view_task_hierarchy(self):
        print("\n--- Task Hierarchy ---")
        task_id = input("Task ID: ").strip()

        hierarchy = TaskManager.get_task_hierarchy(task_id)
        if not hierarchy:
            print("✗ Task not found")
            return

        self._print_hierarchy(hierarchy, 0)

    def _print_hierarchy(self, hierarchy, level):
        indent = "  " * level
        task = hierarchy["task"]

        print(f"{indent}{task['title']} ({task['type']}) [{task['status']}]")
        if task["deadline"]:
            print(f"{indent}   Due: {task['deadline']}")

        for subtask in hierarchy["subtasks"]:
            self._print_hierarchy(subtask, level + 1)

    def view_user_workload(self):
        print("\n--- User Workload ---")
        user_id = input("User ID (leave blank for current user): ").strip()

        if not user_id:
            current_user = session.get_current_user()
            if not current_user:
                print("✗ No user logged in")
                return
            user_id = current_user.id

        workload = TaskManager.get_user_workload(user_id)
        if not workload:
            print("✗ User not found")
            return

        print(f"\nWorkload for {workload['username']}:")
        print(f"Total tasks: {workload['total_tasks']}")

        print("\nTasks by status:")
        for status, count in workload["tasks_by_status"].items():
            print(f"  {status}: {count}")

        if workload["upcoming_deadlines"]:
            print("\nUpcoming deadlines:")
            for task in workload["upcoming_deadlines"][:5]:  # Show next 5
                print(f"  {task['title']} - Due in {task['days_until']} days")

        if workload["overdue_tasks"]:
            print("\nOverdue tasks:")
            for task in workload["overdue_tasks"][:5]:  # Show first 5
                print(f"  {task['title']} - {task['days_overdue']} days overdue")

    def logout(self):
        session.logout()
        print("✓ Logged out successfully")

    def run(self):
        while self.running:
            self.print_header()
            self.print_menu()

            try:
                choice = input("\nEnter your choice: ").strip()

                if session.is_logged_in():
                    if choice == "1":
                        self.view_tasks()
                    elif choice == "2":
                        self.create_task()
                    elif choice == "3":
                        self.create_subtask()
                    elif choice == "4":
                        self.create_story()
                    elif choice == "5":
                        self.update_task()
                    elif choice == "6":
                        self.delete_task()
                    elif choice == "7":
                        self.move_task()
                    elif choice == "8":
                        self.view_task_hierarchy()
                    elif choice == "9":
                        self.view_user_workload()
                    elif choice == "10":
                        self.logout()
                    elif choice == "0":
                        self.running = False
                        print("Goodbye!")
                    else:
                        print("✗ Invalid choice")
                else:
                    if choice == "1":
                        self.register()
                    elif choice == "2":
                        self.login()
                    elif choice == "0":
                        self.running = False
                        print("Goodbye!")
                    else:
                        print("✗ Invalid choice")

                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"✗ An error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    # Import db here to avoid circular import
    from models import db

    cli = TaskManagementCLI()
    cli.run()

# Task Management System

A comprehensive task management system built in Python that allows users to manage tasks, subtasks, and stories within projects. The system includes user authentication, task hierarchy management, and workload tracking capabilities.

## Features

### User Management

- **User Registration**: Create new user accounts with username, email, and password
- **User Login**: Secure authentication with password hashing
- **Session Management**: Track logged-in users

### Task Management

- **Create Tasks**: Create new tasks with title, description, deadline, and assigned user
- **Create Subtasks**: Add subtasks to existing tasks
- **Create Stories**: Group multiple tasks into stories
- **Update Tasks**: Modify task details including title, description, deadline, and status
- **Delete Tasks**: Remove tasks and their dependent subtasks
- **Task Hierarchy**: View and manage task relationships

### Advanced Features

- **Move Tasks**: Reorganize task hierarchy by moving tasks between parents
- **User Workload**: Track user workload with statistics on task status, deadlines, and overdue tasks
- **Task Status**: Track task progress with pending, in_progress, completed, and cancelled statuses
- **Deadline Management**: Set and track task deadlines with overdue notifications

### Task Types

- **Tasks**: Standalone work items
- **Subtasks**: Tasks that belong to parent tasks
- **Stories**: Collections of related tasks

## System Architecture

### Core Components

1. **Models (`models.py`)**

   - `User`: User account management
   - `Task`: Task, subtask, and story entities
   - `Project`: Project container
   - `Database`: In-memory data storage

2. **Authentication (`auth.py`)**

   - `AuthService`: User registration and login
   - `SessionManager`: User session tracking

3. **Task Management (`task_manager.py`)**

   - `TaskManager`: Core task operations and business logic

4. **CLI Interface (`cli.py`)**
   - `TaskManagementCLI`: Command-line interface for user interaction

### Data Models

#### User

- `id`: Unique identifier
- `username`: User's username
- `email`: User's email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

#### Task

- `id`: Unique identifier
- `title`: Task title
- `description`: Task description
- `task_type`: Type (task, subtask, story)
- `status`: Current status (pending, in_progress, completed, cancelled)
- `deadline`: Optional deadline date
- `assigned_user_id`: ID of assigned user
- `parent_id`: ID of parent task (for hierarchy)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Installation and Usage

### Prerequisites

- Python 3.12 or higher
- No external dependencies required (uses only Python standard library)

### Running the Application

1. Clone or download the project files
2. Navigate to the project directory
3. Run the main application:

```bash
python main.py
```

### Using the CLI Interface

#### Starting the Application

When you run the application, you'll see the main menu:

```
==================================================
      TASK MANAGEMENT SYSTEM
==================================================

Main Menu:
1. Register
2. Login
0. Exit
```

#### User Registration

1. Select option 1 to register a new account
2. Enter your username, email, and password
3. Password must be at least 6 characters long

#### User Login

1. Select option 2 to login
2. Enter your username and password

#### Task Management (After Login)

Once logged in, the full task management menu will something like the following:

```
==================================================
      TASK MANAGEMENT SYSTEM
==================================================

Logged in as: your_username

Main Menu:
1. View my tasks
2. Create new task
3. Create subtask
4. Create story
5. Update task
6. Delete task
7. Move task
8. View task hierarchy
9. View user workload
10. Logout
0. Exit
```

### Key Functions

#### createTask(title, desc, deadline)

Creates a new task with the given details:

- `title`: Task title (required)
- `desc`: Task description (optional)
- `deadline`: Deadline date in YYYY-MM-DD format (optional)

#### createSubtask(parentTaskId, title, desc, deadline)

Adds a subtask to an existing task:

- `parentTaskId`: ID of the parent task
- `title`: Subtask title (required)
- `desc`: Subtask description (optional)
- `deadline`: Deadline date (optional)

#### createStory(title, desc, tasks)

Groups tasks together into a story:

- `title`: Story title (required)
- `desc`: Story description (optional)
- `tasks`: List of task IDs to include (optional)

#### moveTask(taskId, newParentId)

Moves a task to a different parent:

- `taskId`: ID of the task to move
- `newParentId`: ID of the new parent (can be None for root level)

#### getUserWorkload(userId)

Retrieves workload statistics for a user:

- `userId`: ID of the user
- Returns: Task counts by status, upcoming deadlines, overdue tasks

### Example Workflow

1. **Register and Login**

   ```
   1. Register
   Username: john_doe
   Email: john@example.com
   Password: mypassword123
   ```

2. **Create Tasks**

   ```
   2. Create new task
   Title: Design Homepage
   Description: Create wireframes and mockups for the homepage
   Deadline: 2024-12-31
   ```

3. **Create Subtasks**

   ```
   3. Create subtask
   Parent Task ID: [task_id_from_previous_step]
   Title: Create wireframes
   Description: Sketch initial layout ideas
   ```

4. **Create Story**

   ```
   4. Create story
   Title: Website Redesign
   Description: Complete redesign of company website
   Task IDs to include: [task_id_1,task_id_2]
   ```

5. **View Workload**
   ```
   9. View user workload
   User ID: [leave blank for current user]
   ```

## Error Handling

The system includes comprehensive error handling:

- Input validation for required fields
- Date format validation
- User authentication validation
- Task existence validation
- Circular dependency prevention for task movement

## Data Persistence

Currently, the system uses in-memory storage. Data is lost when the application restarts. For production use, we can consider integrating with a database system like SQLite, PostgreSQL, or MongoDB.

## Security Features

- Password hashing using SHA-256
- Session management
- Input validation
- Authentication required for all task operations

## Future Enhancements

Potential improvements for future versions:

- Database persistence (SQLite, PostgreSQL)
- User roles and permissions
- Task dependencies and relationships

## Testing

To test the system:

1. Run the application with `uv run main.py` or `python main.py`
2. Register a test user
3. Create sample tasks, subtasks, and stories
4. Test all CRUD operations
5. Verify task hierarchy movement
6. Check workload statistics

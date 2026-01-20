# Todo CLI App

A clean and lightweight command-line todo application that runs entirely in memory. It demonstrates core CRUD operations along with task completion, searching, filtering, and sorting. The project is designed to showcase solid CLI design, validation, and error handling in Python.

---

## Key Features

* Create tasks with title, description, priority, and tags
* View tasks with clear status indicators and priority icons
* Mark tasks as complete or incomplete
* Update task details, priority, and tags
* Delete tasks by ID
* Search tasks by keyword across title, description, and tags
* Filter tasks by status, priority, or tag
* Sort tasks by priority, status, or title
* Strong input validation and user-friendly error messages

---

## Requirements

* Python 3.13 or higher
* UV package manager

---

## Setup Instructions

1. Verify Python installation:

   ```bash
   python --version
   ```

2. Install UV (if not already installed):

   ```bash
   pip install uv
   ```

3. Navigate to the project root directory

4. Install dependencies:

   ```bash
   uv sync
   ```

5. Run the application:

   ```bash
   uv run python src/cli/main.py
   ```

---

## Available Commands

Once the application starts, you can use the following commands:

* `add <title> [description] [--priority <level>] [--tags <tag1,tag2,...>]`
  Add a new task with optional priority and tags

* `list [--sort <field>] [--filter <type:value>] [--search <keyword>]`
  Display all tasks with optional sorting, filtering, and searching

* `update <id> [--title <title>] [--description <description>] [--priority <level>] [--tags <tag1,tag2,...>]`
  Update an existing task by ID

* `delete <id>`
  Delete a task by ID

* `complete <id>`
  Mark a task as complete

* `incomplete <id>`
  Mark a task as incomplete

* `search <keyword>`
  Search tasks by keyword

* `help`
  Display available commands

* `quit` or `exit`
  Exit the application

---

## Command Options

* `--priority <level>`
  Accepted values: `High`, `Medium`, `Low`

* `--tags <tag1,tag2,...>`
  Comma-separated list of tags

* `--sort <field>`
  Sort by `priority`, `status`, or `title`

* `--filter <type:value>`
  Examples:

  * `status:completed`
  * `priority:High`
  * `tag:work`

* `--search <keyword>`
  Search in title, description, and tags

---

## Example Usage

```text
> add "Buy groceries" "Shopping for dinner" --priority High --tags shopping,urgent
[SUCCESS] Task added with ID: 1

> add "Complete project" "Finish the todo app implementation" --priority Medium --tags work,important
[SUCCESS] Task added with ID: 2

> list
[1] 🔴 ○ Buy groceries - Shopping for dinner | Priority: High | Tags: shopping, urgent | Status: ○ Incomplete
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> complete 1
[SUCCESS] Task 1 marked as complete

> list --filter tag:work
[2] 🟡 ○ Complete project - Finish the todo app implementation | Priority: Medium | Tags: important, work | Status: ○ Incomplete

> quit
Goodbye!
```

---

## Error Handling

The application provides clear error messages for common issues, including:

* Unknown or invalid commands
* Non-existent task IDs
* Missing required arguments
* Title length over 100 characters
* Description length over 500 characters
* Invalid priority values
* Empty or malformed tags
* Invalid filter or sort formats

---

## Notes

* All tasks are stored in memory and reset when the application exits
* Designed for learning, demos, and CLI best practices
* Easy to extend with persistence or additional features

---

Happy task tracking 🚀

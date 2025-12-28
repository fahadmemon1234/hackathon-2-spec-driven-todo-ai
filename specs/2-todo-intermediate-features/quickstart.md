# Quickstart Guide: Todo App with Intermediate Features

## Setting up the enhanced todo app
1. Clone the repository
2. Install dependencies with UV: `uv sync`
3. Run the application: `uv run python src/cli/main.py`

## Using new features

### 1. Adding Tasks with Priority and Tags
Add a new task with priority and tags:
```
add "Complete project proposal" --priority High --tags work,important
```

Add a task with just priority:
```
add "Buy groceries" --priority Medium
```

Add a task with just tags:
```
add "Call plumber" --tags home,maintenance
```

### 2. Listing Tasks

List all tasks:
```
list
```

List tasks sorted by priority (High to Low):
```
list --sort priority
```

List tasks sorted alphabetically by title:
```
list --sort title
```

List tasks sorted by completion status (incomplete first):
```
list --sort status
```

### 3. Filtering Tasks

Show only completed tasks:
```
list --filter status:completed
```

Show only incomplete tasks:
```
list --filter status:incomplete
```

Show only high priority tasks:
```
list --filter priority:High
```

Show tasks with a specific tag:
```
list --filter tag:work
```

### 4. Searching Tasks

Search for tasks containing a keyword in title, description, or tags:
```
search "project"
```

Or use the list command with search:
```
list --search "grocery"
```

### 5. Updating Tasks

Update a task's priority and tags:
```
update 1 --priority Low --tags personal,optional
```

Update only the priority:
```
update 1 --priority Medium
```

Update only the tags:
```
update 1 --tags work,important,urgent
```

### 6. Marking Tasks Complete/Incomplete

Mark a task as complete:
```
complete 1
```

Mark a task as incomplete:
```
incomplete 1
```

### 7. Deleting Tasks

Delete a task:
```
delete 1
```

### 8. Getting Help

View available commands:
```
help
```

View help for a specific command:
```
help <command>
```

## Example Workflow

1. Add some tasks:
   ```
   add "Finish report" --priority High --tags work,important
   add "Buy milk" --priority Medium --tags shopping
   add "Call mom" --priority Low --tags personal,family
   ```

2. View all tasks:
   ```
   list
   ```

3. Sort tasks by priority:
   ```
   list --sort priority
   ```

4. Filter work-related tasks:
   ```
   list --filter tag:work
   ```

5. Search for specific tasks:
   ```
   search "report"
   ```

6. Update a task:
   ```
   update 1 --priority Medium
   ```

7. Mark a task complete:
   ```
   complete 2
   ```
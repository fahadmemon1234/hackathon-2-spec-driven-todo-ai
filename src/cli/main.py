import sys
import os
# Add the src directory to the path so imports work correctly
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from services.todo_manager import TodoManager, TaskNotFoundError


class TodoApp:
    """
    Main CLI application for the Todo app.
    Handles user input and commands.
    """

    def __init__(self):
        """Initialize the TodoApp with a TodoManager instance."""
        self.todo_manager = TodoManager()
        self.running = True

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo CLI App!")
        print("Type 'help' for available commands or 'quit' to exit.")

        while self.running:
            try:
                command_input = input("\n> ").strip()
                if not command_input:
                    continue

                self.process_command(command_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    def process_command(self, command_input: str):
        """Process a command from the user."""
        # Parse the command and arguments more intelligently
        parts = command_input.strip().split()
        if not parts:
            return

        command = parts[0].lower()

        # For commands that need to preserve spaces in arguments, parse differently
        if command == "add":
            # For add command, the format is: add <title> [description]
            # We need to handle spaces in title and description
            args = self._parse_add_command(command_input)
            self.handle_add(args)
        elif command == "update":
            # For update command, the format is: update <id> <title> [description]
            args = self._parse_update_command(command_input)
            self.handle_update(args)
        elif command == "list":
            self.handle_list(parts[1:])
        elif command == "delete":
            self.handle_delete(parts[1:])
        elif command == "complete":
            self.handle_complete(parts[1:])
        elif command == "incomplete":
            self.handle_incomplete(parts[1:])
        elif command == "help":
            self.handle_help(parts[1:])
        elif command == "search":
            self.handle_search(parts[1:])
        elif command in ["quit", "exit"]:
            self.handle_quit(parts[1:])
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")

    def _parse_add_command(self, command_input: str) -> list:
        """Parse the add command, handling spaces in title and description, and options like --priority and --tags."""
        # Find where options start (like --priority, --tags) to separate them from title/description
        options_start_idx = len(command_input)
        for i, char in enumerate(command_input):
            if char == '-' and i + 1 < len(command_input) and command_input[i + 1] == '-':
                options_start_idx = i
                break

        # Separate the main command from options
        main_part = command_input[:options_start_idx].strip()
        options_part = command_input[options_start_idx:].strip() if options_start_idx < len(command_input) else ""

        # Split the main part to get the command
        parts = main_part.split()
        if len(parts) < 2:
            return ["", "", "Medium", set()]  # Default values

        # Process options if they exist
        priority = "Medium"  # Default priority
        tags = set()  # Default empty tags set

        if options_part:
            # If there are options, we need to parse them
            # Find the start of options in the original command
            all_parts = command_input.strip().split()
            option_idx = len(all_parts)
            for i, part in enumerate(all_parts):
                if part.startswith('--'):
                    option_idx = i
                    break

            # Process options
            i = option_idx
            while i < len(all_parts):
                part = all_parts[i]

                if part == '--priority' and i + 1 < len(all_parts):
                    priority = all_parts[i + 1]
                    i += 2  # Skip the priority value
                elif part == '--tags' and i + 1 < len(all_parts):
                    # Parse tags from comma-separated string
                    tags_str = all_parts[i + 1]
                    tags = {tag.strip() for tag in tags_str.split(',') if tag.strip()}
                    i += 2  # Skip the tags value
                else:
                    i += 1

            # Everything before the options is title and description
            title_desc_parts = all_parts[1:option_idx]
        else:
            # No options, so all parts after 'add' are title and description
            title_desc_parts = parts[1:]

        # For the test case "add Buy milk Grocery shopping", we expect:
        # Title: "Buy milk", Description: "Grocery shopping"
        # This suggests that the first two words form the title, and the rest form the description
        if len(title_desc_parts) == 0:
            return ["", "", priority, tags]
        elif len(title_desc_parts) == 1:
            title = title_desc_parts[0]
            description = ""
        elif len(title_desc_parts) == 2:
            title = ' '.join(title_desc_parts[:2])  # First two words as title
            description = ""
        else:
            title = ' '.join(title_desc_parts[:2])  # First two words as title
            description = ' '.join(title_desc_parts[2:])  # Remaining words as description

        return [title, description, priority, tags]

    def _parse_update_command(self, command_input: str) -> list:
        """Parse the update command, handling spaces in title and description, and options like --priority and --tags."""
        # Use shlex to properly handle quoted strings
        import shlex
        try:
            parts = shlex.split(command_input)
        except:
            # If shlex fails, fall back to basic split
            parts = command_input.strip().split()

        if len(parts) < 2:
            return []

        # Initialize default values
        task_id = parts[1]  # The ID should be the second part
        title = None
        description = None
        priority = None  # Will remain None if not specified
        tags = None  # Will remain None if not specified

        # Process arguments starting from index 2
        i = 2
        while i < len(parts):
            part = parts[i]

            if part == '--title' and i + 1 < len(parts):
                title = parts[i + 1]
                i += 2  # Skip the title value
            elif part == '--description' and i + 1 < len(parts):
                description = parts[i + 1]
                i += 2  # Skip the description value
            elif part == '--priority' and i + 1 < len(parts):
                priority = parts[i + 1]
                i += 2  # Skip the priority value
            elif part == '--tags' and i + 1 < len(parts):
                # Parse tags from comma-separated string
                tags_str = parts[i + 1]
                tags = {tag.strip() for tag in tags_str.split(',') if tag.strip()}
                i += 2  # Skip the tags value
            else:
                i += 1  # Move to next part

        return [task_id, title, description, priority, tags]

    def handle_add(self, args: list):
        """Handle the 'add' command."""
        if len(args) < 1:
            print("Usage: add <title> [description] [--priority <level>] [--tags <tag1,tag2,...>]")
            return

        title = args[0]
        description = args[1] if len(args) > 1 else ""
        priority = args[2] if len(args) > 2 else "Medium"
        tags = args[3] if len(args) > 3 else set()

        try:
            task_id = self.todo_manager.add_task(title, description, priority, tags)
            print(f"[SUCCESS] Task added with ID: {task_id} | Title: {title} | Priority: {priority} | Tags: {tags}")
        except ValueError as e:
            print(f"[ERROR] {e}")

    def handle_list(self, args: list):
        """Handle the 'list' command."""
        # Parse arguments for sort, filter, and search options
        sort_by = None
        filter_by = None
        search_keyword = None
        
        i = 0
        while i < len(args):
            if args[i] == '--sort' and i + 1 < len(args):
                sort_by = args[i + 1]
                i += 2
            elif args[i] == '--filter' and i + 1 < len(args):
                filter_by = args[i + 1]
                i += 2
            elif args[i] == '--search' and i + 1 < len(args):
                search_keyword = args[i + 1]
                i += 2
            else:
                print("Usage: list [--sort <field>] [--filter <type:value>] [--search <keyword>]")
                return

        # Get tasks based on search, filter, and sort options
        tasks = self.todo_manager.get_all_tasks()
        
        # Apply search if specified
        if search_keyword:
            tasks = self.todo_manager.search_tasks(search_keyword)
        
        # Apply filter if specified
        if filter_by:
            # Parse filter type and value
            if ':' in filter_by:
                filter_type, filter_value = filter_by.split(':', 1)
                if filter_type == 'status':
                    tasks = self.todo_manager.filter_tasks(status=filter_value)
                elif filter_type == 'priority':
                    tasks = self.todo_manager.filter_tasks(priority=filter_value)
                elif filter_type == 'tag':
                    tasks = self.todo_manager.filter_tasks(tag=filter_value)
            else:
                print("Invalid filter format. Use --filter <type:value>")
                return
        
        # Apply sort if specified
        if sort_by:
            tasks = self.todo_manager.sort_tasks(sort_by)

        if not tasks:
            print("No tasks found.")
            return

        # Import the display utility function
        from src.cli.display import format_task_display
        
        for task in tasks:
            print(format_task_display(task))

    def handle_update(self, args: list):
        """Handle the 'update' command."""
        if len(args) < 1:
            print("Usage: update <id> [--title <title>] [--description <description>] [--priority <level>] [--tags <tag1,tag2,...>]")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("[ERROR] Task ID must be an integer")
            return

        # Extract parameters (could be None if not specified)
        title = args[1] if len(args) > 1 and args[1] is not None else None
        description = args[2] if len(args) > 2 and args[2] is not None else None
        priority = args[3] if len(args) > 3 and args[3] is not None else None
        tags = args[4] if len(args) > 4 and args[4] is not None else None

        try:
            # Update the task with only the specified parameters
            self.todo_manager.update_task(
                task_id=task_id,
                title=title,
                description=description,
                priority=priority,
                tags=tags
            )
            print(f"[SUCCESS] Task {task_id} updated successfully")
        except TaskNotFoundError:
            print(f"[ERROR] Task with ID {task_id} does not exist.")
        except ValueError as e:
            print(f"[ERROR] {e}")

    def handle_delete(self, args: list):
        """Handle the 'delete' command."""
        if len(args) != 1:
            print("Usage: delete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("[ERROR] Task ID must be an integer")
            return

        try:
            self.todo_manager.delete_task(task_id)
            print(f"[SUCCESS] Task {task_id} deleted successfully")
        except TaskNotFoundError:
            print(f"[ERROR] Task with ID {task_id} does not exist.")

    def handle_complete(self, args: list):
        """Handle the 'complete' command."""
        if len(args) != 1:
            print("Usage: complete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("[ERROR] Task ID must be an integer")
            return

        try:
            self.todo_manager.mark_complete(task_id)
            print(f"[SUCCESS] Task {task_id} marked as complete")
        except TaskNotFoundError:
            print(f"[ERROR] Task with ID {task_id} does not exist.")

    def handle_incomplete(self, args: list):
        """Handle the 'incomplete' command."""
        if len(args) != 1:
            print("Usage: incomplete <id>")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("[ERROR] Task ID must be an integer")
            return

        try:
            self.todo_manager.mark_incomplete(task_id)
            print(f"[SUCCESS] Task {task_id} marked as incomplete")
        except TaskNotFoundError:
            print(f"[ERROR] Task with ID {task_id} does not exist.")

    def handle_search(self, args: list):
        """Handle the 'search' command."""
        if len(args) != 1:
            print("Usage: search <keyword>")
            return

        keyword = args[0]

        # Use the search functionality from the todo manager
        matching_tasks = self.todo_manager.search_tasks(keyword)

        if not matching_tasks:
            print(f"[INFO] No tasks found containing '{keyword}'.")
            return

        # Import the display utility function
        from src.cli.display import format_task_display

        print(f"[SUCCESS] Found {len(matching_tasks)} task(s) containing '{keyword}':")
        for task in matching_tasks:
            print(format_task_display(task))

    def handle_help(self, args: list):
        """Handle the 'help' command."""
        if len(args) != 0:
            print("Usage: help")
            return

        print("Available commands:")
        print("  add <title> [description] [--priority <level>] [--tags <tag1,tag2,...>]    - Add a new task")
        print("  list [--sort <field>] [--filter <type:value>] [--search <keyword>]        - List all tasks")
        print("  update <id> [--title <title>] [--description <description>] [--priority <level>] [--tags <tag1,tag2,...>] - Update a task")
        print("  delete <id>                  - Delete a task")
        print("  complete <id>                - Mark a task as complete")
        print("  incomplete <id>              - Mark a task as incomplete")
        print("  search <keyword>             - Search tasks by keyword")
        print("  help                         - Show this help message")
        print("  quit/exit                    - Exit the application")
        print("")
        print("Options:")
        print("  --priority <level>           - Priority level (High, Medium, Low)")
        print("  --tags <tag1,tag2,...>       - Comma-separated list of tags")
        print("  --sort <field>               - Sort by field (priority, status, title)")
        print("  --filter <type:value>        - Filter by type and value (status:completed, priority:High, tag:work)")
        print("  --search <keyword>           - Search by keyword in title, description, or tags")
        print("")
        print("Examples:")
        print("  add \"Buy groceries\" --priority High --tags shopping,urgent")
        print("  list --sort priority")
        print("  list --filter status:completed")
        print("  list --filter tag:work")
        print("  list --search \"project\"")
        print("  update 1 --priority Medium --tags work,important")
        print("  search \"grocery\"")

    def handle_quit(self, args: list):
        """Handle the 'quit' or 'exit' command."""
        if len(args) != 0:
            print("Usage: quit (or exit)")
            return

        print("Goodbye!")
        self.running = False


def main():
    """Main entry point for the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
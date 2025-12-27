import sys
from src.services.todo_manager import TodoManager, TaskNotFoundError


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
        elif command in ["quit", "exit"]:
            self.handle_quit(parts[1:])
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")

    def _parse_add_command(self, command_input: str) -> list:
        """Parse the add command, handling spaces in title and description."""
        # Remove the command part
        parts = command_input.strip().split(' ', 1)
        if len(parts) < 2:
            return []

        args_str = parts[1]
        # For the example in quickstart.md: "add Buy groceries Shopping for dinner"
        # Title should be "Buy groceries", description should be "Shopping for dinner"
        # So we'll split by taking the first two words as title and the rest as description
        words = args_str.split()
        if len(words) == 0:
            return []
        elif len(words) == 1:
            # If only one word, treat it as title with empty description
            return [words[0], ""]
        elif len(words) == 2:
            # If two words, first is title, second is description
            return words
        else:
            # If more than two words, first two are title, rest is description
            title = " ".join(words[:2])
            description = " ".join(words[2:])
            return [title, description]

    def _parse_update_command(self, command_input: str) -> list:
        """Parse the update command, handling spaces in title and description."""
        # Remove the command part
        parts = command_input.strip().split(' ', 2)  # Split into at most 3 parts: command, id, rest
        if len(parts) < 3:
            return parts[1:] if len(parts) > 1 else []

        cmd, task_id, rest = parts
        # For update command, similar to add: first two words as title, rest as description
        words = rest.split()
        if len(words) == 0:
            return [task_id]
        elif len(words) == 1:
            # If only one word, treat it as title with empty description
            return [task_id, words[0], ""]
        elif len(words) == 2:
            # If two words, first is title, second is description
            return [task_id] + words
        else:
            # If more than two words, first two are title, rest is description
            title = " ".join(words[:2])
            description = " ".join(words[2:])
            return [task_id, title, description]
    
    def handle_add(self, args: list):
        """Handle the 'add' command."""
        if len(args) < 1:
            print("Usage: add <title> [description]")
            return

        title = args[0]
        description = " ".join(args[1:]) if len(args) > 1 else ""

        try:
            task_id = self.todo_manager.add_task(title, description)
            print(f"Task added with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def handle_list(self, args: list):
        """Handle the 'list' command."""
        if len(args) != 0:
            print("Usage: list")
            return
        
        tasks = self.todo_manager.get_all_tasks()
        
        if not tasks:
            print("No tasks found.")
            return
        
        for task in tasks:
            status = "Complete" if task.completed else "Incomplete"
            print(f"ID: {task.id} | Title: {task.title} | Description: {task.description} | Status: {status}")
    
    def handle_update(self, args: list):
        """Handle the 'update' command."""
        if len(args) < 2:
            print("Usage: update <id> <title> [description]")
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be an integer")
            return

        title = args[1]
        description = " ".join(args[2:]) if len(args) > 2 else ""

        try:
            self.todo_manager.update_task(task_id, title, description)
            print(f"Task {task_id} updated successfully")
        except TaskNotFoundError:
            print(f"Task with ID {task_id} does not exist.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def handle_delete(self, args: list):
        """Handle the 'delete' command."""
        if len(args) != 1:
            print("Usage: delete <id>")
            return
        
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be an integer")
            return
        
        try:
            self.todo_manager.delete_task(task_id)
            print(f"Task {task_id} deleted successfully")
        except TaskNotFoundError:
            print(f"Task with ID {task_id} does not exist.")
    
    def handle_complete(self, args: list):
        """Handle the 'complete' command."""
        if len(args) != 1:
            print("Usage: complete <id>")
            return
        
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be an integer")
            return
        
        try:
            self.todo_manager.mark_complete(task_id)
            print(f"Task {task_id} marked as complete")
        except TaskNotFoundError:
            print(f"Task with ID {task_id} does not exist.")
    
    def handle_incomplete(self, args: list):
        """Handle the 'incomplete' command."""
        if len(args) != 1:
            print("Usage: incomplete <id>")
            return
        
        try:
            task_id = int(args[0])
        except ValueError:
            print("Error: ID must be an integer")
            return
        
        try:
            self.todo_manager.mark_incomplete(task_id)
            print(f"Task {task_id} marked as incomplete")
        except TaskNotFoundError:
            print(f"Task with ID {task_id} does not exist.")
    
    def handle_help(self, args: list):
        """Handle the 'help' command."""
        if len(args) != 0:
            print("Usage: help")
            return
        
        print("Available commands:")
        print("  add <title> <description>    - Add a new task")
        print("  list                         - List all tasks")
        print("  update <id> <title> <description> - Update a task")
        print("  delete <id>                  - Delete a task")
        print("  complete <id>                - Mark a task as complete")
        print("  incomplete <id>              - Mark a task as incomplete")
        print("  help                         - Show this help message")
        print("  quit/exit                    - Exit the application")
    
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
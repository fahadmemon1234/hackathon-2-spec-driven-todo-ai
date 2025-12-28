"""
Argument parser for the Todo CLI app.
Handles parsing of command-line arguments with support for new features like priority and tags.
"""

import argparse
from typing import List, Optional


class TodoArgumentParser:
    """
    Argument parser for the Todo CLI app.
    """

    def __init__(self):
        """Initialize the argument parser with subcommands for different operations."""
        self.parser = argparse.ArgumentParser(
            description="Todo CLI App - Manage your tasks efficiently"
        )
        self.subparsers = self.parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        self.add_parser = self.subparsers.add_parser('add', help='Add a new task')
        self.add_parser.add_argument('title', help='Title of the task')
        self.add_parser.add_argument('description', nargs='?', default='', help='Description of the task')
        self.add_parser.add_argument('--priority', choices=['High', 'Medium', 'Low'],
                                     default='Medium', help='Priority level of the task')
        self.add_parser.add_argument('--tags', type=self.parse_tags,
                                     help='Comma-separated list of tags (e.g., "work,important")')

        # Update command
        self.update_parser = self.subparsers.add_parser('update', help='Update an existing task')
        self.update_parser.add_argument('id', type=int, help='ID of the task to update')
        self.update_parser.add_argument('--title', help='New title for the task')
        self.update_parser.add_argument('--description', help='New description for the task')
        self.update_parser.add_argument('--priority', choices=['High', 'Medium', 'Low'],
                                        help='New priority level for the task')
        self.update_parser.add_argument('--tags', type=self.parse_tags,
                                        help='New comma-separated list of tags')

        # List command
        self.list_parser = self.subparsers.add_parser('list', help='List all tasks')
        self.list_parser.add_argument('--sort', choices=['priority', 'status', 'title'],
                                      help='Sort tasks by specified field')
        self.list_parser.add_argument('--filter', action='append',
                                      help='Filter tasks (format: type:value, e.g., "status:completed", "priority:High", "tag:work")')
        self.list_parser.add_argument('--search', help='Search tasks by keyword')

        # Delete command
        self.delete_parser = self.subparsers.add_parser('delete', help='Delete a task')
        self.delete_parser.add_argument('id', type=int, help='ID of the task to delete')

        # Complete command
        self.complete_parser = self.subparsers.add_parser('complete', help='Mark a task as complete')
        self.complete_parser.add_argument('id', type=int, help='ID of the task to mark as complete')

        # Incomplete command
        self.incomplete_parser = self.subparsers.add_parser('incomplete', help='Mark a task as incomplete')
        self.incomplete_parser.add_argument('id', type=int, help='ID of the task to mark as incomplete')

        # Search command
        self.search_parser = self.subparsers.add_parser('search', help='Search tasks by keyword')
        self.search_parser.add_argument('keyword', help='Keyword to search for')

    def parse_tags(self, tags_str: str) -> set:
        """
        Parse a comma-separated string of tags into a set.

        Args:
            tags_str: Comma-separated string of tags

        Returns:
            A set of tags
        """
        if not tags_str:
            return set()

        # Split by comma and strip whitespace, then filter out empty strings
        tags = {tag.strip() for tag in tags_str.split(',') if tag.strip()}
        return tags

    def parse_args(self, args: List[str]) -> argparse.Namespace:
        """
        Parse the command-line arguments.

        Args:
            args: List of command-line arguments

        Returns:
            Parsed arguments as a Namespace object
        """
        return self.parser.parse_args(args)

    def print_help(self):
        """Print the help message."""
        self.parser.print_help()

    def validate_args(self, args):
        """
        Perform additional validation on parsed arguments.

        Args:
            args: Parsed arguments namespace

        Returns:
            True if arguments are valid, raises ValueError otherwise
        """
        if args.command == 'add':
            # Validate title length
            if not (1 <= len(args.title) <= 100):
                raise ValueError(f"Title must be between 1 and 100 characters, got {len(args.title)}")

            # Validate description length
            if args.description and not (1 <= len(args.description) <= 500):
                raise ValueError(f"Description must be between 1 and 500 characters, got {len(args.description)}")

            # Validate tags
            if args.tags:
                for tag in args.tags:
                    if not tag.strip():
                        raise ValueError(f"Tags must be non-empty strings")

        elif args.command == 'update':
            # Validate task ID
            if args.id <= 0:
                raise ValueError(f"Task ID must be a positive integer, got {args.id}")

            # Validate title if provided
            if args.title and not (1 <= len(args.title) <= 100):
                raise ValueError(f"Title must be between 1 and 100 characters, got {len(args.title) if args.title else 0}")

            # Validate description if provided
            if args.description and not (1 <= len(args.description) <= 500):
                raise ValueError(f"Description must be between 1 and 500 characters, got {len(args.description) if args.description else 0}")

            # Validate tags if provided
            if args.tags:
                for tag in args.tags:
                    if not tag.strip():
                        raise ValueError(f"Tags must be non-empty strings")

        elif args.command == 'list':
            # Validate sort option if provided
            if args.sort and args.sort not in ['priority', 'status', 'title']:
                raise ValueError(f"Sort option must be one of 'priority', 'status', 'title', got '{args.sort}'")

            # Validate filter format if provided
            if args.filter:
                for f in args.filter:
                    if ':' not in f:
                        raise ValueError(f"Filter must be in format 'type:value', got '{f}'")
                    filter_type, filter_value = f.split(':', 1)
                    if filter_type not in ['status', 'priority', 'tag']:
                        raise ValueError(f"Filter type must be one of 'status', 'priority', 'tag', got '{filter_type}'")

        elif args.command in ['delete', 'complete', 'incomplete']:
            # Validate task ID
            if args.id <= 0:
                raise ValueError(f"Task ID must be a positive integer, got {args.id}")

        elif args.command == 'search':
            # Validate search keyword
            if not args.keyword or len(args.keyword.strip()) == 0:
                raise ValueError(f"Search keyword cannot be empty")

        return True
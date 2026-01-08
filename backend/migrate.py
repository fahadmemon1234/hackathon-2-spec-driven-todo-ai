#!/usr/bin/env python3
"""Migration script to create conversations and messages tables."""

import os
from dotenv import load_dotenv
from sqlmodel import create_engine, text
from models import Conversation, Message, Task

def main():
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not found in environment")
        return

    print(f"Using database URL: {DATABASE_URL[:50]}...")

    try:
        # Create engine
        engine = create_engine(DATABASE_URL, echo=True)

        print("\nCreating conversations and messages tables...")

        # Import models to register them with SQLModel metadata
        from models import SQLModel
        SQLModel.metadata.create_all(engine)

        print("Tables created successfully!")

        # Verify the tables exist
        with engine.connect() as conn:
            # Check if conversations table exists (SQLModel creates table names from class names)
            result = conn.execute(text("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables
                   WHERE table_schema = 'public'
                   AND table_name = 'conversation'
                );
            """))
            conversations_exist = result.scalar()

            # Check if messages table exists (SQLModel creates table names from class names)
            result = conn.execute(text("""
                SELECT EXISTS (
                   SELECT FROM information_schema.tables
                   WHERE table_schema = 'public'
                   AND table_name = 'message'
                );
            """))
            messages_exist = result.scalar()

            print(f"Conversations table exists: {conversations_exist}")
            print(f"Messages table exists: {messages_exist}")

            if conversations_exist and messages_exist:
                print("\n[SUCCESS] Migration completed successfully!")
            else:
                print("\n[ERROR] Migration may not have completed properly")

    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
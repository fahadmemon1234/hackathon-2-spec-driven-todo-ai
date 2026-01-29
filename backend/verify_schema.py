#!/usr/bin/env python3
"""Script to verify that the database schema matches the model definition."""

import os
from dotenv import load_dotenv
from sqlmodel import create_engine, text
from backend.models import Task, User, Conversation, Message

def main():
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL', '')
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not found in environment")
        return

    print(f"Using database URL: {DATABASE_URL[:50]}...")

    try:
        # Create engine
        engine = create_engine(DATABASE_URL, echo=False)

        print("\nVerifying schema matches model definition...")

        # Check the Task model
        model_fields = []
        for field_name in Task.model_fields.keys():
            model_fields.append(field_name)

        print(f"Fields defined in Task model: {model_fields}")

        # Check the database columns for task
        with engine.connect() as conn:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task';"))
            db_columns = [row[0] for row in result.fetchall()]

        print(f"Columns in task database table: {db_columns}")

        # Check if all model fields exist in the database
        missing_in_db = []
        for field in model_fields:
            if field not in db_columns:
                missing_in_db.append(field)

        extra_in_db = []
        for col in db_columns:
            if col not in [f for f in model_fields]:
                extra_in_db.append(col)

        if missing_in_db:
            print(f"\n[ERROR] MISSING IN DATABASE: {missing_in_db}")
        else:
            print("\n[SUCCESS] All model fields exist in database")

        if extra_in_db:
            print(f"\n[INFO] EXTRA IN DATABASE (not in model): {extra_in_db}")
        else:
            print("[SUCCESS] No extra columns in database")

        # Specifically check for priority and category
        if 'priority' in db_columns:
            print("[SUCCESS] Priority column exists in database")
        else:
            print("[ERROR] Priority column missing from database")

        if 'category' in db_columns:
            print("[SUCCESS] Category column exists in database")
        else:
            print("[ERROR] Category column missing from database")

        if not missing_in_db:
            print("\n[SUCCESS] Database schema is in sync with model definition!")
        else:
            print(f"\n[INFO] Need to add missing columns: {missing_in_db}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
"""
Script to fix the alembic version table by updating the revision ID to match the actual file.
"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment or use default
database_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# Create engine
engine = create_engine(database_url)

# Update the alembic_version table to match the actual revision ID in the file
with engine.connect() as conn:
    # First, check current version
    result = conn.execute(text("SELECT * FROM alembic_version"))
    current_version = result.fetchone()
    if current_version:
        print(f"Current version in alembic_version table: {current_version[0]}")
        
        # Update to match the actual revision ID in the file
        conn.execute(text("UPDATE alembic_version SET version_num = 'advanced_features_001'"))
        conn.commit()
        print("Updated alembic_version table to 'advanced_features_001'")
    else:
        # If no version exists, insert it
        conn.execute(text("INSERT INTO alembic_version (version_num) VALUES ('advanced_features_001')"))
        conn.commit()
        print("Inserted 'advanced_features_001' into alembic_version table")

print("Alembic version table updated successfully.")
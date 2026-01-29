#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add the backend directory to Python path
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

# Change to the backend directory
os.chdir(backend_dir)

# Clear any existing models to avoid conflicts
import gc
import importlib
import sys

# Remove any previously loaded modules to avoid conflicts
modules_to_remove = [mod for mod in sys.modules if mod.startswith('backend') or mod.startswith('models')]
for mod in modules_to_remove:
    del sys.modules[mod]

# Force garbage collection
gc.collect()

# Now run the uvicorn server
if __name__ == "__main__":
    import uvicorn
    # Import the app after setting up the path
    from main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
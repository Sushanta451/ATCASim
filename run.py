import os
import sys

# Path to root of the project (folder containing run.py)
ROOT = os.path.dirname(os.path.abspath(__file__))

# Add src/ to Python path
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

# Import radar entry point
from radar.radar_main import main

if __name__ == "__main__":
    main()

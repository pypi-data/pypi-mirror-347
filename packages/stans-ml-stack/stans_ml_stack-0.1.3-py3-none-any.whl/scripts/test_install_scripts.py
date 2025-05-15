#!/usr/bin/env python3

import os
import sys

# Add the parent directory to the path so we can import from the UI script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the components from the UI script
from scripts.install_ml_stack_ui import CORE_COMPONENTS, EXTENSION_COMPONENTS, SCRIPTS_DIR

def check_script_exists(component):
    """Check if the installation script for a component exists."""
    script_path = os.path.join(SCRIPTS_DIR, component["script"])
    exists = os.path.exists(script_path)
    print(f"Script for {component['name']}: {component['script']} - {'EXISTS' if exists else 'MISSING'}")
    return exists

def main():
    """Main function."""
    print("Checking CORE_COMPONENTS scripts...")
    core_missing = []
    for component in CORE_COMPONENTS:
        if not check_script_exists(component):
            core_missing.append(component["name"])
    
    print("\nChecking EXTENSION_COMPONENTS scripts...")
    ext_missing = []
    for component in EXTENSION_COMPONENTS:
        if not check_script_exists(component):
            ext_missing.append(component["name"])
    
    print("\nSummary:")
    print(f"Core components with missing scripts: {core_missing}")
    print(f"Extension components with missing scripts: {ext_missing}")

if __name__ == "__main__":
    main()

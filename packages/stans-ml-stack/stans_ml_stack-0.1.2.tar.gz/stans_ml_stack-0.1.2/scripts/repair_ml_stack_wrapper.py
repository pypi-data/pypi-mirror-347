#!/usr/bin/env python3
"""
Wrapper script for repair_ml_stack.sh.
This script provides a Python entry point for the repair_ml_stack.sh script.
"""

import os
import sys
import subprocess

def main():
    """
    Main entry point for the ML Stack repair.
    This function is called when the script is run directly or through the ml-stack-repair command.
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the repair_ml_stack.sh script
    repair_script = os.path.join(script_dir, "repair_ml_stack.sh")
    
    # Make sure the script is executable
    if not os.access(repair_script, os.X_OK):
        os.chmod(repair_script, 0o755)
    
    try:
        # Run the repair script
        result = subprocess.run([repair_script], check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("Repair interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error running repair script: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

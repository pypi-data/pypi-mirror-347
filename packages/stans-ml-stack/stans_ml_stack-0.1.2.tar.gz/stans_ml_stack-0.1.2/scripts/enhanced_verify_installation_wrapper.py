#!/usr/bin/env python3
"""
Wrapper script for enhanced_verify_installation.sh.
This script provides a Python entry point for the enhanced_verify_installation.sh script.
"""

import os
import sys
import subprocess

def main():
    """
    Main entry point for the ML Stack verification.
    This function is called when the script is run directly or through the ml-stack-verify command.
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the enhanced_verify_installation.sh script
    verify_script = os.path.join(script_dir, "enhanced_verify_installation.sh")
    
    # Make sure the script is executable
    if not os.access(verify_script, os.X_OK):
        os.chmod(verify_script, 0o755)
    
    try:
        # Run the verification script
        result = subprocess.run([verify_script], check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("Verification interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error running verification script: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

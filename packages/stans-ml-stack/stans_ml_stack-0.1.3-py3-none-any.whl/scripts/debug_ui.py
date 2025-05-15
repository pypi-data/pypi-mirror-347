#!/usr/bin/env python3
"""
Debug script for the ML Stack UI
"""

import os
import sys
import platform
import subprocess
from datetime import datetime

# Constants
HOME_DIR = os.path.expanduser("~")
MLSTACK_DIR = os.path.join(HOME_DIR, "Prod", "Stan-s-ML-Stack")
SCRIPTS_DIR = os.path.join(MLSTACK_DIR, "scripts")
LOGS_DIR = os.path.join(MLSTACK_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

def log_message(message):
    """Log a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")
    
    print(log_line)

def run_command(command):
    """Run a shell command and return the return code, stdout, and stderr."""
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        return_code = process.returncode
        
        return return_code, stdout, stderr
    except Exception as e:
        return 1, "", f"Error: {str(e)}"

def main():
    """Main function."""
    # Create log file
    with open(LOG_FILE, "w") as f:
        f.write(f"ML Stack UI Debug Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"System: {platform.system()} {platform.release()}\n")
        f.write(f"Python: {platform.python_version()}\n")
        f.write("-" * 80 + "\n\n")
    
    log_message("Starting debug script")
    
    # Test importing textual
    log_message("Testing textual import")
    try:
        from textual.app import App
        log_message("Successfully imported textual.app.App")
    except ImportError as e:
        log_message(f"Failed to import textual.app.App: {str(e)}")
        return_code, stdout, stderr = run_command(f"{sys.executable} -m pip install textual")
        log_message(f"Installed textual: {return_code}, {stderr}")
        try:
            from textual.app import App
            log_message("Successfully imported textual.app.App after installation")
        except ImportError as e:
            log_message(f"Still failed to import textual.app.App: {str(e)}")
    
    # Test creating a simple textual app
    log_message("Testing simple textual app")
    try:
        from textual.app import App
        
        class SimpleApp(App):
            def on_mount(self):
                log_message("SimpleApp mounted")
                self.exit()
        
        log_message("Created SimpleApp class")
        app = SimpleApp()
        log_message("Created SimpleApp instance")
        log_message("Running SimpleApp")
        app.run()
        log_message("SimpleApp ran successfully")
    except Exception as e:
        log_message(f"Error running SimpleApp: {str(e)}")
        import traceback
        log_message(f"Traceback: {traceback.format_exc()}")
    
    log_message("Debug script completed")

if __name__ == "__main__":
    main()

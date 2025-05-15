#!/usr/bin/env python3
"""
Test script for the ML Stack UI
"""

import os
import sys
import platform
import subprocess
import shlex
from datetime import datetime
from typing import Optional, Tuple

# Constants
HOME_DIR = os.path.expanduser("~")
MLSTACK_DIR = os.path.join(HOME_DIR, "Prod", "Stan-s-ML-Stack")
SCRIPTS_DIR = os.path.join(MLSTACK_DIR, "scripts")
LOGS_DIR = os.path.join(MLSTACK_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, f"test_ui_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Global variable to store sudo password
SUDO_PASSWORD = None

def log_message(message, level="INFO"):
    """Log a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")
    
    print(log_line)

def run_command(command, timeout=30, use_sudo=False) -> Tuple[int, str, str]:
    """Run a shell command and return the return code, stdout, and stderr."""
    global SUDO_PASSWORD
    
    # If the command starts with sudo and we have a sudo password, use it
    if command.strip().startswith("sudo") and SUDO_PASSWORD:
        log_message(f"Running sudo command with cached credentials: {command}")
        # Modify the command to use the stored sudo password
        command = f"echo {shlex.quote(SUDO_PASSWORD)} | sudo -S {command[5:]}"
    elif use_sudo and SUDO_PASSWORD:
        log_message(f"Running command with sudo: {command}")
        # Add sudo with password to the command
        command = f"echo {shlex.quote(SUDO_PASSWORD)} | sudo -S {command}"
    else:
        log_message(f"Running command: {command}")
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            log_message(f"Command timed out after {timeout} seconds: {command}", "WARNING")
            return 1, "", f"Command timed out after {timeout} seconds"
        
        if return_code != 0:
            log_message(f"Command failed with return code {return_code}", "ERROR")
            log_message(f"stderr: {stderr}", "ERROR")
        
        return return_code, stdout, stderr
    except Exception as e:
        log_message(f"Error executing command: {str(e)}", "ERROR")
        return 1, "", f"Error: {str(e)}"

def verify_sudo_password(password):
    """Verify the sudo password."""
    log_message("Starting sudo password verification")
    if not password:
        log_message("No password entered")
        return False
    
    log_message("Verifying sudo access")
    
    # Create a temporary script to verify sudo access
    temp_script = os.path.join(SCRIPTS_DIR, "temp_sudo_verify.sh")
    with open(temp_script, "w") as f:
        f.write("""#!/bin/bash
echo "$1" | sudo -S echo "Success" 2>/dev/null
if [ $? -eq 0 ]; then
    # Cache sudo credentials for a while
    echo "$1" | sudo -S echo "Caching sudo credentials" > /dev/null 2>&1
    exit 0
else
    exit 1
fi
""")
    
    # Make the script executable
    os.chmod(temp_script, 0o755)
    log_message(f"Created verification script at {temp_script}")
    
    # Run the script
    log_message("Running sudo verification script")
    return_code, stdout, stderr = run_command(f"bash {temp_script} {shlex.quote(password)}")
    log_message(f"Verification script returned: {return_code}")
    
    # Clean up
    os.remove(temp_script)
    log_message("Removed verification script")
    
    if return_code == 0:
        # Store the password in a global variable for later use
        global SUDO_PASSWORD
        SUDO_PASSWORD = password
        log_message("Sudo password verified successfully")
        return True
    else:
        log_message("Incorrect sudo password")
        return False

def main():
    """Main function."""
    # Create log file
    with open(LOG_FILE, "w") as f:
        f.write(f"ML Stack UI Test Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"System: {platform.system()} {platform.release()}\n")
        f.write(f"Python: {platform.python_version()}\n")
        f.write("-" * 80 + "\n\n")
    
    log_message("Starting test script")
    
    # Test importing textual
    log_message("Testing textual import")
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Container
        from textual.widgets import Header, Footer, Static, Button, Input
        from textual.screen import Screen
        log_message("Successfully imported textual modules")
    except ImportError as e:
        log_message(f"Failed to import textual modules: {str(e)}", "ERROR")
        return
    
    # Test creating a simple textual app with screens
    log_message("Testing textual app with screens")
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Container
        from textual.widgets import Header, Footer, Static, Button, Input
        from textual.screen import Screen
        
        class PasswordScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Header(show_clock=True)
                with Container(id="password-container"):
                    yield Static("Enter Password", id="password-title")
                    yield Input(placeholder="Enter password", password=True, id="password-input")
                    yield Button("Continue", id="continue-button")
                    yield Static("", id="status")
                yield Footer()
            
            def on_button_pressed(self, event: Button.Pressed) -> None:
                if event.button.id == "continue-button":
                    self.verify_password()
            
            def on_input_submitted(self, event: Input.Submitted) -> None:
                if event.input.id == "password-input":
                    self.verify_password()
            
            def verify_password(self) -> None:
                password = self.query_one("#password-input").value
                self.query_one("#status").update("Verifying password...")
                
                if verify_sudo_password(password):
                    self.query_one("#status").update("Password verified!")
                    self.app.push_screen(WelcomeScreen())
                else:
                    self.query_one("#status").update("Incorrect password!")
        
        class WelcomeScreen(Screen):
            def compose(self) -> ComposeResult:
                yield Header(show_clock=True)
                with Container(id="welcome-container"):
                    yield Static("Welcome!", id="welcome-title")
                    yield Static("You have successfully logged in.", id="welcome-message")
                    yield Button("Exit", id="exit-button")
                yield Footer()
            
            def on_button_pressed(self, event: Button.Pressed) -> None:
                if event.button.id == "exit-button":
                    self.app.exit()
            
            def on_mount(self) -> None:
                log_message("WelcomeScreen mounted")
        
        class TestApp(App):
            def on_mount(self) -> None:
                log_message("TestApp mounted")
                self.push_screen(PasswordScreen())
            
            def on_screen_resume(self, event) -> None:
                log_message(f"Screen resumed: {event.screen.__class__.__name__}")
            
            def on_screen_suspend(self, event) -> None:
                log_message(f"Screen suspended: {event.screen.__class__.__name__}")
        
        log_message("Created TestApp class")
        app = TestApp()
        log_message("Created TestApp instance")
        log_message("Running TestApp")
        app.run()
        log_message("TestApp ran successfully")
    except Exception as e:
        log_message(f"Error running TestApp: {str(e)}", "ERROR")
        import traceback
        log_message(f"Traceback: {traceback.format_exc()}", "ERROR")
    
    log_message("Test script completed")

if __name__ == "__main__":
    main()

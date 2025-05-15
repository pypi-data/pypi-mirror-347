#!/usr/bin/env python3

import os
import sys
from textual.app import App

# Add the parent directory to the path so we can import from the UI script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the InstallationScreen from the UI script
from scripts.install_ml_stack_ui import InstallationScreen, log_message

class TestApp(App):
    """Test app for the InstallationScreen."""
    
    def on_mount(self):
        """Mount the InstallationScreen."""
        log_message("TestApp mounted")
        self.push_screen(InstallationScreen())
        log_message("InstallationScreen pushed")

def main():
    """Main function."""
    app = TestApp()
    app.run()

if __name__ == "__main__":
    main()

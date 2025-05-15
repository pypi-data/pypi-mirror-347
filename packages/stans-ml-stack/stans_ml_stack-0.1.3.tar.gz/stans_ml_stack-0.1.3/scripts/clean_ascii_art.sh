#!/bin/bash
#
# Author: Stanley Chisango (Scooter Lacroix)
# Email: scooterlacroix@gmail.com
# GitHub: https://github.com/scooter-lacroix
# X: https://x.com/scooter_lacroix
# Patreon: https://patreon.com/ScooterLacroix
#
# If this code saved you time, consider buying me a coffee! ☕
# "Code is like humor. When you have to explain it, it's bad!" - Cory House
#
# =============================================================================
# ASCII Art Cleaner Script
# =============================================================================
# This script cleans up the ASCII art file by removing problematic ANSI escape
# sequences that might cause display issues in the terminal.
#
# Date: $(date +"%Y-%m-%d")
# =============================================================================

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
UNDERLINE='\033[4m'
RESET='\033[0m'

# Function to print colored messages
print_header() {
    echo -e "${CYAN}${BOLD}=== $1 ===${RESET}"
    echo
}

print_step() {
    echo -e "${MAGENTA}>> $1${RESET}"
}

print_success() {
    echo -e "${GREEN}✓ $1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${RESET}"
}

print_error() {
    echo -e "${RED}✗ $1${RESET}"
}

# Main function
clean_ascii_art() {
    print_header "ASCII Art Cleaner"

    # Get the directory paths
    SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
    ASSETS_DIR="$(dirname "$SCRIPT_DIR")/assets"
    
    # Check if assets directory exists
    if [ ! -d "$ASSETS_DIR" ]; then
        print_error "Assets directory not found: $ASSETS_DIR"
        exit 1
    fi
    
    # Check if the ASCII art file exists
    ASCII_FILE="$ASSETS_DIR/ml_stack_logo_ascii.txt"
    if [ ! -f "$ASCII_FILE" ]; then
        print_error "ASCII art file not found: $ASCII_FILE"
        exit 1
    fi
    
    print_step "Cleaning ASCII art file: $ASCII_FILE"
    
    # Create a temporary file
    TEMP_FILE="$ASCII_FILE.tmp"
    
    # Remove problematic ANSI escape sequences
    # This keeps the color codes but removes cursor movement and other problematic sequences
    cat "$ASCII_FILE" | sed 's/\x1b\[?25[hl]//g' | sed 's/\x1b\[0m\s*//g' > "$TEMP_FILE"
    
    # Replace the original file with the cleaned version
    mv "$TEMP_FILE" "$ASCII_FILE"
    
    print_success "ASCII art file cleaned successfully"
    
    # Display the cleaned ASCII art
    print_step "Displaying cleaned ASCII art..."
    cat "$ASCII_FILE"
    
    print_success "ASCII art cleaning completed"
}

# Run the main function
clean_ascii_art

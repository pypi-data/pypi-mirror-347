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
# ASCII Art Generator Script
# =============================================================================
# This script generates ASCII art from the ML Stack logo and saves it to a file.
# It uses jp2a to convert the PNG image to colored ASCII art.
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

print_section() {
    echo -e "${BLUE}${BOLD}>>> $1${RESET}"
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main function
generate_ascii_art() {
    print_header "ASCII Art Generator"

    # Get the directory paths
    SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
    ASSETS_DIR="$(dirname "$SCRIPT_DIR")/assets"
    
    # Check if assets directory exists
    if [ ! -d "$ASSETS_DIR" ]; then
        print_error "Assets directory not found: $ASSETS_DIR"
        exit 1
    fi
    
    # Check if the logo exists
    LOGO_PATH="$ASSETS_DIR/ml_stack_logo.png"
    if [ ! -f "$LOGO_PATH" ]; then
        print_error "ML Stack logo not found: $LOGO_PATH"
        exit 1
    fi
    
    # Check if jp2a is installed
    if ! command_exists jp2a; then
        print_error "jp2a is not installed. Please install it first."
        print_step "On Debian/Ubuntu: sudo apt-get install jp2a"
        exit 1
    fi
    
    # Generate ASCII art
    print_step "Generating ASCII art from $LOGO_PATH"
    ASCII_OUTPUT="$ASSETS_DIR/ml_stack_logo_ascii.txt"
    
    # Use jp2a to generate colored ASCII art
    jp2a --width=80 --height=40 --colors "$LOGO_PATH" > "$ASCII_OUTPUT"
    
    # Check if the file was created successfully
    if [ -f "$ASCII_OUTPUT" ] && [ -s "$ASCII_OUTPUT" ]; then
        print_success "ASCII art generated successfully: $ASCII_OUTPUT"
    else
        print_error "Failed to generate ASCII art"
        exit 1
    fi
    
    print_success "ASCII art generation completed"
}

# Run the main function
generate_ascii_art

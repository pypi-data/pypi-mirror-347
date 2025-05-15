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
# Chafa Installation Script
# =============================================================================
# This script installs Chafa, a terminal graphics utility that can display
# images in the terminal. It's used by the ML Stack installer to display
# the logo and other graphics.
#
# Date: $(date +"%Y-%m-%d")
# =============================================================================

# ASCII Art Banner
cat << "EOF"
  ██████╗██╗  ██╗ █████╗ ███████╗ █████╗     ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ███████╗██████╗ 
 ██╔════╝██║  ██║██╔══██╗██╔════╝██╔══██╗    ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔════╝██╔══██╗
 ██║     ███████║███████║█████╗  ███████║    ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     █████╗  ██████╔╝
 ██║     ██╔══██║██╔══██║██╔══╝  ██╔══██║    ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══╝  ██╔══██╗
 ╚██████╗██║  ██║██║  ██║██║     ██║  ██║    ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗███████╗██║  ██║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝    ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                                    
                                Terminal Graphics Utility Installer
EOF
echo

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

# Function to show progress bar
show_progress_bar() {
    local duration=$1
    local steps=20
    local sleep_time=$(echo "scale=2; $duration/$steps" | bc)
    
    echo -ne "${CYAN}["
    for ((i=0; i<steps; i++)); do
        echo -ne "${GREEN}#"
        sleep $sleep_time
    done
    echo -e "${CYAN}] ${GREEN}Done!${RESET}"
}

# Main installation function
install_chafa() {
    print_header "Chafa Installation"
    
    # Check if chafa is already installed
    if command_exists chafa; then
        print_warning "Chafa is already installed"
        chafa_version=$(chafa --version | head -n 1)
        print_step "Current version: $chafa_version"
        
        read -p "Do you want to reinstall? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_step "Skipping Chafa installation"
            return 0
        fi
    fi
    
    print_section "Installing dependencies"
    
    # Install dependencies
    print_step "Installing required packages..."
    sudo apt-get update
    sudo apt-get install -y build-essential libglib2.0-dev libmagickwand-dev libavcodec-dev libavformat-dev libswscale-dev libfreetype6-dev
    
    # Check if installation from package manager is possible
    print_step "Checking if Chafa is available in package manager..."
    if apt-cache show chafa &>/dev/null; then
        print_step "Installing Chafa from package manager..."
        sudo apt-get install -y chafa
        
        if command_exists chafa; then
            chafa_version=$(chafa --version | head -n 1)
            print_success "Chafa installed successfully from package manager"
            print_step "Version: $chafa_version"
            return 0
        else
            print_warning "Failed to install Chafa from package manager, trying from source..."
        fi
    else
        print_step "Chafa not available in package manager, installing from source..."
    fi
    
    # Create temporary directory
    print_step "Creating temporary directory..."
    temp_dir=$(mktemp -d)
    cd "$temp_dir"
    
    # Clone repository
    print_step "Cloning Chafa repository..."
    git clone https://github.com/hpjansson/chafa.git
    cd chafa
    
    # Configure and build
    print_step "Configuring build..."
    ./autogen.sh
    
    print_step "Building Chafa (this may take a while)..."
    make -j$(nproc) &
    make_pid=$!
    
    # Show progress bar while building
    show_progress_bar 30
    
    # Wait for make to complete
    wait $make_pid
    
    # Install
    print_step "Installing Chafa..."
    sudo make install
    
    # Update library cache
    print_step "Updating library cache..."
    sudo ldconfig
    
    # Clean up
    print_step "Cleaning up..."
    cd
    rm -rf "$temp_dir"
    
    # Verify installation
    if command_exists chafa; then
        chafa_version=$(chafa --version | head -n 1)
        print_success "Chafa installed successfully from source"
        print_step "Version: $chafa_version"
        return 0
    else
        print_error "Failed to install Chafa"
        return 1
    fi
}

# Run the installation function
install_chafa

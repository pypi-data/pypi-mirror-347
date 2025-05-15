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
# Assets Setup Script
# =============================================================================
# This script sets up the assets directory and downloads the ML Stack logo.
# It also installs chafa, a terminal graphics utility for displaying images.
#
# Date: $(date +"%Y-%m-%d")
# =============================================================================

# ASCII Art Banner
cat << "EOF"
  █████╗ ███████╗███████╗███████╗████████╗███████╗    ███████╗███████╗████████╗██╗   ██╗██████╗
 ██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
 ███████║███████╗███████╗█████╗     ██║   ███████╗    ███████╗█████╗     ██║   ██║   ██║██████╔╝
 ██╔══██║╚════██║╚════██║██╔══╝     ██║   ╚════██║    ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝
 ██║  ██║███████║███████║███████╗   ██║   ███████║    ███████║███████╗   ██║   ╚██████╔╝██║
 ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   ╚══════╝    ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝

                                  Assets Setup Script
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

# Main function
setup_assets() {
    print_header "Assets Setup"

    # Create assets directory
    print_step "Creating assets directory..."
    ASSETS_DIR="$(dirname "$(dirname "$0")")/assets"
    mkdir -p "$ASSETS_DIR"

    # Download ML Stack logo
    print_step "Downloading ML Stack logo..."
    if [ -f "$ASSETS_DIR/ml_stack_logo.png" ]; then
        print_warning "ML Stack logo already exists, skipping download"
    else
        # Try to download the logo from GitHub
        wget -q -O "$ASSETS_DIR/ml_stack_logo.png" "https://raw.githubusercontent.com/scooter-lacroix/Stan-s-ML-Stack/main/assets/ml_stack_logo.png" || \
        curl -s -o "$ASSETS_DIR/ml_stack_logo.png" "https://raw.githubusercontent.com/scooter-lacroix/Stan-s-ML-Stack/main/assets/ml_stack_logo.png"

        # Check if download was successful
        if [ -f "$ASSETS_DIR/ml_stack_logo.png" ] && [ -s "$ASSETS_DIR/ml_stack_logo.png" ]; then
            print_success "ML Stack logo downloaded successfully"
        else
            print_warning "Failed to download ML Stack logo, creating a placeholder"

            # Create a placeholder logo using ImageMagick if available
            if command_exists convert; then
                print_step "Creating placeholder logo using ImageMagick..."
                convert -size 200x100 xc:transparent -font Arial -pointsize 24 -fill orange -gravity center -annotate 0 "Stan's ML Stack" "$ASSETS_DIR/ml_stack_logo.png"
                print_success "Placeholder logo created successfully"
            else
                print_warning "ImageMagick not available, skipping placeholder creation"
            fi
        fi
    fi

    # Install chafa
    print_step "Installing chafa..."
    if command_exists chafa; then
        print_success "chafa is already installed"
    else
        # Check if the install script exists
        if [ -f "$(dirname "$0")/install_chafa.sh" ]; then
            print_step "Running chafa installation script..."
            bash "$(dirname "$0")/install_chafa.sh"
        else
            print_warning "chafa installation script not found, trying to install directly"

            # Try to install chafa directly
            if command_exists apt-get; then
                print_step "Installing chafa using apt-get..."
                sudo apt-get update
                sudo apt-get install -y chafa
            elif command_exists brew; then
                print_step "Installing chafa using brew..."
                brew install chafa
            else
                print_error "No package manager found, cannot install chafa"
            fi
        fi

        # Check if installation was successful
        if command_exists chafa; then
            print_success "chafa installed successfully"
        else
            print_error "Failed to install chafa"
        fi
    fi

    # Test chafa with the logo
    if command_exists chafa && [ -f "$ASSETS_DIR/ml_stack_logo.png" ]; then
        print_step "Testing chafa with the logo..."
        # Use the same options as in the UI script for consistency
        chafa --size=80x40 --colors=256 --color-space=rgb --symbols=all --dither=diffusion "$ASSETS_DIR/ml_stack_logo.png"
        print_success "chafa test successful"
    fi

    # Generate ASCII art version of the logo using jp2a
    if command_exists jp2a && [ -f "$ASSETS_DIR/ml_stack_logo.png" ]; then
        print_step "Generating ASCII art with jp2a..."
        # Generate colored ASCII art and save to file
        jp2a --width=80 --height=40 --colors "$ASSETS_DIR/ml_stack_logo.png" > "$ASSETS_DIR/ml_stack_logo_ascii.txt"

        # Check if the file was created successfully
        if [ -f "$ASSETS_DIR/ml_stack_logo_ascii.txt" ] && [ -s "$ASSETS_DIR/ml_stack_logo_ascii.txt" ]; then
            print_success "ASCII art generated successfully"

            # Clean the ASCII art file
            print_step "Cleaning ASCII art file..."
            # Remove problematic ANSI escape sequences
            # This keeps the color codes but removes cursor movement and other problematic sequences
            TEMP_FILE="$ASSETS_DIR/ml_stack_logo_ascii.tmp"
            cat "$ASSETS_DIR/ml_stack_logo_ascii.txt" | sed 's/\x1b\[?25[hl]//g' | sed 's/\x1b\[0m\s*//g' > "$TEMP_FILE"
            mv "$TEMP_FILE" "$ASSETS_DIR/ml_stack_logo_ascii.txt"
            print_success "ASCII art file cleaned successfully"

            # Display the ASCII art
            print_step "Displaying ASCII art..."
            cat "$ASSETS_DIR/ml_stack_logo_ascii.txt"
            print_success "ASCII art display successful"
        else
            print_warning "Failed to generate ASCII art"
        fi
    else
        if ! command_exists jp2a; then
            print_warning "jp2a is not installed, cannot generate ASCII art"

            # Try to install jp2a
            if command_exists apt-get; then
                print_step "Installing jp2a using apt-get..."
                sudo apt-get update
                sudo apt-get install -y jp2a

                # Check if installation was successful
                if command_exists jp2a; then
                    print_success "jp2a installed successfully"

                    # Generate ASCII art
                    print_step "Generating ASCII art with jp2a..."
                    jp2a --width=80 --height=40 --colors "$ASSETS_DIR/ml_stack_logo.png" > "$ASSETS_DIR/ml_stack_logo_ascii.txt"

                    if [ -f "$ASSETS_DIR/ml_stack_logo_ascii.txt" ] && [ -s "$ASSETS_DIR/ml_stack_logo_ascii.txt" ]; then
                        print_success "ASCII art generated successfully"

                        # Clean the ASCII art file
                        print_step "Cleaning ASCII art file..."
                        # Remove problematic ANSI escape sequences
                        TEMP_FILE="$ASSETS_DIR/ml_stack_logo_ascii.tmp"
                        cat "$ASSETS_DIR/ml_stack_logo_ascii.txt" | sed 's/\x1b\[?25[hl]//g' | sed 's/\x1b\[0m\s*//g' > "$TEMP_FILE"
                        mv "$TEMP_FILE" "$ASSETS_DIR/ml_stack_logo_ascii.txt"
                        print_success "ASCII art file cleaned successfully"
                    else
                        print_warning "Failed to generate ASCII art"
                    fi
                else
                    print_error "Failed to install jp2a"
                fi
            elif command_exists brew; then
                print_step "Installing jp2a using brew..."
                brew install jp2a

                # Check if installation was successful
                if command_exists jp2a; then
                    print_success "jp2a installed successfully"

                    # Generate ASCII art
                    print_step "Generating ASCII art with jp2a..."
                    jp2a --width=80 --height=40 --colors "$ASSETS_DIR/ml_stack_logo.png" > "$ASSETS_DIR/ml_stack_logo_ascii.txt"

                    if [ -f "$ASSETS_DIR/ml_stack_logo_ascii.txt" ] && [ -s "$ASSETS_DIR/ml_stack_logo_ascii.txt" ]; then
                        print_success "ASCII art generated successfully"

                        # Clean the ASCII art file
                        print_step "Cleaning ASCII art file..."
                        # Remove problematic ANSI escape sequences
                        TEMP_FILE="$ASSETS_DIR/ml_stack_logo_ascii.tmp"
                        cat "$ASSETS_DIR/ml_stack_logo_ascii.txt" | sed 's/\x1b\[?25[hl]//g' | sed 's/\x1b\[0m\s*//g' > "$TEMP_FILE"
                        mv "$TEMP_FILE" "$ASSETS_DIR/ml_stack_logo_ascii.txt"
                        print_success "ASCII art file cleaned successfully"
                    else
                        print_warning "Failed to generate ASCII art"
                    fi
                else
                    print_error "Failed to install jp2a"
                fi
            else
                print_error "No package manager found, cannot install jp2a"
            fi
        fi

        # Verify the image is a valid PNG
        if command_exists file; then
            file_type=$(file -b "$ASSETS_DIR/ml_stack_logo.png")
            if echo "$file_type" | grep -q "PNG image"; then
                print_success "Image verified as PNG: $file_type"
            else
                print_warning "Image may not be a valid PNG: $file_type"
                print_step "Attempting to fix the image..."

                # Try to convert the image to PNG if ImageMagick is available
                if command_exists convert; then
                    mv "$ASSETS_DIR/ml_stack_logo.png" "$ASSETS_DIR/ml_stack_logo.png.bak"
                    convert "$ASSETS_DIR/ml_stack_logo.png.bak" "$ASSETS_DIR/ml_stack_logo.png"

                    # Check if conversion was successful
                    if [ -f "$ASSETS_DIR/ml_stack_logo.png" ] && [ -s "$ASSETS_DIR/ml_stack_logo.png" ]; then
                        file_type=$(file -b "$ASSETS_DIR/ml_stack_logo.png")
                        if echo "$file_type" | grep -q "PNG image"; then
                            print_success "Image successfully converted to PNG: $file_type"
                        else
                            print_error "Failed to convert image to PNG"
                            # Restore original
                            mv "$ASSETS_DIR/ml_stack_logo.png.bak" "$ASSETS_DIR/ml_stack_logo.png"
                        fi
                    else
                        print_error "Failed to convert image"
                        # Restore original
                        mv "$ASSETS_DIR/ml_stack_logo.png.bak" "$ASSETS_DIR/ml_stack_logo.png"
                    fi
                else
                    print_warning "ImageMagick not available, cannot convert image"
                fi
            fi
        fi
    fi

    print_success "Assets setup completed successfully"
}

# Run the main function
setup_assets

#!/bin/bash

# Set up colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# Progress bar variables
PROGRESS_BAR_WIDTH=50
PROGRESS_CURRENT=0
PROGRESS_TOTAL=100
PROGRESS_CHAR="▓"
PROGRESS_EMPTY="░"
PROGRESS_ANIMATION=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
ANIMATION_INDEX=0

# Suppress HIP logs
export AMD_LOG_LEVEL=0
export HIP_VISIBLE_DEVICES=0,1,2
export ROCR_VISIBLE_DEVICES=0,1,2

# Function to initialize progress bar
init_progress_bar() {
    PROGRESS_TOTAL=$1
    PROGRESS_CURRENT=0
    
    # Save cursor position
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        tput sc
        # Clear line and print initial progress bar
        tput el
        draw_progress_bar
        # Move cursor back to saved position
        tput rc
    fi
}

# Function to update progress bar
update_progress_bar() {
    local increment=${1:-1}
    PROGRESS_CURRENT=$((PROGRESS_CURRENT + increment))
    
    # Ensure we don't exceed the total
    if [ $PROGRESS_CURRENT -gt $PROGRESS_TOTAL ]; then
        PROGRESS_CURRENT=$PROGRESS_TOTAL
    fi
    
    # Save cursor position
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        tput sc
        # Move to top of terminal
        tput cup 0 0
        # Clear line and print updated progress bar
        tput el
        draw_progress_bar
        # Move cursor back to saved position
        tput rc
    fi
}

# Function to draw progress bar
draw_progress_bar() {
    local percent=$((PROGRESS_CURRENT * 100 / PROGRESS_TOTAL))
    local completed=$((PROGRESS_CURRENT * PROGRESS_BAR_WIDTH / PROGRESS_TOTAL))
    local remaining=$((PROGRESS_BAR_WIDTH - completed))
    
    # Update animation index
    ANIMATION_INDEX=$(( (ANIMATION_INDEX + 1) % ${#PROGRESS_ANIMATION[@]} ))
    local spinner=${PROGRESS_ANIMATION[$ANIMATION_INDEX]}
    
    # Draw progress bar with colors
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -ne "${CYAN}${BOLD}[${RESET}${MAGENTA}"
        for ((i=0; i<completed; i++)); do
            echo -ne "${PROGRESS_CHAR}"
        done
        
        for ((i=0; i<remaining; i++)); do
            echo -ne "${BLUE}${PROGRESS_EMPTY}"
        done
        
        echo -ne "${RESET}${CYAN}${BOLD}]${RESET} ${percent}% ${spinner} "
        
        # Add task description if provided
        if [ -n "$1" ]; then
            echo -ne "$1"
        fi
        
        echo -ne "\r"
    fi
}

# Function to complete progress bar
complete_progress_bar() {
    PROGRESS_CURRENT=$PROGRESS_TOTAL
    
    # Save cursor position
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        tput sc
        # Move to top of terminal
        tput cup 0 0
        # Clear line and print completed progress bar
        tput el
        draw_progress_bar "Complete!"
        echo
        # Move cursor back to saved position
        tput rc
    fi
}

# Function to print colored messages
print_header() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${CYAN}${BOLD}=== $1 ===${RESET}"
    else
        echo "=== $1 ==="
    fi
    echo
}

print_section() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${BLUE}${BOLD}>>> $1${RESET}"
    else
        echo ">>> $1"
    fi
}

print_step() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${MAGENTA}>> $1${RESET}"
    else
        echo ">> $1"
    fi
}

print_success() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${GREEN}✓ $1${RESET}"
    else
        echo "✓ $1"
    fi
}

print_warning() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${YELLOW}⚠ $1${RESET}"
    else
        echo "⚠ $1"
    fi
}

print_error() {
    if [ -t 1 ] && [ -z "$NO_COLOR" ]; then
        echo -e "${RED}✗ $1${RESET}"
    else
        echo "✗ $1"
    fi
}

# Function to check if a Python module exists
python_module_exists() {
    python3 -c "import $1" 2>/dev/null
    return $?
}

# Function to check if MPI is installed
check_mpi() {
    if command -v mpirun >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to install PyTorch with MPI support
install_pytorch_mpi() {
    print_header "Installing PyTorch with MPI Support"
    
    # Initialize progress bar
    init_progress_bar 100
    update_progress_bar 5
    draw_progress_bar "Checking MPI installation..."
    
    # Check if MPI is installed
    if ! check_mpi; then
        print_error "MPI is not installed. Please install MPI first."
        print_step "Run the install_mpi4py.sh script to install MPI."
        complete_progress_bar
        return 1
    fi
    
    print_success "MPI is installed"
    update_progress_bar 10
    draw_progress_bar "Checking PyTorch installation..."
    
    # Check if PyTorch is already installed
    if python_module_exists "torch"; then
        torch_version=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null)
        print_success "PyTorch is already installed (version: $torch_version)"
        
        # Check if PyTorch has MPI support
        if python3 -c "import torch; exit(0 if hasattr(torch.distributed, 'init_process_group') else 1)" 2>/dev/null; then
            print_success "PyTorch has MPI support"
            complete_progress_bar
            return 0
        else
            print_warning "PyTorch does not have MPI support, reinstalling..."
        fi
    else
        print_warning "PyTorch is not installed, installing..."
    fi
    
    update_progress_bar 20
    draw_progress_bar "Installing PyTorch with ROCm and MPI support..."
    
    # Install PyTorch with ROCm support
    print_step "Installing PyTorch with ROCm support..."
    
    # Set environment variables
    export PYTORCH_ROCM_ARCH=gfx900,gfx906,gfx908,gfx90a,gfx1030,gfx1100,gfx1101,gfx1102
    
    # Install PyTorch with ROCm support
    if command -v uv >/dev/null 2>&1; then
        uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
    else
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
    fi
    
    update_progress_bar 40
    draw_progress_bar "Installing PyTorch MPI support..."
    
    # Install PyTorch MPI support
    print_step "Installing PyTorch MPI support..."
    
    # Install torch-mpi
    if command -v uv >/dev/null 2>&1; then
        uv pip install torch-mpi
    else
        pip install torch-mpi
    fi
    
    update_progress_bar 60
    draw_progress_bar "Verifying installation..."
    
    # Verify installation
    if python_module_exists "torch"; then
        torch_version=$(python3 -c "import torch; print(torch.__version__)" 2>/dev/null)
        print_success "PyTorch is installed (version: $torch_version)"
        
        # Check if PyTorch has MPI support
        if python3 -c "import torch; exit(0 if hasattr(torch.distributed, 'init_process_group') else 1)" 2>/dev/null; then
            print_success "PyTorch has MPI support"
            complete_progress_bar
            return 0
        else
            print_warning "PyTorch does not have MPI support"
            print_step "You may need to build PyTorch from source with MPI support"
            complete_progress_bar
            return 1
        fi
    else
        print_error "PyTorch installation failed"
        complete_progress_bar
        return 1
    fi
}

# Main function
main() {
    install_pytorch_mpi
    return $?
}

# Run main function
main
exit $?

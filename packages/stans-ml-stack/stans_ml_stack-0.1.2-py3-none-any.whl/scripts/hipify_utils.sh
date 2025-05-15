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
# HIPIFY Utilities for AMD GPUs
# =============================================================================
# This script provides utilities for converting CUDA code to HIP for AMD GPUs.
# It's used by various installation scripts to ensure proper AMD compatibility.
#
# Date: $(date +"%Y-%m-%d")
# =============================================================================

# ASCII Art Banner
cat << "EOF"
  ██╗  ██╗██╗██████╗ ██╗███████╗██╗   ██╗    ██╗   ██╗████████╗██╗██╗     ███████╗
  ██║  ██║██║██╔══██╗██║██╔════╝╚██╗ ██╔╝    ██║   ██║╚══██╔══╝██║██║     ██╔════╝
  ███████║██║██████╔╝██║█████╗   ╚████╔╝     ██║   ██║   ██║   ██║██║     ███████╗
  ██╔══██║██║██╔═══╝ ██║██╔══╝    ╚██╔╝      ██║   ██║   ██║   ██║██║     ╚════██║
  ██║  ██║██║██║     ██║██║        ██║       ╚██████╔╝   ██║   ██║███████╗███████║
  ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚═╝        ╚═╝        ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝
                                                                                   
                    CUDA to HIP Conversion Utilities for AMD GPUs
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

# Function to check if hipify-perl is installed
check_hipify_tools() {
    print_section "Checking HIPIFY tools"
    
    if command -v hipify-perl &> /dev/null; then
        print_success "hipify-perl is installed"
    else
        print_warning "hipify-perl is not installed, attempting to install it"
        
        # Check if ROCm is installed
        if [ -d "/opt/rocm" ]; then
            print_step "ROCm is installed, installing hipify-perl"
            sudo apt-get update
            sudo apt-get install -y hipify-clang
            
            if command -v hipify-perl &> /dev/null; then
                print_success "hipify-perl installed successfully"
            else
                print_error "Failed to install hipify-perl"
                return 1
            fi
        else
            print_error "ROCm is not installed, cannot install hipify-perl"
            return 1
        fi
    fi
    
    return 0
}

# Function to hipify a single file
hipify_file() {
    local input_file=$1
    local output_file=$2
    
    print_step "Hipifying file: $input_file -> $output_file"
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$output_file")"
    
    # Hipify the file
    hipify-perl "$input_file" > "$output_file"
    
    if [ $? -eq 0 ]; then
        print_success "File hipified successfully"
        return 0
    else
        print_error "Failed to hipify file"
        return 1
    fi
}

# Function to hipify a directory
hipify_directory() {
    local input_dir=$1
    local output_dir=$2
    local file_pattern=${3:-"*.cu *.cuh *.cpp *.h *.hpp *.cc"}
    
    print_section "Hipifying directory: $input_dir -> $output_dir"
    
    # Create output directory if it doesn't exist
    mkdir -p "$output_dir"
    
    # Find all files matching the pattern
    local files=$(find "$input_dir" -type f -name "*.cu" -o -name "*.cuh" -o -name "*.cpp" -o -name "*.h" -o -name "*.hpp" -o -name "*.cc")
    
    local success_count=0
    local failure_count=0
    
    for file in $files; do
        # Get relative path
        local rel_path=${file#$input_dir/}
        local output_file="$output_dir/$rel_path"
        
        # Replace .cu with .hip.cpp and .cuh with .hip.hpp
        if [[ "$output_file" == *.cu ]]; then
            output_file="${output_file%.cu}.hip.cpp"
        elif [[ "$output_file" == *.cuh ]]; then
            output_file="${output_file%.cuh}.hip.hpp"
        fi
        
        # Create directory if it doesn't exist
        mkdir -p "$(dirname "$output_file")"
        
        # Hipify the file
        print_step "Hipifying file: $rel_path"
        hipify-perl "$file" > "$output_file"
        
        if [ $? -eq 0 ]; then
            success_count=$((success_count + 1))
        else
            failure_count=$((failure_count + 1))
            print_error "Failed to hipify file: $rel_path"
        fi
    done
    
    print_section "Hipification summary"
    print_success "Successfully hipified files: $success_count"
    if [ $failure_count -gt 0 ]; then
        print_error "Failed to hipify files: $failure_count"
    fi
    
    return 0
}

# Function to apply common post-hipify fixes
apply_post_hipify_fixes() {
    local directory=$1
    
    print_section "Applying post-hipify fixes to directory: $directory"
    
    # Find all hipified files
    local files=$(find "$directory" -type f -name "*.hip.cpp" -o -name "*.hip.hpp" -o -name "*.cpp" -o -name "*.hpp" -o -name "*.h" -o -name "*.cc")
    
    for file in $files; do
        print_step "Applying fixes to file: $file"
        
        # Fix common issues
        sed -i 's/cudaSuccess/hipSuccess/g' "$file"
        sed -i 's/cudaError/hipError/g' "$file"
        sed -i 's/cudaEvent/hipEvent/g' "$file"
        sed -i 's/cudaStream/hipStream/g' "$file"
        sed -i 's/cudaMemcpy/hipMemcpy/g' "$file"
        sed -i 's/cudaMemcpyHostToDevice/hipMemcpyHostToDevice/g' "$file"
        sed -i 's/cudaMemcpyDeviceToHost/hipMemcpyDeviceToHost/g' "$file"
        sed -i 's/cudaMemcpyDeviceToDevice/hipMemcpyDeviceToDevice/g' "$file"
        sed -i 's/cudaMemset/hipMemset/g' "$file"
        sed -i 's/cudaMalloc/hipMalloc/g' "$file"
        sed -i 's/cudaFree/hipFree/g' "$file"
        sed -i 's/cudaGetErrorString/hipGetErrorString/g' "$file"
        sed -i 's/cudaGetLastError/hipGetLastError/g' "$file"
        sed -i 's/cudaDeviceSynchronize/hipDeviceSynchronize/g' "$file"
        sed -i 's/cudaSetDevice/hipSetDevice/g' "$file"
        sed -i 's/cudaGetDevice/hipGetDevice/g' "$file"
        sed -i 's/cudaGetDeviceCount/hipGetDeviceCount/g' "$file"
        sed -i 's/cudaGetDeviceProperties/hipGetDeviceProperties/g' "$file"
        sed -i 's/cudaDeviceProp/hipDeviceProp_t/g' "$file"
        sed -i 's/cudaLaunchKernel/hipLaunchKernel/g' "$file"
        
        # Fix includes
        sed -i 's/#include <cuda\.h>/#include <hip\/hip_runtime.h>/g' "$file"
        sed -i 's/#include <cuda_runtime\.h>/#include <hip\/hip_runtime.h>/g' "$file"
        sed -i 's/#include <cuda_runtime_api\.h>/#include <hip\/hip_runtime_api.h>/g' "$file"
        sed -i 's/#include <device_launch_parameters\.h>/#include <hip\/hip_runtime.h>/g' "$file"
        sed -i 's/#include <device_functions\.h>/#include <hip\/hip_runtime.h>/g' "$file"
    done
    
    print_success "Post-hipify fixes applied successfully"
    return 0
}

# Main function to hipify a project
hipify_project() {
    local input_dir=$1
    local output_dir=$2
    
    print_header "Hipifying project: $input_dir -> $output_dir"
    
    # Check hipify tools
    check_hipify_tools
    if [ $? -ne 0 ]; then
        print_error "Hipify tools check failed"
        return 1
    fi
    
    # Hipify directory
    hipify_directory "$input_dir" "$output_dir"
    if [ $? -ne 0 ]; then
        print_error "Directory hipification failed"
        return 1
    fi
    
    # Apply post-hipify fixes
    apply_post_hipify_fixes "$output_dir"
    if [ $? -ne 0 ]; then
        print_error "Post-hipify fixes failed"
        return 1
    fi
    
    print_success "Project hipified successfully"
    return 0
}

# If script is run directly, show usage
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    print_header "HIPIFY Utilities for AMD GPUs"
    echo "This script provides utilities for converting CUDA code to HIP for AMD GPUs."
    echo
    echo "Usage:"
    echo "  source $(basename "${BASH_SOURCE[0]}") # To load functions"
    echo "  hipify_project <input_dir> <output_dir> # To hipify a project"
    echo "  hipify_file <input_file> <output_file> # To hipify a single file"
    echo "  hipify_directory <input_dir> <output_dir> # To hipify a directory"
    echo "  apply_post_hipify_fixes <directory> # To apply post-hipify fixes"
    echo
fi

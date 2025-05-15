#!/bin/bash
# Filter script to suppress common ROCm warnings
# This script is used to filter out common ROCm warnings that are not actual errors

# Usage: ./filter_rocm_warnings.sh [command to run]
# Example: ./filter_rocm_warnings.sh ./enhanced_verify_installation.sh

# Check if a command was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 [command to run]"
    echo "Example: $0 ./enhanced_verify_installation.sh"
    exit 1
fi

# Run the command and filter out common ROCm warnings
"$@" 2>&1 | grep -v -E '(hip_code_object\.cpp.*amd::Comgr::get_data\(\) return 0 size|hip_fatbin\.cpp.*Cannot find CO in the bundle|hip_platform\.cpp.*init: Returned hipErrorNoBinaryForGpu|hip_device_runtime\.cpp.*hipGetDevice|All Unique FDs are closed)'

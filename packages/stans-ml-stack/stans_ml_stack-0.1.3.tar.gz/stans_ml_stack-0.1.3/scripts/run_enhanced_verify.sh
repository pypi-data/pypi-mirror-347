#!/bin/bash
# Wrapper script for enhanced_verify_installation.sh
# This script runs the enhanced verification script with filtered output

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILTER_SCRIPT="$SCRIPT_DIR/filter_rocm_warnings.sh"
VERIFY_SCRIPT="$SCRIPT_DIR/enhanced_verify_installation.sh"

# Check if the filter script exists
if [ ! -f "$FILTER_SCRIPT" ]; then
    echo "Error: Filter script not found at $FILTER_SCRIPT"
    exit 1
fi

# Check if the verification script exists
if [ ! -f "$VERIFY_SCRIPT" ]; then
    echo "Error: Verification script not found at $VERIFY_SCRIPT"
    exit 1
fi

# Make sure both scripts are executable
chmod +x "$FILTER_SCRIPT"
chmod +x "$VERIFY_SCRIPT"

# Run the verification script with filtered output
echo "Running enhanced verification with filtered output..."
"$FILTER_SCRIPT" "$VERIFY_SCRIPT" "$@"

# Check the exit code
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Verification failed with exit code $exit_code"
    exit $exit_code
fi

echo "Verification completed successfully"
exit 0

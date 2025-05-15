#!/bin/bash
# Wrapper script for repair_ml_stack.sh with progress updates
echo "Starting Repair ML Stack..."

# Set environment variables to use uv for Python package installation
export USE_UV=1
export PATH="$HOME/.cargo/bin:$PATH"
export NONINTERACTIVE=1
# Suppress HIP logs
export AMD_LOG_LEVEL=0
export HIP_VISIBLE_DEVICES=0,1,2
export ROCR_VISIBLE_DEVICES=0,1,2
# Set DEBIAN_FRONTEND to noninteractive to avoid sudo prompts
export DEBIAN_FRONTEND=noninteractive

# Create a sudo wrapper function that uses the cached password
sudo_with_pass() {
    echo '32465' | sudo -S "$@"
}

# Export the sudo wrapper function
export -f sudo_with_pass

# Replace sudo with our wrapper in the script
sed -i 's/\bsudo\b/sudo_with_pass/g' /home/stan/Prod/Stan-s-ML-Stack/scripts/repair_ml_stack.sh

# Create a progress bar function
progress_bar() {
    local duration=$1
    local elapsed=0
    local progress=0
    local width=50
    local bar=""

    while [ $elapsed -lt $duration ]; do
        # Calculate progress percentage
        progress=$((elapsed * 100 / duration))
        filled=$((progress * width / 100))
        empty=$((width - filled))

        # Create the progress bar
        bar="["
        for ((i=0; i<filled; i++)); do
            bar+="█"
        done
        for ((i=0; i<empty; i++)); do
            bar+=" "
        done
        bar+="] $progress%"

        # Print the progress bar
        echo -ne "\r$bar"

        # Sleep for a bit
        sleep 1
        elapsed=$((elapsed + 1))
    done
    echo ""
}

# Run the actual script with NONINTERACTIVE mode to avoid prompts
# Use stdbuf to ensure unbuffered output
stdbuf -oL -eL /home/stan/Prod/Stan-s-ML-Stack/scripts/repair_ml_stack.sh 2>&1 | while IFS= read -r line; do
    echo "$line"
    # Flush stdout to ensure real-time output
    sleep 0.01
done

# Capture the exit code
exit_code=${PIPESTATUS[0]}

# Restore the original script (remove our sudo wrapper)
sed -i 's/\bsudo_with_pass\b/sudo/g' /home/stan/Prod/Stan-s-ML-Stack/scripts/repair_ml_stack.sh

echo "Script completed with exit code: $exit_code"
exit $exit_code

#!/usr/bin/env python3
"""
ML Stack Installation Bridge Script

This script serves as a bridge between the Rust-based UI and the Python backend.
It handles communication between the two components and executes the installation scripts.

Author: Stanley Chisango (Scooter Lacroix)
Email: scooterlacroix@gmail.com
GitHub: https://github.com/scooter-lacroix
X: https://x.com/scooter_lacroix
Patreon: https://patreon.com/ScooterLacroix
"""

import os
import sys
import json
import time
import subprocess
import platform
import shlex
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple, Callable
import tempfile

# Constants
HOME_DIR = os.path.expanduser("~")
MLSTACK_DIR = os.path.join(HOME_DIR, "Prod", "Stan-s-ML-Stack")
SCRIPTS_DIR = os.path.join(MLSTACK_DIR, "scripts")
LOGS_DIR = os.path.join(MLSTACK_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, f"ml_stack_install_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Global variable to store sudo password
SUDO_PASSWORD = None

# Components to install
CORE_COMPONENTS = [
    {
        "name": "ML Stack Core",
        "description": "Core ML Stack components",
        "script": "install_ml_stack.sh",
        "required": True,
        "status": "pending"
    },
    {
        "name": "Flash Attention",
        "description": "Efficient attention computation",
        "script": "install_flash_attention_ck.sh",
        "required": True,
        "status": "pending"
    }
]

EXTENSION_COMPONENTS = [
    {
        "name": "Triton",
        "description": "Compiler for parallel programming",
        "script": "install_triton.sh",
        "required": False,
        "status": "pending"
    },
    {
        "name": "BITSANDBYTES",
        "description": "Efficient quantization for deep learning models",
        "script": "install_bitsandbytes.sh",
        "required": False,
        "status": "pending"
    },
    {
        "name": "vLLM",
        "description": "High-throughput inference engine for LLMs",
        "script": "install_vllm.sh",
        "required": False,
        "status": "pending"
    },
    {
        "name": "ROCm SMI",
        "description": "System monitoring and management for AMD GPUs",
        "script": "install_rocm_smi.sh",
        "required": False,
        "status": "pending"
    },
    {
        "name": "PyTorch Profiler",
        "description": "Performance analysis for PyTorch models",
        "script": "install_pytorch_profiler.sh",
        "required": False,
        "status": "pending"
    },
    {
        "name": "Weights & Biases",
        "description": "Experiment tracking and visualization",
        "script": "install_wandb.sh",
        "required": False,
        "status": "pending"
    }
]

def log_message(message: str, level: str = "INFO") -> None:
    """Log a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"

    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

    print(log_line)

def run_command(command: str, cwd: Optional[str] = None, timeout: Optional[int] = 300, use_sudo: bool = False) -> Tuple[int, str, str]:
    """Run a shell command and return the return code, stdout, and stderr with a timeout."""
    global SUDO_PASSWORD

    # If the command starts with sudo and we have a sudo password, use it
    if command.strip().startswith("sudo") and SUDO_PASSWORD:
        log_message(f"Running sudo command with cached credentials: {command}")
        # Modify the command to use the stored sudo password
        command = f"echo {shlex.quote(SUDO_PASSWORD)} | sudo -S {command[5:]}"
    elif use_sudo and SUDO_PASSWORD:
        log_message(f"Running command with sudo: {command}")
        # Add sudo with password to the command
        command = f"echo {shlex.quote(SUDO_PASSWORD)} | sudo -S {command}"
    else:
        log_message(f"Running command: {command}")

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )

        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return_code = process.returncode
        except subprocess.TimeoutExpired:
            process.kill()
            log_message(f"Command timed out after {timeout} seconds: {command}", "WARNING")
            return 1, "", f"Command timed out after {timeout} seconds"

        if return_code != 0:
            log_message(f"Command failed with return code {return_code}", "ERROR")
            log_message(f"stderr: {stderr}", "ERROR")

        return return_code, stdout, stderr
    except Exception as e:
        log_message(f"Error executing command: {str(e)}", "ERROR")
        return 1, "", f"Error: {str(e)}"

def detect_hardware() -> Dict[str, Any]:
    """Detect hardware information."""
    log_message("Detecting hardware...")

    hardware_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "amd_gpus": [],
        "rocm_version": None,
        "rocm_path": None
    }

    # Check if ROCm is installed
    return_code, stdout, stderr = run_command("which rocminfo", timeout=5)
    if return_code == 0 and stdout.strip():
        log_message("ROCm is installed")
        hardware_info["rocm_path"] = os.path.dirname(os.path.dirname(stdout.strip()))

        # Try to get ROCm version
        return_code, stdout, stderr = run_command("ls -d /opt/rocm-* 2>/dev/null | grep -o '[0-9]\\+\\.[0-9]\\+\\.[0-9]\\+' | head -n 1", timeout=5)
        if return_code == 0 and stdout.strip():
            hardware_info["rocm_version"] = stdout.strip()
            log_message(f"ROCm version: {hardware_info['rocm_version']}")
    else:
        log_message("ROCm is not installed or not in PATH")

    # Detect AMD GPUs using lspci
    log_message("Detecting AMD GPUs...")
    return_code, stdout, stderr = run_command("lspci | grep -i 'amd\\|radeon\\|advanced micro devices' | grep -i 'vga\\|3d\\|display'", timeout=5)
    if return_code == 0 and stdout.strip():
        hardware_info["amd_gpus"] = [line.strip() for line in stdout.strip().split("\n")]
        log_message(f"Found {len(hardware_info['amd_gpus'])} AMD GPU(s)")
    else:
        log_message("No AMD GPUs detected using lspci or command failed")

    log_message("Hardware detection completed")
    return hardware_info

def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed."""
    log_message("Checking dependencies...")

    dependencies = {
        "build-essential": False,
        "cmake": False,
        "git": False,
        "python3-dev": False,
        "python3-pip": False,
        "libnuma-dev": False,
        "pciutils": False,
        "mesa-utils": False,
        "clinfo": False
    }

    for dep in dependencies:
        log_message(f"Checking dependency: {dep}")
        return_code, stdout, stderr = run_command(f"dpkg -l | grep -q 'ii  {dep} '", timeout=5)
        dependencies[dep] = return_code == 0
        log_message(f"Dependency {dep}: {'Installed' if dependencies[dep] else 'Not installed'}")

    log_message("Dependency check completed")
    return dependencies

def install_dependencies(missing_deps: List[str]) -> bool:
    """Install missing dependencies."""
    if not missing_deps:
        log_message("No missing dependencies to install")
        return True

    log_message(f"Installing missing dependencies: {', '.join(missing_deps)}")

    # Update package lists
    log_message("Running apt-get update")
    update_cmd = "sudo apt-get update"
    update_return_code, _, update_stderr = run_command(update_cmd, timeout=60)
    if update_return_code != 0:
        log_message(f"Failed to update package lists: {update_stderr}", "ERROR")
        return False

    # Install each dependency separately
    for dep in missing_deps:
        log_message(f"Installing {dep}")
        install_cmd = f"sudo apt-get install -y {dep}"
        install_return_code, _, install_stderr = run_command(install_cmd, timeout=60)
        if install_return_code != 0:
            log_message(f"Failed to install {dep}: {install_stderr}", "ERROR")
            continue

        # Verify installation
        log_message(f"Verifying installation of {dep}")
        verify_cmd = f"dpkg-query -W -f='${{Status}}' {dep} 2>/dev/null | grep -q 'install ok installed'"
        verify_return_code, _, _ = run_command(verify_cmd, timeout=5)
        if verify_return_code != 0:
            log_message(f"Failed to verify installation of {dep}", "ERROR")
            continue

        log_message(f"Successfully installed {dep}")

    # Final verification
    log_message("Verifying all dependencies")
    all_installed = True
    for dep in missing_deps:
        verify_cmd = f"dpkg-query -W -f='${{Status}}' {dep} 2>/dev/null | grep -q 'install ok installed'"
        return_code, _, _ = run_command(verify_cmd, timeout=5)
        if return_code != 0:
            log_message(f"Dependency {dep} is still missing", "ERROR")
            all_installed = False

    if all_installed:
        log_message("All dependencies installed successfully")
        return True
    else:
        log_message("Some dependencies failed to install", "WARNING")
        return False

def install_component(component: Dict[str, Any]) -> bool:
    """Install a component."""
    name = component["name"]
    script = component["script"]
    script_path = os.path.join(SCRIPTS_DIR, script)

    if not os.path.exists(script_path):
        log_message(f"Installation script not found for {name}: {script_path}", "ERROR")
        return False

    # Make the script executable
    os.chmod(script_path, 0o755)

    # Update component status
    component["status"] = "installing"
    log_message(f"Installing {name}...")

    # Create a modified script that provides progress updates
    temp_script_path = os.path.join(SCRIPTS_DIR, f"temp_{script}")
    with open(temp_script_path, "w") as f:
        f.write(f"""#!/bin/bash
# Wrapper script for {script} with progress updates
echo "Starting installation of {name}..."

# Run the actual installation script and capture output in real-time
{script_path} 2>&1 | while IFS= read -r line; do
    echo "$line"
    # Flush stdout to ensure real-time output
    sleep 0.1
done

# Capture the exit code
exit_code=${{PIPESTATUS[0]}}
echo "Installation script completed with exit code: $exit_code"
exit $exit_code
""")

    # Make the script executable
    os.chmod(temp_script_path, 0o755)

    # Run the modified script with a longer timeout
    process = subprocess.Popen(
        f"bash {temp_script_path}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1  # Line buffered
    )

    # Read output in real-time
    output_lines = []
    for line in iter(process.stdout.readline, ''):
        output_lines.append(line)
        log_message(f"[{name}] {line.strip()}")

    # Wait for the process to complete
    process.stdout.close()
    return_code = process.wait()

    # Clean up the temporary script
    try:
        os.remove(temp_script_path)
    except Exception as e:
        log_message(f"Error removing temporary script: {str(e)}", "WARNING")

    # Process the output
    stdout = "".join(output_lines)

    if return_code != 0:
        log_message(f"Installation of {name} failed with exit code {return_code}", "ERROR")
        component["status"] = "failed"
        return False

    # Update component status
    component["status"] = "installed"
    log_message(f"Installation of {name} completed successfully", "SUCCESS")
    return True

def create_ipc_file():
    """Create a temporary file for IPC between Python and Rust."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    log_message(f"Created IPC file at {temp_file.name}")
    return temp_file.name

def update_ipc_file(ipc_file: str, data: Dict[str, Any]):
    """Update the IPC file with new data."""
    with open(ipc_file, 'w') as f:
        json.dump(data, f)

def read_ipc_file(ipc_file: str) -> Dict[str, Any]:
    """Read data from the IPC file."""
    try:
        with open(ipc_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def main():
    """Main function."""
    log_message("Starting ML Stack Installation Bridge")

    # Create IPC file
    ipc_file = create_ipc_file()

    # Initialize data
    data = {
        "hardware": detect_hardware(),
        "dependencies": check_dependencies(),
        "core_components": CORE_COMPONENTS,
        "extension_components": EXTENSION_COMPONENTS,
        "logs": [],
        "command": None,
        "response": None
    }

    # Update IPC file
    update_ipc_file(ipc_file, data)

    # Start the Rust UI
    ui_process = subprocess.Popen(
        f"cd {MLSTACK_DIR}/ml_stack_ui && cargo run -- --ipc-file {ipc_file}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1  # Line buffered
    )

    # Main loop
    try:
        while ui_process.poll() is None:
            # Read IPC file
            ipc_data = read_ipc_file(ipc_file)

            # Check for commands
            command = ipc_data.get("command")
            if command:
                log_message(f"Received command: {command}")

                # Process command
                if command == "install_dependencies":
                    # Get missing dependencies
                    deps = ipc_data.get("dependencies", {})
                    missing_deps = [dep for dep, installed in deps.items() if not installed]

                    # Install missing dependencies
                    success = install_dependencies(missing_deps)

                    # Update dependencies
                    data["dependencies"] = check_dependencies()
                    data["response"] = {"command": command, "success": success}

                elif command == "install_component":
                    # Get component to install
                    component_name = ipc_data.get("component_name")
                    component = None

                    # Find component
                    for comp in data["core_components"]:
                        if comp["name"] == component_name:
                            component = comp
                            break

                    if not component:
                        for comp in data["extension_components"]:
                            if comp["name"] == component_name:
                                component = comp
                                break

                    if component:
                        # Install component
                        success = install_component(component)
                        data["response"] = {"command": command, "success": success}
                    else:
                        log_message(f"Component not found: {component_name}", "ERROR")
                        data["response"] = {"command": command, "success": False}

                # Clear command
                data["command"] = None

                # Update IPC file
                update_ipc_file(ipc_file, data)

            # Sleep to avoid high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        log_message("Interrupted by user")

    finally:
        # Clean up
        if ui_process.poll() is None:
            ui_process.terminate()

        try:
            os.remove(ipc_file)
            log_message(f"Removed IPC file: {ipc_file}")
        except Exception as e:
            log_message(f"Error removing IPC file: {str(e)}", "ERROR")

        log_message("ML Stack Installation Bridge stopped")

if __name__ == "__main__":
    main()

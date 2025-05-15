#!/usr/bin/env python3
"""
Test script for the ML Stack component detector.
"""

import os
import sys
import json
import subprocess
from typing import Dict, Any

def run_command(command: str, timeout: int = 60) -> tuple:
    """Run a shell command and return the output."""
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode
        return return_code, stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)

def check_ml_stack_components() -> Dict[str, bool]:
    """Check which ML Stack components are installed using the component detector script."""
    components = {
        "pytorch": False,
        "onnxruntime": False,
        "migraphx": False,
        "flash_attention": False,
        "rccl": False,
        "mpi": False,
        "megatron": False,
        "triton": False,
        "bitsandbytes": False,
        "vllm": False,
        "rocm_smi": False,
        "pytorch_profiler": False,
        "wandb": False,
        "rocm": False
    }
    
    # Create a temporary script to capture the output of the component detector
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_script = os.path.join(script_dir, "temp_component_check.sh")
    with open(temp_script, "w") as f:
        f.write("""#!/bin/bash
# Source the component detector library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DETECTOR_SCRIPT="$PARENT_DIR/../scripts/ml_stack_component_detector.sh"

if [ -f "$DETECTOR_SCRIPT" ]; then
    source "$DETECTOR_SCRIPT"
else
    echo "Error: Component detector script not found at $DETECTOR_SCRIPT"
    exit 1
fi

# Check components
check_rocm > /dev/null
rocm_installed=$?

check_pytorch > /dev/null
pytorch_installed=$?

check_onnxruntime > /dev/null
onnxruntime_installed=$?

check_migraphx > /dev/null
migraphx_installed=$?

check_flash_attention > /dev/null
flash_attention_installed=$?

check_rccl > /dev/null
rccl_installed=$?

check_mpi > /dev/null
mpi_installed=$?

check_megatron > /dev/null
megatron_installed=$?

check_triton > /dev/null
triton_installed=$?

check_bitsandbytes > /dev/null
bitsandbytes_installed=$?

check_vllm > /dev/null
vllm_installed=$?

check_rocm_smi > /dev/null
rocm_smi_installed=$?

check_pytorch_profiler > /dev/null
pytorch_profiler_installed=$?

check_wandb > /dev/null
wandb_installed=$?

# Output component status in JSON format
echo "{"
echo "  \\"rocm\\": $([ $rocm_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"pytorch\\": $([ $pytorch_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"onnxruntime\\": $([ $onnxruntime_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"migraphx\\": $([ $migraphx_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"flash_attention\\": $([ $flash_attention_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"rccl\\": $([ $rccl_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"mpi\\": $([ $mpi_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"megatron\\": $([ $megatron_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"triton\\": $([ $triton_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"bitsandbytes\\": $([ $bitsandbytes_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"vllm\\": $([ $vllm_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"rocm_smi\\": $([ $rocm_smi_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"pytorch_profiler\\": $([ $pytorch_profiler_installed -eq 0 ] && echo "true" || echo "false"),"
echo "  \\"wandb\\": $([ $wandb_installed -eq 0 ] && echo "true" || echo "false")"
echo "}"
""")
    
    # Make the script executable
    os.chmod(temp_script, 0o755)
    
    # Run the script
    print("Running component detection script...")
    return_code, stdout, stderr = run_command(f"bash {temp_script}", timeout=30)
    
    # Clean up
    os.remove(temp_script)
    
    if return_code == 0 and stdout.strip():
        try:
            # Parse the JSON output
            component_data = json.loads(stdout.strip())
            
            # Update components with the detected values
            for key in components:
                if key in component_data:
                    components[key] = component_data[key]
            
            print(f"Component detection completed: {json.dumps(components, indent=2)}")
        except Exception as e:
            print(f"Error parsing component detection output: {str(e)}")
            print("Falling back to original component detection method...")
            return check_ml_stack_components_original()
    else:
        print(f"Component detection script failed: {stderr}")
        print("Falling back to original component detection method...")
        return check_ml_stack_components_original()
    
    return components

def check_ml_stack_components_original() -> Dict[str, bool]:
    """Original method to check which ML Stack components are installed."""
    components = {
        "pytorch": False,
        "onnxruntime": False,
        "migraphx": False,
        "flash_attention": False,
        "rccl": False,
        "mpi": False,
        "megatron": False,
        "triton": False,
        "bitsandbytes": False,
        "vllm": False,
        "rocm_smi": False,
        "pytorch_profiler": False,
        "wandb": False,
        "rocm": False
    }
    
    # Check ROCm
    try:
        return_code, stdout, stderr = run_command("which rocminfo", timeout=5)
        if return_code == 0:
            components["rocm"] = True
    except Exception:
        pass
    
    # Check PyTorch
    try:
        import torch
        components["pytorch"] = True
        
        # Check PyTorch Profiler
        try:
            from torch.profiler import profile
            components["pytorch_profiler"] = True
        except ImportError:
            pass
    except ImportError:
        pass
    
    # Check ONNX Runtime
    try:
        import onnxruntime
        components["onnxruntime"] = True
    except ImportError:
        pass
    
    # Check MIGraphX
    try:
        import migraphx
        components["migraphx"] = True
    except ImportError:
        pass
    
    # Check Flash Attention
    try:
        import flash_attention_amd
        components["flash_attention"] = True
    except ImportError:
        try:
            import flash_attn
            components["flash_attention"] = True
        except ImportError:
            pass
    
    # Check RCCL
    if os.path.exists("/opt/rocm/lib/librccl.so"):
        components["rccl"] = True
    
    # Check MPI
    try:
        return_code, stdout, stderr = run_command("which mpirun", timeout=5)
        if return_code == 0 and stdout.strip():
            components["mpi"] = True
    except Exception:
        pass
    
    # Check Megatron-LM
    try:
        import megatron
        components["megatron"] = True
    except ImportError:
        pass
    
    # Check Triton
    try:
        import triton
        components["triton"] = True
    except ImportError:
        pass
    
    # Check BITSANDBYTES
    try:
        import bitsandbytes
        components["bitsandbytes"] = True
    except ImportError:
        pass
    
    # Check vLLM
    try:
        import vllm
        components["vllm"] = True
    except ImportError:
        pass
    
    # Check ROCm SMI
    try:
        from rocm_smi_lib import rsmi
        components["rocm_smi"] = True
    except ImportError:
        pass
    
    # Check Weights & Biases
    try:
        import wandb
        components["wandb"] = True
    except ImportError:
        pass
    
    return components

def detect_hardware() -> Dict[str, Any]:
    """Detect hardware information using the component detector script."""
    hardware_info = {
        "rocm_version": None,
        "rocm_path": None,
        "amd_gpus": [],
        "gpu_count": 0
    }
    
    # Create a temporary script to capture the output of the component detector
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_script = os.path.join(script_dir, "temp_hardware_detect.sh")
    with open(temp_script, "w") as f:
        f.write("""#!/bin/bash
# Source the component detector library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
DETECTOR_SCRIPT="$PARENT_DIR/../scripts/ml_stack_component_detector.sh"

if [ -f "$DETECTOR_SCRIPT" ]; then
    source "$DETECTOR_SCRIPT"
else
    echo "Error: Component detector script not found at $DETECTOR_SCRIPT"
    exit 1
fi

# Detect hardware
detect_rocm
detect_amd_gpus

# Output hardware info in JSON format
echo "{"
echo "  \\"rocm_version\\": \\"$ROCM_VERSION\\","
echo "  \\"rocm_path\\": \\"$ROCM_PATH\\","
echo "  \\"gpu_count\\": $GPU_COUNT,"
echo "  \\"amd_gpus\\": ["

# Get GPU names from rocminfo
if command_exists rocminfo; then
    gpu_names=$(rocminfo | grep -A 10 "Device Type:.*GPU" | grep "Marketing Name" | awk -F: '{print $2}' | sed 's/^[ \\t]*//')
    first=true
    while IFS= read -r gpu; do
        if [ "$first" = true ]; then
            echo "    \\"$gpu\\""
            first=false
        else
            echo "    ,\\"$gpu\\""
        fi
    done <<< "$gpu_names"
fi

echo "  ]"
echo "}"
""")
    
    # Make the script executable
    os.chmod(temp_script, 0o755)
    
    # Run the script
    print("Running hardware detection script...")
    return_code, stdout, stderr = run_command(f"bash {temp_script}", timeout=30)
    
    # Clean up
    os.remove(temp_script)
    
    if return_code == 0 and stdout.strip():
        try:
            # Parse the JSON output
            hw_data = json.loads(stdout.strip())
            
            # Update hardware_info with the detected values
            hardware_info["rocm_version"] = hw_data.get("rocm_version")
            hardware_info["rocm_path"] = hw_data.get("rocm_path")
            hardware_info["amd_gpus"] = hw_data.get("amd_gpus", [])
            hardware_info["gpu_count"] = hw_data.get("gpu_count", 0)
            
            print(f"Hardware detection completed: {json.dumps(hardware_info, indent=2)}")
        except Exception as e:
            print(f"Error parsing hardware detection output: {str(e)}")
    else:
        print(f"Hardware detection script failed: {stderr}")
    
    return hardware_info

def main():
    """Main function."""
    print("Testing ML Stack Component Detector")
    print("==================================")
    
    # Detect hardware
    print("\nDetecting hardware...")
    hardware_info = detect_hardware()
    
    # Check components
    print("\nChecking components...")
    components = check_ml_stack_components()
    
    # Print summary
    print("\nSummary:")
    print(f"ROCm Version: {hardware_info['rocm_version']}")
    print(f"ROCm Path: {hardware_info['rocm_path']}")
    print(f"GPU Count: {hardware_info['gpu_count']}")
    print("AMD GPUs:")
    for gpu in hardware_info['amd_gpus']:
        print(f"  - {gpu}")
    
    print("\nInstalled Components:")
    for component, installed in components.items():
        status = "Installed" if installed else "Not installed"
        print(f"  - {component}: {status}")

if __name__ == "__main__":
    main()

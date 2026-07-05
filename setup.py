#!/usr/bin/env python3
"""
Voice Detection UI Setup Script
Install all dependencies and verify installation
"""

import subprocess
import sys
import os
from pathlib import Path

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible"""
    print_section("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        return False
    print("✓ Python version is compatible")
    return True

def install_dependencies():
    """Install all dependencies from requirements.txt"""
    print_section("Installing Dependencies")
    
    requirements_path = Path(__file__).parent / "requirements.txt"
    if not requirements_path.exists():
        print(f"ERROR: requirements.txt not found at {requirements_path}")
        return False
    
    print(f"Installing from {requirements_path}")
    
    try:
        # Install using pip
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("✓ Installation completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Installation failed!")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def verify_installation():
    """Verify all packages are installed correctly"""
    print_section("Verifying Installation")
    
    packages = [
        "gradio",
        "numpy", 
        "scipy",
        "soundfile",
        "pydub",
        "matplotlib",
        "torch",
        "transformers",
        "accelerate",
        "sentencepiece",
        "onnxruntime",
        "huggingface_hub"
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} imported successfully")
        except ImportError as e:
            print(f"✗ {package} failed to import: {e}")
            all_ok = False
    
    return all_ok

def main():
    print("="*60)
    print("  Voice Detection UI - Dependency Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\nERROR: Some packages failed to install correctly")
        sys.exit(1)
    
    print_section("Setup Complete")
    print("✓ All dependencies installed and verified")
    print("\nNext steps:")
    print("  1. Check pip list: python -m pip list")
    print("  2. Create project structure")
    print("  3. Start implementing voice detection UI")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

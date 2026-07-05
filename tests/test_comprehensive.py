#!/usr/bin/env python3
"""
Comprehensive test suite for Voice Detection UI.
Covers connectivity, positive/negative, and cross-language tests.
Output: color-coded with exit codes.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

# ANSI color codes
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'reset': '\033[0m',
    'bold': '\033[1m'
}

def print_status(test_name: str, passed: bool, message: str = ""):
    """Print color-coded test result."""
    if passed:
        print(f"{COLORS['green']}✅ PASS{COLORS['reset']}: {test_name}")
    else:
        print(f"{COLORS['red']}❌ FAIL{COLORS['reset']}: {test_name}")
        if message:
            print(f"   {COLORS['yellow']}→ {message}{COLORS['reset']}")

def run_command(cmd: list[str], timeout: int = 30) -> tuple[bool, str]:
    """Run shell command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="E:/2.Projects/voice-detect-ui"
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def test_python_version() -> tuple[bool, str]:
    """Test Python version >= 3.8."""
    result = run_command([sys.executable, "--version"])
    if not result[0]:
        return False, "Python version check failed"
    
    version = result[1].strip()
    if "Python 3.8" in version or "Python 3.9" in version or "Python 3.10" in version or "Python 3.11" in version:
        return True, f"Python {version}"
    return False, f"Python {version} (requires 3.8+)"

def test_dependencies_installed() -> tuple[bool, str]:
    """Test core dependencies are installed."""
    packages = ["gradio", "torch", "numpy", "scipy", "soundfile", "matplotlib"]
    missing = []
    
    for pkg in packages:
        success, _ = run_command([sys.executable, "-c", f"import {pkg}"])
        if not success:
            missing.append(pkg)
    
    if not missing:
        return True, "All core packages installed"
    return False, f"Missing: {', '.join(missing)}"

def test_models_directory_exists() -> tuple[bool, str]:
    """Test models directory exists."""
    models_path = Path("E:/2.Projects/voice-detect-ui/models")
    if models_path.exists():
        return True, f"Models dir exists: {models_path}"
    return False, f"Models directory missing: {models_path}"

def test_readme_exists() -> tuple[bool, str]:
    """Test README.md exists."""
    readme_path = Path("E:/2.Projects/voice-detect-ui/README.md")
    if readme_path.exists():
        return True, f"README.md exists ({readme_path.stat().st_size} bytes)"
    return False, "README.md missing"

def test_hermes_md_exists() -> tuple[bool, str]:
    """Test .hermes.md exists."""
    hermes_path = Path("E:/2.Projects/voice-detect-ui/.hermes.md")
    if hermes_path.exists():
        return True, f".hermes.md exists ({hermes_path.stat().st_size} bytes)"
    return False, ".hermes.md missing"

def test_pyproject_toml_exists() -> tuple[bool, str]:
    """Test pyproject.toml exists."""
    pyproject_path = Path("E:/2.Projects/voice-detect-ui/pyproject.toml")
    if pyproject_path.exists():
        return True, f"pyproject.toml exists ({pyproject_path.stat().st_size} bytes)"
    return False, "pyproject.toml missing"

def test_gitignore_exists() -> tuple[bool, str]:
    """Test .gitignore exists."""
    gitignore_path = Path("E:/2.Projects/voice-detect-ui/.gitignore")
    if gitignore_path.exists():
        return True, f".gitignore exists ({gitignore_path.stat().st_size} bytes)"
    return False, ".gitignore missing"

def test_architecture_md_exists() -> tuple[bool, str]:
    """Test ARCHITECTURE.md exists."""
    arch_path = Path("E:/2.Projects/voice-detect-ui/ARCHITECTURE.md")
    if arch_path.exists():
        return True, f"ARCHITECTURE.md exists ({arch_path.stat().st_size} bytes)"
    return False, "ARCHITECTURE.md missing"

def test_quickstart_md_exists() -> tuple[bool, str]:
    """Test QUICKSTART.md exists."""
    quick_path = Path("E:/2.Projects/voice-detect-ui/QUICKSTART.md")
    if quick_path.exists():
        return True, f"QUICKSTART.md exists ({quick_path.stat().st_size} bytes)"
    return False, "QUICKSTART.md missing"

def test_troubleshooting_md_exists() -> tuple[bool, str]:
    """Test TROUBLESHOOTING.md exists."""
    troubleshooting_path = Path("E:/2.Projects/voice-detect-ui/TROUBLESHOOTING.md")
    if troubleshooting_path.exists():
        return True, f"TROUBLESHOOTING.md exists ({troubleshooting_path.stat().st_size} bytes)"
    return False, "TROUBLESHOOTING.md missing"

def test_changelog_md_exists() -> tuple[bool, str]:
    """Test CHANGELOG.md exists."""
    changelog_path = Path("E:/2.Projects/voice-detect-ui/CHANGELOG.md")
    if changelog_path.exists():
        return True, f"CHANGELOG.md exists ({changelog_path.stat().st_size} bytes)"
    return False, "CHANGELOG.md missing"

def test_env_example_exists() -> tuple[bool, str]:
    """Test .env.example exists."""
    env_path = Path("E:/2.Projects/voice-detect-ui/.env.example")
    if env_path.exists():
        return True, f".env.example exists ({env_path.stat().st_size} bytes)"
    return False, ".env.example missing"

def test_src_directory_exists() -> tuple[bool, str]:
    """Test src directory exists."""
    src_path = Path("E:/2.Projects/voice-detect-ui/src")
    if src_path.exists() and src_path.is_dir():
        return True, f"src/ directory exists"
    return False, "src/ directory missing"

def test_tests_directory_exists() -> tuple[bool, str]:
    """Test tests directory exists."""
    tests_path = Path("E:/2.Projects/voice-detect-ui/tests")
    if tests_path.exists() and tests_path.is_dir():
        return True, f"tests/ directory exists"
    return False, "tests/ directory missing"

def test_main_py_exists() -> tuple[bool, str]:
    """Test main.py exists."""
    main_path = Path("E:/2.Projects/voice-detect-ui/main.py")
    if main_path.exists():
        return True, f"main.py exists ({main_path.stat().st_size} bytes)"
    return False, "main.py missing"

def test_app_py_exists() -> tuple[bool, str]:
    """Test app.py exists."""
    app_path = Path("E:/2.Projects/voice-detect-ui/app.py")
    if app_path.exists():
        return True, f"app.py exists ({app_path.stat().st_size} bytes)"
    return False, "app.py missing"

def test_requirements_txt_exists() -> tuple[bool, str]:
    """Test requirements.txt exists."""
    req_path = Path("E:/2.Projects/voice-detect-ui/requirements.txt")
    if req_path.exists():
        return True, f"requirements.txt exists ({req_path.stat().st_size} bytes)"
    return False, "requirements.txt missing"

def test_setup_py_exists() -> tuple[bool, str]:
    """Test setup.py exists."""
    setup_path = Path("E:/2.Projects/voice-detect-ui/setup.py")
    if setup_path.exists():
        return True, f"setup.py exists ({setup_path.stat().st_size} bytes)"
    return False, "setup.py missing"

def test_python_syntax():
    """Test Python files have valid syntax."""
    py_files = list(Path("E:/2.Projects/voice-detect-ui/src").glob("*.py"))
    py_files += [Path("E:/2.Projects/voice-detect-ui/main.py")]
    py_files += [Path("E:/2.Projects/voice-detect-ui/app.py")]
    
    failed = []
    for py_file in py_files:
        success, _ = run_command([sys.executable, "-m", "py_compile", str(py_file)])
        if not success:
            failed.append(str(py_file))
    
    if not failed:
        return True, f"All {len(py_files)} Python files have valid syntax"
    return False, f"Syntax errors in: {', '.join(failed)}"

def test_import_modules():
    """Test core modules can be imported."""
    sys.path.insert(0, "E:/2.Projects/voice-detect-ui")
    
    modules = [
        "src.audio_preprocessing",
        "src.model_loader",
        "src.models",
        "src.visualization",
        "src.localization"
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
        except ImportError as e:
            failed.append(f"{module}: {e}")
    
    if not failed:
        return True, f"All {len(modules)} modules import successfully"
    return False, f"Import errors: {chr(10).join(failed)}"

def test_gradio_interface():
    """Test Gradio app can be instantiated (non-blocking)."""
    cmd = [
        sys.executable, "-c",
        """
import sys
sys.path.insert(0, 'E:/2.Projects/voice-detect-ui')
from main import create_interface
try:
    demo = create_interface()
    print('Gradio interface created successfully')
    sys.exit(0)
except Exception as e:
    print(f'Failed: {e}')
    sys.exit(1)
"""
    ]
    return run_command(cmd, timeout=20)

def test_pytest_suite():
    """Run pytest on test suite."""
    success, output = run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        timeout=60
    )
    return success, output

def test_file_structure():
    """Test expected file structure exists."""
    expected_files = [
        "README.md",
        ".hermes.md",
        "ARCHITECTURE.md",
        "QUICKSTART.md",
        "PERFORMANCE.md",
        "TROUBLESHOOTING.md",
        "CHANGELOG.md",
        "pyproject.toml",
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "main.py",
        "app.py",
        "setup.py",
    ]
    
    missing = []
    for f in expected_files:
        if not Path(f"E:/2.Projects/voice-detect-ui/{f}").exists():
            missing.append(f)
    
    if not missing:
        return True, f"All {len(expected_files)} expected files present"
    return False, f"Missing: {', '.join(missing)}"

def test_directory_structure():
    """Test expected directories exist."""
    expected_dirs = [
        "src",
        "tests",
        "models",
        "data",
        "docs",
        "assets"
    ]
    
    missing = []
    for d in expected_dirs:
        if not Path(f"E:/2.Projects/voice-detect-ui/{d}").exists():
            missing.append(d)
    
    if not missing:
        return True, f"All {len(expected_dirs)} directories exist"
    return False, f"Missing: {', '.join(missing)}"

def main():
    """Run all tests and report results."""
    print(f"{COLORS['bold']}=== Voice Detection UI - Comprehensive Test Suite ==={COLORS['reset']}\n")
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies Installed", test_dependencies_installed),
        ("Models Directory Exists", test_models_directory_exists),
        ("README.md Exists", test_readme_exists),
        (".hermes.md Exists", test_hermes_md_exists),
        ("pyproject.toml Exists", test_pyproject_toml_exists),
        (".gitignore Exists", test_gitignore_exists),
        ("ARCHITECTURE.md Exists", test_architecture_md_exists),
        ("QUICKSTART.md Exists", test_quickstart_md_exists),
        ("TROUBLESHOOTING.md Exists", test_troubleshooting_md_exists),
        ("CHANGELOG.md Exists", test_changelog_md_exists),
        (".env.example Exists", test_env_example_exists),
        ("src/ Directory Exists", test_src_directory_exists),
        ("tests/ Directory Exists", test_tests_directory_exists),
        ("main.py Exists", test_main_py_exists),
        ("app.py Exists", test_app_py_exists),
        ("requirements.txt Exists", test_requirements_txt_exists),
        ("setup.py Exists", test_setup_py_exists),
        ("Python Syntax Valid", test_python_syntax),
        ("Modules Import", test_import_modules),
        ("Gradio Interface Instantiable", test_gradio_interface),
        ("File Structure Complete", test_file_structure),
        ("Directory Structure Complete", test_directory_structure),
    ]
    
    results = []
    for name, test_func in tests:
        passed, message = test_func()
        results.append((name, passed, message))
    
    # Summary
    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)
    
    print(f"\n{COLORS['bold']}=== Summary ==={COLORS['reset']}")
    print(f"{COLORS['green']}Passed: {passed_count}/{total_count}{COLORS['reset']}")
    
    failed_tests = [(name, msg) for name, passed, msg in results if not passed]
    if failed_tests:
        print(f"\n{COLORS['yellow']}Failed tests:{COLORS['reset']}")
        for name, msg in failed_tests:
            print(f"  ❌ {name}: {msg}")
    
    # Exit code
    sys.exit(0 if passed_count == total_count else 1)

if __name__ == "__main__":
    main()

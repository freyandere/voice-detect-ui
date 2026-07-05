#!/usr/bin/env python3
"""
Test script for model_loader.py
"""

import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model_loader import load_model, validate_model_path, get_model_path, SUPPORTED_MODELS

def test_supported_models():
    """Test loading supported models"""
    print("=" * 60)
    print("Testing Supported Models")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Using temporary directory: {tmpdir}")
        
        # Test age-gender model
        print("\n1. Testing age-gender model...")
        try:
            model_path = get_model_path("age-gender", tmpdir)
            print(f"✓ Success: {model_path}")
            assert os.path.exists(model_path), "Model file does not exist"
            assert model_path.endswith('.gguf'), "Not a .gguf file"
            print("✓ Validation passed")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False
        
        # Test emotion model
        print("\n2. Testing emotion model...")
        try:
            model_path = get_model_path("emotion", tmpdir)
            print(f"✓ Success: {model_path}")
            assert os.path.exists(model_path), "Model file does not exist"
            assert model_path.endswith('.gguf'), "Not a .gguf file"
            print("✓ Validation passed")
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False
        
        # Test speaker verification models
        print("\n3. Testing speaker verification models...")
        for model_name in ["speaker-verification-1", "speaker-verification-2"]:
            try:
                model_path = get_model_path(model_name, tmpdir)
                print(f"✓ {model_name}: {model_path}")
                assert os.path.exists(model_path), "Model file does not exist"
            except Exception as e:
                print(f"✗ {model_name} failed: {e}")
                return False
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return True

def test_direct_model_name():
    """Test loading with direct model name (not in SUPPORTED_MODELS)"""
    print("\n" + "=" * 60)
    print("Testing Direct Model Name")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            model_path = get_model_path("age-gender-wav2vec2-audeering", tmpdir)
            print(f"✓ Success: {model_path}")
            assert os.path.exists(model_path)
            print("✓ Validation passed")
            return True
        except Exception as e:
            print(f"✗ Failed: {e}")
            return False

if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Model Loader Test Suite" + " " * 27 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    success = True
    
    # Test supported models
    if not test_supported_models():
        success = False
    
    # Test direct model name
    if not test_direct_model_name():
        success = False
    
    if success:
        print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
        sys.exit(0)
    else:
        print("\n✗✗✗ SOME TESTS FAILED ✗✗✗")
        sys.exit(1)

"""
Model Loader for GGUF Voice Detection Models

This module provides functions to download and load GGUF models from HuggingFace.
"""

import os
from huggingface_hub import hf_hub_download, list_repo_files


# Supported voice detection models
SUPPORTED_MODELS = {
    "age-gender": "age-gender-wav2vec2-audeering",
    "emotion": "emotion-wav2vec2-superb-er",
    "speaker-verification-1": "ecapa-tdnn-voxceleb",
    "speaker-verification-2": "wespeaker-resnet34-voxceleb",
    "campplus": "campplus-zh-cn",
    "eres2net": "eres2net-base-zh-cn"
}


def get_model_files(repo_id):
    """Get list of files in a HuggingFace repository."""
    try:
        files = list_repo_files(repo_id)
        return [f for f in files if f.endswith('.gguf') or f in ['config.json', 'tokenizer.json']]
    except Exception as e:
        print(f"Error listing files for {repo_id}: {e}")
        return []


def load_model(model_name, model_dir):
    """
    Load GGUF model from HuggingFace.
    
    Args:
        model_name (str): Name of the model (e.g., "age-gender", "emotion")
        model_dir (str): Directory to store downloaded models
    
    Returns:
        str: Path to the downloaded model directory
    
    Raises:
        ValueError: If model_name is not supported or model files cannot be downloaded
    """
    # All models are in the same repository
    repo_id = "mudler/voice-detect-gguf"
    
    # Map common names to actual model filenames (without .gguf)
    name_to_model = {
        "age_gender": "age-gender-wav2vec2-audeering",
        "emotion": "emotion-wav2vec2-superb-er",
        "speaker_verification": "ecapa-tdnn-voxceleb",
        "speaker_verification_wespeaker": "wespeaker-resnet34-voxceleb"
    }
    
    # Get the actual model filename (without .gguf extension)
    if model_name in name_to_model:
        model_filename = name_to_model[model_name]
    elif model_name in SUPPORTED_MODELS:
        model_filename = SUPPORTED_MODELS[model_name]
    else:
        # Direct filename (without .gguf extension)
        model_filename = model_name

    # Create model directory
    local_dir = os.path.join(model_dir, "voice-detect-gguf")
    os.makedirs(local_dir, exist_ok=True)

    print(f"Downloading {model_filename} from {repo_id}...")

    available_files = get_model_files(repo_id)

    # Always append .gguf extension to model filename
    model_filename = f"{model_filename}.gguf"

    # Check if the model file exists in the repo
    if model_filename not in available_files:
        raise ValueError(f"Model {model_filename} not found in {repo_id}")

    # Download the model file
    try:
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=model_filename,
            local_dir=local_dir
        )
        print(f"✓ Downloaded {model_filename} to {file_path}")
    except Exception as e:
        print(f"✗ Error downloading {model_filename}: {e}")
        raise

    # Also download config.json if available
    if "config.json" in available_files:
        try:
            config_path = hf_hub_download(
                repo_id=repo_id,
                filename="config.json",
                local_dir=local_dir
            )
            print(f"✓ Downloaded config.json to {config_path}")
        except Exception as e:
            print(f"⚠ Warning: Could not download config.json: {e}")

    # Validate model path and get model file
    model_file = validate_model_path(local_dir, model_filename)
    return model_file


def validate_model_path(model_path, expected_model=None):
    """
    Validate that model files exist.
    
    Args:
        model_path (str): Path to the model directory
        expected_model (str): Expected model filename (without .gguf or with .gguf)
    
    Returns:
        str: Path to the model file (.gguf)
    
    Raises:
        ValueError: If required files are missing
    """
    # Get list of .gguf files
    gguf_files = [f for f in os.listdir(model_path) if f.endswith('.gguf')]
    if not gguf_files:
        raise ValueError(f"No .gguf files found in {model_path}")
    
    # If expected_model is provided, look for it specifically
    if expected_model:
        # Determine the expected filename (don't append .gguf if already present)
        if expected_model.endswith('.gguf'):
            expected_filename = expected_model
        else:
            expected_filename = f"{expected_model}.gguf"
        
        for f in gguf_files:
            if f == expected_filename:
                return os.path.join(model_path, f)
        
        # If expected file not found, raise error
        raise ValueError(f"Expected model file '{expected_filename}' not found in {model_path}")
    
    # Fallback: return first .gguf file
    return os.path.join(model_path, gguf_files[0])


def get_model_path(model_name, model_dir):
    """
    Get or download model path.

    Args:
        model_name (str): Name of the model
        model_dir (str): Directory to store models

    Returns:
        str: Path to the model file (.gguf)
    """
    model_dir_path = load_model(model_name, model_dir)
    
    # Get the actual model filename
    if model_name in SUPPORTED_MODELS:
        model_filename = SUPPORTED_MODELS[model_name]
    else:
        model_filename = f"{model_name}.gguf"
    
    # Check if the model file exists in the repo (add .gguf if needed)
    if not model_filename.endswith('.gguf'):
        model_filename_with_ext = f"{model_filename}.gguf"
        if os.path.exists(os.path.join(model_dir_path, model_filename_with_ext)):
            model_filename = model_filename_with_ext
    
    # Look for the specific model file
    model_file = os.path.join(model_dir_path, model_filename)
    if os.path.exists(model_file):
        return model_file
    
    # Fallback: find any .gguf file
    gguf_files = [f for f in os.listdir(model_dir_path) if f.endswith('.gguf')]
    if gguf_files:
        return os.path.join(model_dir_path, gguf_files[0])
    
    raise ValueError(f"Model file not found in {model_dir_path}")


def test_model_loading():
    """Test function to verify model loading works correctly."""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        print("Testing model loading...")
        
        # Test age-gender model
        try:
            model_path = get_model_path("age-gender", tmpdir)
            print(f"✓ Age-gender model loaded: {model_path}")
            assert os.path.exists(model_path)
        except Exception as e:
            print(f"✗ Age-gender model failed: {e}")
            return False
        
        # Test emotion model
        try:
            model_path = get_model_path("emotion", tmpdir)
            print(f"✓ Emotion model loaded: {model_path}")
            assert os.path.exists(model_path)
        except Exception as e:
            print(f"✗ Emotion model failed: {e}")
            return False
        
        print("✓ All model loading tests passed")
        return True


if __name__ == "__main__":
    # Run tests
    test_model_loading()

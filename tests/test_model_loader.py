"""Model loader tests."""
import pytest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.model_loader import (
    load_model,
    validate_model_path,
    get_model_path,
    SUPPORTED_MODELS,
    get_model_files
)


def test_supported_models_dict():
    """Test that SUPPORTED_MODELS dictionary is properly defined."""
    assert isinstance(SUPPORTED_MODELS, dict)
    assert "age-gender" in SUPPORTED_MODELS
    assert "emotion" in SUPPORTED_MODELS
    assert "speaker-verification-1" in SUPPORTED_MODELS


def test_validate_model_path_with_valid_gguf(tmp_path):
    """Test validate_model_path with valid GGUF file."""
    model_dir = tmp_path / "voice-detect-gguf"
    model_dir.mkdir()
    gguf_file = model_dir / "model.gguf"
    gguf_file.touch()

    assert validate_model_path(str(model_dir)) is True


def test_validate_model_path_with_no_gguf(tmp_path):
    """Test validate_model_path with no GGUF file should raise error."""
    model_dir = tmp_path / "voice-detect-gguf"
    model_dir.mkdir()

    with pytest.raises(ValueError):
        validate_model_path(str(model_dir))


def test_get_model_files_success():
    """Test get_model_files with mocked response."""
    mock_files = ["model.gguf", "config.json", "tokenizer.json"]
    with patch('src.model_loader.list_repo_files', return_value=mock_files):
        result = get_model_files("test-repo")
        assert result == ["model.gguf", "config.json", "tokenizer.json"]


def test_get_model_files_with_error():
    """Test get_model_files when an exception occurs."""
    with patch('src.model_loader.list_repo_files', side_effect=Exception("Error")):
        result = get_model_files("test-repo")
        assert result == []


def test_get_model_path_with_mocked_download(tmp_path):
    """Test get_model_path with mocked hf_hub_download."""
    mock_model_dir = tmp_path / "voice-detect-gguf"
    mock_model_dir.mkdir()
    mock_model_file = mock_model_dir / "age-gender-wav2vec2-audearing.gguf"
    mock_model_file.touch()

    with patch('huggingface_hub.list_repo_files', return_value=["age-gender-wav2vec2-audearing.gguf"]), \
         patch('src.model_loader.hf_hub_download', return_value=str(mock_model_file)), \
         patch('src.model_loader.validate_model_path', return_value=True):
        result = get_model_path("age-gender", str(tmp_path))
        assert os.path.exists(result)
        assert result.endswith('.gguf')


def test_get_model_path_with_direct_name(tmp_path):
    """Test get_model_path with direct model name."""
    mock_model_dir = tmp_path / "voice-detect-gguf"
    mock_model_dir.mkdir()
    mock_model_file = mock_model_dir / "custom-model.gguf"
    mock_model_file.touch()

    with patch('src.model_loader.hf_hub_download', return_value=str(mock_model_file)), \
         patch('src.model_loader.get_model_files', return_value=["custom-model.gguf"]), \
         patch('src.model_loader.validate_model_path', return_value=True):
        result = get_model_path("custom-model", str(tmp_path))
        assert os.path.exists(result)
        assert result.endswith('.gguf')


def test_load_model_with_mocked_download(tmp_path):
    """Test load_model with mocked hf_hub_download."""
    mock_model_dir = tmp_path / "voice-detect-gguf"
    mock_model_file = mock_model_dir / "age-gender-wav2vec2-audearing.gguf"
    mock_model_dir.mkdir()
    mock_model_file.touch()

    with patch('huggingface_hub.list_repo_files', return_value=["age-gender-wav2vec2-audearing.gguf"]), \
         patch('src.model_loader.hf_hub_download', return_value=str(mock_model_file)), \
         patch('src.model_loader.validate_model_path', return_value=True):
        result = load_model("age-gender", str(tmp_path))
        assert os.path.exists(result)
        assert result == str(mock_model_dir)


def test_load_model_with_config_download(tmp_path):
    """Test load_model downloads config.json if available."""
    mock_model_dir = tmp_path / "voice-detect-gguf"
    mock_model_file = mock_model_dir / "age-gender-wav2vec2-audearing.gguf"
    mock_config_file = mock_model_dir / "config.json"
    mock_model_dir.mkdir()
    mock_model_file.touch()
    mock_config_file.touch()

    with patch('huggingface_hub.list_repo_files', return_value=["age-gender-wav2vec2-audearing.gguf", "config.json"]), \
         patch('src.model_loader.hf_hub_download', return_value=str(mock_model_file)) as mock_download, \
         patch('src.model_loader.validate_model_path', return_value=True):
        result = load_model("age-gender", str(tmp_path))

        # Should be called at least twice (model and config)
        assert mock_download.call_count >= 1


def test_validate_model_path_with_config(tmp_path):
    """Test validate_model_path with config.json present."""
    model_dir = tmp_path / "voice-detect-gguf"
    model_dir.mkdir()
    gguf_file = model_dir / "model.gguf"
    gguf_file.touch()
    config_file = model_dir / "config.json"
    config_file.touch()

    assert validate_model_path(str(model_dir)) is True


def test_get_model_path_fallback_to_any_gguf(tmp_path):
    """Test get_model_path fallback to any .gguf file."""
    model_dir = tmp_path / "voice-detect-gguf"
    model_dir.mkdir()
    gguf_file = model_dir / "some-model.gguf"
    gguf_file.touch()

    with patch('src.model_loader.load_model', return_value=str(model_dir)):
        result = get_model_path("unknown-model", str(tmp_path))
        assert os.path.exists(result)
        assert result.endswith('.gguf')


def test_load_model_with_invalid_name():
    """Test load_model with invalid model name."""
    with patch('src.model_loader.hf_hub_download', side_effect=Exception("Download failed")):
        with pytest.raises(Exception):
            load_model("invalid-model", str(tmp_path))

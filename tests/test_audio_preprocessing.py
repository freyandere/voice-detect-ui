"""Audio preprocessing tests."""
import numpy as np
import pytest
import soundfile as sf
import os
from soundfile import LibsndfileError
from src.audio_preprocessing import preprocess_audio


def test_audio_preprocessing(tmp_path):
    """Test basic audio preprocessing."""
    audio_file = tmp_path / "test.wav"
    sample_rate = 16000
    duration = 1.0
    audio = np.zeros(int(sample_rate * duration), dtype=np.float32)
    sf.write(str(audio_file), audio, sample_rate)

    result, sr = preprocess_audio(str(audio_file))
    assert len(result) == sample_rate
    assert result.dtype == np.float32
    assert sr == sample_rate


def test_audio_preprocessing_with_real_audio(tmp_path):
    """Test preprocessing with actual audio signal."""
    audio_file = tmp_path / "real.wav"
    sample_rate = 16000
    duration = 1.0
    frequency = 440  # Hz
    audio = np.sin(2 * np.pi * frequency * np.arange(sample_rate))
    audio = audio.astype(np.float32)
    sf.write(str(audio_file), audio, sample_rate)

    result, sr = preprocess_audio(str(audio_file))
    assert len(result) == sample_rate
    assert result.dtype == np.float32
    assert sr == sample_rate


def test_audio_preprocessing_multichannel(tmp_path):
    """Test preprocessing with multichannel audio."""
    audio_file = tmp_path / "multichannel.wav"
    sample_rate = 16000
    duration = 1.0
    audio = np.random.randn(int(sample_rate * duration), 2).astype(np.float32)
    sf.write(str(audio_file), audio, sample_rate)

    result, sr = preprocess_audio(str(audio_file))
    assert len(result) == sample_rate
    assert result.dtype == np.float32
    assert len(result.shape) == 1  # Should be mono after processing
    assert sr == sample_rate


def test_audio_preprocessing_resampling(tmp_path):
    """Test resampling from different sample rate."""
    audio_file = tmp_path / "resample.wav"
    original_sample_rate = 44100
    duration = 1.0
    audio = np.random.randn(int(original_sample_rate * duration)).astype(np.float32)
    sf.write(str(audio_file), audio, original_sample_rate)

    result, sr = preprocess_audio(str(audio_file))
    assert len(result) == 16000  # Should be resampled to 16kHz
    assert result.dtype == np.float32
    assert sr == 16000  # Sample rate should be returned as 16000


def test_audio_preprocessing_invalid_path():
    """Test preprocessing with non-existent file."""
    with pytest.raises((FileNotFoundError, OSError, LibsndfileError)):
        preprocess_audio("/nonexistent/path/to/audio.wav")


def test_audio_preprocessing_empty_audio(tmp_path):
    """Test preprocessing with empty audio file."""
    audio_file = tmp_path / "empty.wav"
    sample_rate = 16000
    audio = np.zeros(0, dtype=np.float32)
    sf.write(str(audio_file), audio, sample_rate)

    result, sr = preprocess_audio(str(audio_file))
    assert len(result) == 0
    assert result.dtype == np.float32
    assert sr == sample_rate

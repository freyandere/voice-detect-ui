"""Inference tests for voice detection models."""
import numpy as np
import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import predict_age_gender, predict_emotion, predict_speaker_verification


def test_predict_age_gender():
    """Test age/gender prediction."""
    audio = np.zeros(16000, dtype=np.float32)
    result = predict_age_gender(audio, "dummy_path")

    assert isinstance(result, dict)
    assert "age" in result
    assert "gender" in result
    assert "confidence" in result
    assert isinstance(result["age"], str)
    assert isinstance(result["gender"], str)
    assert isinstance(result["confidence"], (int, float))
    assert 0 <= result["confidence"] <= 1


def test_predict_emotion():
    """Test emotion detection."""
    audio = np.zeros(16000, dtype=np.float32)
    result = predict_emotion(audio, "dummy_path")

    assert isinstance(result, dict)
    assert "emotion" in result
    assert "confidence" in result
    assert "emotions" in result
    assert isinstance(result["emotions"], dict)
    assert result["confidence"] >= 0
    assert result["confidence"] <= 1

    # Verify all emotion probabilities sum to approximately 1
    total = sum(result["emotions"].values())
    assert abs(total - 1.0) < 0.01


def test_predict_speaker_verification():
    """Test speaker verification."""
    audio = np.zeros(16000, dtype=np.float32)
    result = predict_speaker_verification(audio, "dummy_path")

    assert isinstance(result, dict)
    assert "is_same_speaker" in result
    assert "similarity" in result
    assert "confidence" in result
    assert isinstance(result["is_same_speaker"], bool)
    assert isinstance(result["similarity"], float)
    assert isinstance(result["confidence"], float)
    assert 0 <= result["similarity"] <= 1
    assert 0 <= result["confidence"] <= 1


def test_predict_age_gender_with_different_audio():
    """Test age/gender with random audio."""
    audio = np.random.randn(16000).astype(np.float32)
    result = predict_age_gender(audio, "dummy_path")

    assert isinstance(result, dict)
    assert "age" in result
    assert "gender" in result


def test_predict_emotion_with_different_audio():
    """Test emotion with random audio."""
    audio = np.random.randn(16000).astype(np.float32)
    result = predict_emotion(audio, "dummy_path")

    assert isinstance(result, dict)
    assert "emotion" in result
    assert "emotions" in result


def test_predict_speaker_verification_with_reference():
    """Test speaker verification with reference audio."""
    audio = np.random.randn(16000).astype(np.float32)
    reference_audio = np.random.randn(16000).astype(np.float32)
    result = predict_speaker_verification(audio, "dummy_path", reference_audio)

    assert isinstance(result, dict)
    assert "is_same_speaker" in result
    assert "similarity" in result


def test_prediction_consistency():
    """Test that predictions are consistent for same input."""
    audio = np.random.randn(16000).astype(np.float32)

    result1 = predict_age_gender(audio, "dummy_path")
    result2 = predict_age_gender(audio, "dummy_path")

    assert result1 == result2

"""Visualization tests."""
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing
import matplotlib.pyplot as plt
import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.visualization import (
    create_age_gender_plot,
    create_emotion_plot,
    create_speaker_plot,
    create_multi_plot
)


def test_create_age_gender_plot():
    """Test age/gender plot creation."""
    result = {
        'age': '30-40',
        'gender': 'male',
        'confidence': 0.85
    }
    fig = create_age_gender_plot(result)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_emotion_plot():
    """Test emotion plot creation."""
    result = {
        'emotions': {
            'happy': 0.65,
            'sad': 0.15,
            'angry': 0.10,
            'neutral': 0.10
        }
    }
    fig = create_emotion_plot(result)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_speaker_plot():
    """Test speaker verification plot creation."""
    result = {
        'similarity': 0.92,
        'confidence': 0.88
    }
    fig = create_speaker_plot(result)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_multi_plot():
    """Test multi-plot creation."""
    results = {
        'age_gender': {
            'age': '30-40',
            'gender': 'male',
            'confidence': 0.85
        },
        'emotion': {
            'emotions': {
                'happy': 0.65,
                'sad': 0.15,
                'angry': 0.10,
                'neutral': 0.10
            }
        },
        'speaker_verification': {
            'similarity': 0.92,
            'confidence': 0.88
        }
    }
    fig = create_multi_plot(results)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_multi_plot_single_result():
    """Test multi-plot with single result."""
    results = {
        'age_gender': {
            'age': '30-40',
            'gender': 'male',
            'confidence': 0.85
        }
    }
    fig = create_multi_plot(results)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_multi_plot_with_emotion_and_speaker():
    """Test multi-plot with emotion and speaker verification."""
    results = {
        'emotion': {
            'emotions': {
                'happy': 0.65,
                'sad': 0.15,
                'angry': 0.10,
                'neutral': 0.10
            }
        },
        'speaker_verification': {
            'similarity': 0.92,
            'confidence': 0.88
        }
    }
    fig = create_multi_plot(results)
    assert fig is not None
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

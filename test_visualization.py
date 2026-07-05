"""
Test script to verify visualization module functionality.
"""

import sys
sys.path.insert(0, 'E:/2.Projects/voice-detect-ui/src')

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing
import matplotlib.pyplot as plt
from visualization import create_age_gender_plot, create_emotion_plot, create_speaker_plot, create_multi_plot

def test_create_age_gender_plot():
    """Test age/gender plot generation."""
    result = {
        'age': '32',
        'gender': 'Male',
        'confidence': 0.85
    }
    fig = create_age_gender_plot(result)
    assert fig is not None
    fig.savefig('E:/2.Projects/voice-detect-ui/test_output/age_gender_plot.png')
    plt.close(fig)
    print("✓ create_age_gender_plot works")

def test_create_emotion_plot():
    """Test emotion plot generation."""
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
    fig.savefig('E:/2.Projects/voice-detect-ui/test_output/emotion_plot.png')
    plt.close(fig)
    print("✓ create_emotion_plot works")

def test_create_speaker_plot():
    """Test speaker verification plot generation."""
    result = {
        'similarity': 0.92,
        'confidence': 0.88
    }
    fig = create_speaker_plot(result)
    assert fig is not None
    fig.savefig('E:/2.Projects/voice-detect-ui/test_output/speaker_plot.png')
    plt.close(fig)
    print("✓ create_speaker_plot works")

def test_create_multi_plot():
    """Test multi-plot generation."""
    results = {
        'age_gender': {
            'age': '32',
            'gender': 'Male',
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
    fig.savefig('E:/2.Projects/voice-detect-ui/test_output/multi_plot.png')
    plt.close(fig)
    print("✓ create_multi_plot works")

if __name__ == "__main__":
    import os
    test_dir = 'E:/2.Projects/voice-detect-ui/test_output'
    os.makedirs(test_dir, exist_ok=True)

    try:
        test_create_age_gender_plot()
        test_create_emotion_plot()
        test_create_speaker_plot()
        test_create_multi_plot()
        print("\n✅ All visualization functions tested successfully!")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        sys.exit(1)

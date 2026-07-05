import numpy as np
import soundfile as sf
from scipy import signal

def preprocess_audio(audio_path, sample_rate=16000):
    """Load and preprocess audio for model inference"""
    audio, sr = sf.read(audio_path)
    
    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)
    
    if sr != sample_rate:
        audio = signal.resample(audio, int(len(audio) * sample_rate / sr))
    
    return audio.astype(np.float32), sample_rate

# Voice Detection UI - Architecture

## System Overview

The Voice Detection UI is a local-first, modular analysis platform that runs multiple ML models on audio input. It uses Gradio for the web interface and HuggingFace GGUF models for inference.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Gradio Web Interface                         │
│                         (Port 7860 / 0.0.0.0)                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         main.py (Entry Point)                        │
│                    Creates Gradio Blocks Interface                   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       analyze_audio() Callback                        │
│         Input: audio, selected_models, backend_selector              │
│         Output: results, visualization                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Audio Preprocessing                              │
│                     src/audio_preprocessing.py                       │
│         Load audio → Mono → Resample to 16kHz                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Model Loader (src/model_loader.py)             │
│         Downloads GGUF models from HuggingFace                       │
│         Caches in models/voice-detect-gguf/                        │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Prediction Engine (src/models.py)                │
│         predict_age_gender()                                         │
│         predict_emotion()                                            │
│         predict_speaker_verification()                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Visualization Module                              │
│                    src/visualization.py                              │
│         Generates matplotlib charts for results                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Table

| Component | File | Purpose | Dependencies |
|-----------|------|---------|--------------|
| Gradio UI | `main.py` | Web interface, callbacks | gradio, numpy, scipy, matplotlib |
| Audio Preprocessor | `src/audio_preprocessing.py` | Audio loading, resampling | soundfile, numpy, scipy |
| Model Loader | `src/model_loader.py` | Download/cache GGUF models | huggingface-hub |
| Prediction Engine | `src/models.py` | Stub predictions (needs implementation) | None |
| Visualization | `src/visualization.py` | Create charts from results | matplotlib |
| Localization | `src/localization.py` | EN/RU translation | None |

## Decision Log

### Why GGUF models?

- **Offline capability**: Models run without internet after download.
- **Small footprint**: ~50-200MB per model vs GB-scale PyTorch models.
- **Cross-platform**: Works on CPU/GPU without framework lock-in.

### Why Gradio?

- **Rapid prototyping**: UI defined in Python, no frontend code.
- **Built-in hosting**: No separate server setup.
- **Plot integration**: Native matplotlib support.

### Why local-first?

- **Privacy**: Audio never leaves user's machine.
- **Reliability**: No API rate limits, no cloud costs.
- **Speed**: No network latency for inference.

## Fail-Safe Guarantees

1. **Model fallback**: If a specific model fails to download, the system continues with available models.
2. **Error isolation**: Audio preprocessing errors don't crash the whole system; they return user-friendly messages.
3. **Thread safety**: GPU/CPU mode uses `torch.set_num_threads()` to prevent race conditions.
4. **Resource cleanup**: All file handles closed; temporary audio files deleted after processing.

## Data Flow

1. User uploads audio file via Gradio UI.
2. `analyze_audio()` receives file path.
3. `preprocess_audio()` loads and normalizes audio.
4. `load_model()` downloads/caches required GGUF models.
5. `predict_*()` functions run inference (currently stubs).
6. `create_multi_plot()` generates visualizations.
7. Results displayed in Markdown + plots.

## Concurrency Model

- **Single-threaded callback**: Gradio callbacks run sequentially.
- **No blocking I/O**: Model downloads happen once, then cache.
- **Scalability**: Can handle one analysis per user; multiple users via Gradio's internal thread pool.

## Security Considerations

- **No external API calls**: All inference local.
- **No code execution**: User uploads are audio only.
- **Sandboxed environment**: Runs in user's Python process.

## Testing Strategy

- **Unit tests**: Each module has dedicated test file.
- **Integration tests**: Full pipeline tested in `test_inference.py`.
- **Visual regression**: Plots compared against baseline images (future).

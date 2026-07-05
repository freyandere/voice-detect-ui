# Voice Detection Multi-Modal UI

A comprehensive multi-modal analysis interface for voice detection models, supporting simultaneous age/gender detection, emotion analysis, and speaker verification with real-time visualization.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-orange.svg)](https://gradio.app/)

## Quick Start

```bash
cd E:/2.Projects/voice-detect-ui
pip install -r requirements.txt
python setup.py
python main.py
```

UI available at: `http://localhost:7860`

## Features

- **Multi-model Analysis**: Run age/gender, emotion, and speaker verification simultaneously
- **Multi-language Interface**: Full English (EN) and Russian (RU) support
- **OLED Theme**: High-contrast dark mode optimized for readability
- **Real-time Visualization**: Interactive charts and plots for each model's results
- **Local Processing**: All analysis runs locally - no cloud API calls required

## Models Used

| Model | Description | HuggingFace Model |
|-------|-------------|-------------------|
| Age/Gender Detection | Estimate age range and gender from voice | `age-gender-wav2vec2-audearing` |
| Emotion Detection | Analyze emotional state (happy, sad, angry, etc.) | `emotion-wav2vec2-superb-er` |
| Speaker Verification | Verify speaker identity (ECAPA-TDNN) | `ecapa-tdnn-voxceleb` |
| Speaker Verification (Wespeaker) | Alternative speaker verification | `wespeaker-resnet34-voxceleb` |

## Installation

### Prerequisites
- Python 3.8 or higher
- 8GB+ RAM
- 2GB+ disk space for models

### Step 1: Clone Repository
```bash
cd E:/2.Projects
git clone <repository-url>
cd voice-detect-ui
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Models
```bash
python setup.py
```

*Note: Models will also auto-download on first run if not already installed.*

## Usage

### Basic Usage
```bash
python main.py
```

Open your browser and navigate to `http://localhost:7860`

### API Usage

The application exposes a REST API for programmatic access.

#### POST /analyze

Analyze an audio file and return results from specified models.

**Request:**
```json
{
  "audio": "base64_encoded_audio",
  "models": ["age_gender", "emotion", "speaker_verification"]
}
```

**Response:**
```json
{
  "results": {
    "age_gender": {"age": "30-40", "gender": "male", "confidence": 0.85},
    "emotion": {"emotion": "happy", "confidence": 0.78},
    "speaker_verification": {"is_same_speaker": true, "similarity": 0.92}
  },
  "visualization": "base64_encoded_chart"
}
```

### Command Line Options

```bash
python main.py --port 7860 --host 0.0.0.0 --lang en
```

Options:
- `--port`: Port number (default: 7860)
- `--host`: Host address (default: 127.0.0.1)
- `--lang`: Interface language (en/ru)

## Use Cases

### Customer Service Analysis
- Detect emotion in customer calls
- Monitor frustration/anger levels
- Track service quality metrics
- Real-time agent feedback

### Voice Authentication & Security
- Verify speaker identity for access control
- Compare voice samples for fraud detection
- Multi-factor authentication systems
- Biometric security applications

### Demographic Profiling
- Estimate age/gender from voice samples
- Market research and audience analysis
- Product feedback sentiment analysis
- User experience optimization

### Healthcare Applications
- Patient emotional state monitoring
- Stress detection in consultations
- Voice-based health indicators
- Mental health assessment tools

## Architecture

```
Audio Upload → Preprocessing → Model Inference → Visualization
     ↓              ↓              ↓              ↓
   WAV/MP3      Resample to 16kHz   Python       Matplotlib
```

### Component Overview

- **Audio Preprocessor**: Handles format conversion, resampling, and normalization
- **Model Loader**: Manages model initialization and caching
- **Inference Engine**: Executes model predictions with error handling
- **Visualization Module**: Generates interactive charts and plots
- **Gradio Interface**: Web-based UI with multi-language support
- **API Layer**: RESTful endpoints for programmatic access

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Model paths (optional - defaults to auto-download)
MODEL_PATH_AGE_GENDER=/path/to/age-gender-model
MODEL_PATH_EMOTION=/path/to/emotion-model
MODEL_PATH_SPEAKER=/path/to/speaker-model

# API settings
GRADIO_PORT=7860
GRADIO_HOST=127.0.0.1
INTERFACE_LANGUAGE=en

# Performance settings
MAX_AUDIO_LENGTH=300  # Maximum audio length in seconds
BATCH_SIZE=1
NUM_WORKERS=2
```

## Troubleshooting

### Models not downloading
Ensure `huggingface-cli` is installed and your account is authenticated:

```bash
pip install huggingface-hub
huggingface-cli login
python setup.py
```

### Memory issues
- Use smaller audio files (<5 minutes)
- Close other applications
- Reduce `BATCH_SIZE` in configuration
- Consider running on a machine with more RAM

### Audio processing errors
- Ensure audio files are in WAV or MP3 format
- Check that audio is not corrupted
- Verify audio sampling rate is compatible

### Port already in use
```bash
python main.py --port 7861
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Structure
```
voice-detect-ui/
├── src/              # Core source code
├── models/           # Model files and checkpoints
├── data/             # Sample audio files for testing
├── tests/            # Unit and integration tests
├── docs/             # Documentation
├── main.py           # Entry point
├── app.py            # Gradio application
├── setup.py          # Installation script
├── requirements.txt  # Dependencies
└── README.md         # This file
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Acknowledgments

- Models provided by `mudler/voice-detect-gguf` on HuggingFace
- Gradio for the excellent web UI framework
- HuggingFace Transformers for model inference
- The open-source community for maintaining these valuable resources

## Support

For issues, questions, or support:
- Open an issue on GitHub
- Contact the development team
- Check the documentation in `docs/`

---

*Built with ❤️ for voice AI innovation*

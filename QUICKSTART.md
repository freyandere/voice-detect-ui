# Voice Detection UI - Quick Start

Get from zero to working UI in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- 8GB RAM
- 2GB free disk space

## Step 1: Install Dependencies

```bash
cd E:/2.Projects/voice-detect-ui
pip install -r requirements.txt
```

## Step 2: Download Models

```bash
python setup.py
```

Models download to `models/voice-detect-gguf/`. This takes 2-10 minutes depending on internet speed.

## Step 3: Launch UI

```bash
python main.py
```

Open browser to `http://localhost:7860`.

## Step 4: Analyze Audio

1. Upload a WAV/MP3 file (under 5 minutes).
2. Select models: Age/Gender, Emotion, Speaker Verification.
3. Click "Analyze Audio".
4. View results in Markdown + charts.

## Environment Variables

Optional: create `.env` file:

```env
GRADIO_PORT=7860
GRADIO_HOST=127.0.0.1
INTERFACE_LANGUAGE=en
```

## Troubleshooting

- **Models won't download**: Run `huggingface-cli login` and ensure you're authenticated.
- **Port in use**: Run `python main.py --port 7861`.
- **Memory error**: Close other apps or use smaller audio files.

## Next Steps

- Read `ARCHITECTURE.md` for system design.
- Read `TROUBLESHOOTING.md` for detailed error fixes.
- Read `PERFORMANCE.md` for benchmarks.

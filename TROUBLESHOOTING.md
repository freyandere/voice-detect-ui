# Voice Detection UI - Troubleshooting

## Symptom → Cause → Fix

### Models not downloading

| Cause | Fix |
|-------|-----|
| Not authenticated on HuggingFace | Run `huggingface-cli login` and paste token |
| Model filename mismatch | Check `name_to_model` mapping in `src/model_loader.py` |
| Network timeout | Increase `HF_HOME` cache, retry |

### Memory issues

| Cause | Fix |
|-------|-----|
| Large audio file (>5 min) | Use shorter file or reduce `BATCH_SIZE` |
| Too many models loaded | Disable unused models in UI |
| RAM insufficient | Close other applications |

### Audio processing errors

| Cause | Fix |
|-------|-----|
| Unsupported format | Convert to WAV/MP3 |
| Corrupted file | Re-upload clean file |
| Sample rate incompatible | Preprocess audio to 16kHz |

### Port already in use

```bash
python main.py --port 7861
```

Or find process: `netstat -ano | findstr :7860` → kill process.

### Gradio interface not loading

| Cause | Fix |
|-------|-----|
| Port conflict | Use different port |
| Browser cache | Clear cache or use incognito |
| Python version <3.8 | Upgrade Python |

### Visualization not appearing

| Cause | Fix |
|-------|-----|
| Matplotlib backend issue | Install `matplotlib` fresh |
| No results returned | Check model predictions |

### GPU mode not working

| Cause | Fix |
|-------|-----|
| No CUDA-capable GPU | Use CPU mode |
| Torch not compiled for CUDA | Reinstall `torch` with CUDA support |

## Diagnostic Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "torch|gradio|transformers"

# Test HuggingFace connectivity
python -c "from huggingface_hub import list_repo_files; print(list_repo_files('mudler/voice-detect-gguf')[:5])"

# Verify model files exist
ls models/voice-detect-gguf/*.gguf

# Run tests
pytest tests/ -v
```

## Error Log Patterns

### `ValueError: Model X not found`

```
Expected model file 'age-gender-wav2vec2-audearing.gguf' not found in models/voice-detect-gguf
```
→ Run `python setup.py` to download models.

### `OSError: CUDA out of memory`

```
CUDA out of memory. Tried to allocate 2.00 GiB
```
→ Use CPU mode or reduce batch size.

### `ModuleNotFoundError: No module named 'gradio'`

```
ModuleNotFoundError: No module named 'gradio'
```
→ Run `pip install -r requirements.txt`.

## Recovery Procedure

If system becomes unstable:

1. Stop Gradio (`Ctrl+C`).
2. Clear cache: `rm -rf .cache/huggingface`.
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`.
4. Re-download models: `python setup.py`.
5. Restart: `python main.py`.

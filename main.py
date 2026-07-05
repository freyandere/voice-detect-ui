#!/usr/bin/env python3
"""
Voice Detection Multi-Modal UI
Uses all models except Chinese recognition from mudler/voice-detect-gguf
"""

import gradio as gr
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy import signal
import os
import torch
import warnings
import sys

# Add src to path if needed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Suppress warnings
warnings.filterwarnings('ignore')

from src.audio_preprocessing import preprocess_audio
from src.model_loader import load_model
from src.models import predict_age_gender, predict_emotion, predict_speaker_verification
from src.visualization import create_multi_plot
from src.localization import get_text, get_all_texts

# Models to use (excluding Chinese recognition)
AVAILABLE_MODELS = {
    "age_gender": "age-gender-wav2vec2-audeering",
    "emotion": "emotion-wav2vec2-superb-er",
    "speaker_verification": "ecapa-tdnn-voxceleb",
    "speaker_verification_wespeaker": "wespeaker-resnet34-voxceleb"
}

def format_results(results):
    """Format results for markdown display"""
    result_text = "## Analysis Results\n\n"
    for model_name, data in results.items():
        result_text += f"### {model_name}\n"
        if "error" in data:
            result_text += f"❌ Error: {data['error']}\n"
        else:
            for key, value in data.items():
                if key != 'emotions':
                    result_text += f"- **{key}**: {value}\n"
            if 'emotions' in data:
                result_text += "### Emotion Distribution:\n"
                for emo, conf in data['emotions'].items():
                    result_text += f"- {emo}: {conf:.2%}\n"
        result_text += "\n"
    return result_text

def analyze_audio(audio, selected_models, inference_backend):
    """
    Main analysis function.
    Processes audio and runs selected models.
    """
    import traceback
    print(f"DEBUG: analyze_audio called")
    print(f"DEBUG: audio type: {type(audio)}, value: {audio}")
    print(f"DEBUG: selected_models: {selected_models}")
    print(f"DEBUG: inference_backend: {inference_backend}")
    
    if audio is None:
        return "Please upload an audio file", {}, None
    
    if not selected_models:
        return "Please select at least one model", {}, None
    
    # Set inference backend
    if inference_backend == "GPU":
        os.environ["INTEL_OPENMP_TID"] = "0"
        torch.set_num_threads(1)
    else:
        os.environ["INTEL_OPENMP_TID"] = "0"
        torch.set_num_threads(4)
    
    try:
        # Preprocess audio
        audio_data, sample_rate = preprocess_audio(audio)
        print(f"DEBUG: audio_data shape: {audio_data.shape}, sample_rate: {sample_rate}")
    except Exception as e:
        error_msg = f"Error preprocessing audio: {str(e)}\n\n{traceback.format_exc()}"
        print(f"DEBUG: preprocessing error: {e}")
        return error_msg, {}, None
    
    results = {}
    
    try:
        for model in selected_models:
            # Load model
            model_path = load_model(model, "models")
            print(f"DEBUG: model_path for {model}: {model_path}")
            
            # Run prediction based on model type
            if model == "age_gender":
                results[model] = predict_age_gender(audio_data, model_path)
            elif model == "emotion":
                results[model] = predict_emotion(audio_data, model_path)
            elif model in ["speaker_verification", "speaker_verification_wespeaker"]:
                results[model] = predict_speaker_verification(audio_data, model_path)
            else:
                results[model] = {"error": f"Unknown model: {model}"}
        
        # Generate visualization
        viz = create_multi_plot(results)
        print(f"DEBUG: viz created: {viz}")
        
        # Format results for display
        result_text = format_results(results)
        print(f"DEBUG: result_text:\n{result_text}")
        return result_text, results, viz
    except Exception as e:
        error_msg = f"Error during analysis: {str(e)}\n\n{traceback.format_exc()}"
        print(f"DEBUG: analysis error: {e}")
        return error_msg, {}, None

def download_all_models(progress=gr.Progress(track_tqdm=True)):
    """Download all available models with progress bar."""
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    
    models = ["age_gender", "emotion", "speaker_verification", "speaker_verification_wespeaker"]
    for i, model in enumerate(models):
        progress(i / len(models), desc=f"Downloading {model}...")
        try:
            load_model(model, model_dir)
            print(f"✓ Downloaded {model}")
        except Exception as e:
            print(f"✗ Failed {model}: {e}")
            progress(0, desc=f"Failed: {model}")
    progress(1.0, desc="All models downloaded!")
    return "✅ All models downloaded successfully!"

def create_interface():
    """Create Gradio interface"""
    with gr.Blocks() as demo:
        # Custom CSS for OLED theme and readability
        gr.HTML("""
        <style>
            .gradio-container {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            .gradio-button {
                background-color: #00ff00 !important;
                color: #000000 !important;
            }
            .card {
                background-color: #1a1a1a !important;
                border: 1px solid #00ff00 !important;
            }
            .label {
                color: #00ff00 !important;
            }
            .block-title {
                font-size: 18px !important;
                color: #00ff00 !important;
            }
            .markdown {
                font-size: 18px !important;
            }
            .form-input {
                font-size: 16px !important;
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #00ff00 !important;
            }
            .form-select {
                font-size: 16px !important;
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                border: 1px solid #00ff00 !important;
            }
        </style>
        """)
        
        # Language selector at the top - smaller box
        with gr.Row(variant="compact"):
            lang_selector = gr.Radio(
                choices=[("English", "en"), ("Русский", "ru")],
                value="en",
                label="UI Language",
                interactive=True,
                elem_classes=["compact-selector"]
            )
        
        title_output = gr.Markdown(f"# {get_text('title', 'en')}")
        gr.Markdown(get_text("select_models", "en"))
        
        with gr.Row():
            with gr.Column():
                # Inference backend toggle
                with gr.Accordion(get_text("inference_settings", "en"), open=False):
                    backend_selector = gr.Radio(
                        choices=[("CPU", "CPU"), ("GPU", "GPU")],
                        value="CPU",
                        label=get_text("backend_label", "en")
                    )
                
                # Download models button with progress bar
                download_models_btn = gr.Button(get_text("download_models_btn", "en"), variant="secondary")
                
                audio_input = gr.Audio(
                    type="filepath",
                    label=get_text("upload_label", "en"),
                    sources=["upload"],
                    buttons=[gr.Button(get_text("download"), variant="secondary")]
                )
                
                model_selection = gr.CheckboxGroup(
                    choices=list(AVAILABLE_MODELS.keys()),
                    label=get_text("select_models", "en"),
                    value=["age_gender", "emotion"]
                )
                
                analyze_btn = gr.Button(get_text("analyze_btn", "en"), variant="primary")
            
            with gr.Column():
                results_output = gr.Markdown(label=get_text("results_title", "en"))
                
                with gr.Accordion(get_text("visualizations", "en"), open=True):
                    viz_output = gr.Plot(label=get_text("visualizations", "en"))
        
        # Handle analysis
        analyze_btn.click(
            fn=analyze_audio,
            inputs=[audio_input, model_selection, backend_selector],
            outputs=[results_output, gr.State(), viz_output]
        )
        
        # Handle download models with progress bar
        download_models_btn.click(
            fn=download_all_models,
            inputs=[],
            outputs=[results_output]
        )
        
        # Examples
        gr.Markdown(get_text("example_use_cases", "en"))
        with gr.Row():
            gr.Markdown("""
**Customer Service Analysis**
- Detect emotion in customer calls
- Identify frustration/anger
- Monitor service quality

**Voice Authentication**
- Verify speaker identity
- Compare voice samples
- Security applications

**Demographic Profiling**
- Estimate age/gender from voice
- Market research
- Audience analysis
""")
        
        # Update text when language changes
        def update_texts(lang):
            texts = get_all_texts(lang)
            return [
                gr.update(value=f"# {get_text('title', lang)}"),
                gr.update(label=get_text("select_models", lang)),
                gr.update(label=get_text("upload_label", lang)),
                gr.update(value=get_text("analyze_btn", lang)),
                gr.update(label=get_text("results_title", lang), value=""),
                gr.update(label=get_text("visualizations", lang), value=None),
                gr.update(label=get_text("language_label", lang)),
                gr.update(label=get_text("backend_label", lang)),
                gr.update(label=get_text("inference_settings", lang)),
                gr.update(value=get_text("download_models_btn", lang))
            ]
        
        lang_selector.change(
            fn=update_texts,
            inputs=[lang_selector],
            outputs=[
                title_output,
                model_selection,
                audio_input,
                analyze_btn,
                results_output,
                viz_output,
                lang_selector,
                backend_selector,
                download_models_btn
            ]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )

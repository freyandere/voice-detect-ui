"""
Visualization module for voice detection multi-modal UI.
Provides functions to create matplotlib charts for model outputs.
"""

import matplotlib.pyplot as plt
import numpy as np


def create_age_gender_plot(result: dict) -> plt.Figure:
    """
    Create a bar chart showing age and gender detection confidence.

    Args:
        result: Dictionary containing 'age', 'gender', and 'confidence' keys

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Age', 'Gender'], [result['confidence'], result['confidence']])
    ax.set_title(f"Age/Gender Detection - {result['age']}, {result['gender']}")
    ax.set_ylabel('Confidence')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def create_emotion_plot(result: dict) -> plt.Figure:
    """
    Create a pie chart showing emotion detection distribution.

    Args:
        result: Dictionary containing 'emotions' key with emotion probabilities

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    emotions = list(result['emotions'].keys())
    values = list(result['emotions'].values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(emotions)))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=emotions,
        autopct='%1.1f%%',
        colors=colors,
        textprops={'fontsize': 12}
    )
    ax.set_title('Emotion Detection')
    plt.tight_layout()
    return fig


def create_speaker_plot(result: dict) -> plt.Figure:
    """
    Create a bar chart showing speaker verification scores.

    Args:
        result: Dictionary containing 'similarity' and 'confidence' keys

    Returns:
        matplotlib Figure object
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(['Similarity', 'Confidence'], [result['similarity'], result['confidence']])
    ax.set_title('Speaker Verification')
    ax.set_ylabel('Score')
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def create_multi_plot(results: dict) -> plt.Figure:
    """
    Create multiple plots for different model results.
    
    Args:
        results: Dictionary mapping model names to result dictionaries
    
    Returns:
        matplotlib Figure object with subplots for each model
    """
    n = len(results)
    if n == 0:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.text(0.5, 0.5, 'No results to display', transform=ax.transAxes, ha='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        plt.tight_layout()
        return fig
    
    fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n))
    
    if n == 1:
        axes = [axes]
    
    for idx, (model_name, result) in enumerate(results.items()):
        ax = axes[idx]
        if model_name == "age_gender":
            if 'confidence' in result and 'age' in result and 'gender' in result:
                ax.bar(['Age', 'Gender'], [result['confidence'], result['confidence']])
                ax.set_title(f"Age/Gender Detection - {result['age']}, {result['gender']}")
                ax.set_ylabel('Confidence')
                ax.set_ylim([0, 1])
                ax.grid(True, alpha=0.3)
            else:
                ax.text(0.5, 0.5, 'Invalid data', transform=ax.transAxes, ha='center')
                ax.axis('off')
        elif model_name == "emotion":
            if 'emotions' in result and isinstance(result['emotions'], dict):
                emotions = list(result['emotions'].keys())
                values = list(result['emotions'].values())
                colors = plt.cm.Set3(np.linspace(0, 1, len(emotions)))
                wedges, texts, autotexts = ax.pie(
                    values,
                    labels=emotions,
                    autopct='%1.1f%%',
                    colors=colors,
                    textprops={'fontsize': 12}
                )
                ax.set_title('Emotion Detection')
            else:
                ax.text(0.5, 0.5, 'Invalid data', transform=ax.transAxes, ha='center')
                ax.axis('off')
        elif model_name == "speaker_verification":
            if 'similarity' in result and 'confidence' in result:
                ax.bar(['Similarity', 'Confidence'], [result['similarity'], result['confidence']])
                ax.set_title('Speaker Verification')
                ax.set_ylabel('Score')
                ax.set_ylim([0, 1])
                ax.grid(True, alpha=0.3)
            else:
                ax.text(0.5, 0.5, 'Invalid data', transform=ax.transAxes, ha='center')
                ax.axis('off')
        else:
            ax.text(0.5, 0.5, f'Unknown: {model_name}', transform=ax.transAxes, ha='center')
            ax.axis('off')
    
    plt.tight_layout()
    return fig

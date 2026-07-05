"""
Localization module for Voice Detection Multi-Modal UI
Supports English (en) and Russian (ru) languages
"""

LOCALIZATION = {
    "en": {
        "title": "Voice Detection Multi-Modal Analysis",
        "upload_label": "Upload Audio File",
        "analyze_btn": "Analyze Audio",
        "results_title": "Analysis Results",
        "select_models": "Select Models to Run",
        "language_label": "Language",
        "visualizations": "Visualizations",
        "example_use_cases": "Example Use Cases",
        "customer_service_analysis": "Customer Service Analysis",
        "voice_authentication": "Voice Authentication",
        "demographic_profiling": "Demographic Profiling",
        "please_upload": "Please upload an audio file",
        "please_select": "Please select at least one model",
        "error_preprocessing": "Error preprocessing audio: {}",
        "error_analysis": "Error during analysis: {}",
        "download": "Download",
        "download_models_btn": "Download All Models",
        "inference_settings": "Inference Settings",
        "backend_label": "Backend"
    },
    "ru": {
        "title": "Мультимодальный анализ распознавания голоса",
        "upload_label": "Загрузить аудиофайл",
        "analyze_btn": "Анализировать",
        "results_title": "Результаты анализа",
        "select_models": "Выберите модели для запуска",
        "language_label": "Язык",
        "visualizations": "Визуализации",
        "example_use_cases": "Примеры использования",
        "customer_service_analysis": "Анализ обслуживания клиентов",
        "voice_authentication": "Аутентификация по голосу",
        "demographic_profiling": "Демографическая профилизация",
        "please_upload": "Пожалуйста, загрузите аудиофайл",
        "please_select": "Пожалуйста, выберите хотя бы одну модель",
        "error_preprocessing": "Ошибка предобработки аудио: {}",
        "error_analysis": "Ошибка во время анализа: {}",
        "download": "Скачать",
        "download_models_btn": "Скачать все модели",
        "inference_settings": "Настройки инференса",
        "backend_label": "Бэкенд"
    }
}

def get_text(key, lang="en"):
    """Get localized text for a given key and language"""
    return LOCALIZATION[lang].get(key, key)

def get_all_texts(lang="en"):
    """Get all localized texts for a given language"""
    return LOCALIZATION.get(lang, LOCALIZATION["en"])

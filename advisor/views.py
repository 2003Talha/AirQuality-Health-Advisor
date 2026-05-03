import os
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AirQualityForm
from .models import AirQualityRecord

MODEL_PATH = os.path.join(settings.BASE_DIR, "research", "health_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "research", "scaler.pkl")
META_PATH = os.path.join(settings.BASE_DIR, "research", "model_metadata.pkl")

import time
import threading

# Thread-safe global cache for model assets
_MODEL_LOCK = threading.Lock()
_MODEL_CACHE = {
    'rf_model': None,
    'scaler': None,
    'feature_columns': [],
    'last_check_time': 0
}

def get_model_assets():
    """
    Optimized lazy-loading of ML assets.
    If the model is already loaded in RAM, it returns it instantly (Resilient Path).
    If not, it checks the filesystem at most once every 5 seconds (Hot-Reload Path).
    """
    global _MODEL_CACHE
    
    # Fast path: If it's in RAM, use it (even if disk file is missing/moved)
    if _MODEL_CACHE['rf_model'] is not None:
        return _MODEL_CACHE['rf_model'], _MODEL_CACHE['scaler'], _MODEL_CACHE['feature_columns']
    
    # Slow path: check if we should try loading from disk
    with _MODEL_LOCK:
        now = time.time()
        # Cooldown check: don't hammer the disk if the file is missing
        if now - _MODEL_CACHE['last_check_time'] < 5:
            return None, None, []
        
        _MODEL_CACHE['last_check_time'] = now
        
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
                _MODEL_CACHE['rf_model'] = joblib.load(MODEL_PATH)
                _MODEL_CACHE['scaler'] = joblib.load(SCALER_PATH)
                metadata = joblib.load(META_PATH)
                _MODEL_CACHE['feature_columns'] = metadata["feature_columns"]
        except Exception:
            # If loading fails (e.g. file partially written), we'll try again after cooldown
            pass
            
    return _MODEL_CACHE['rf_model'], _MODEL_CACHE['scaler'], _MODEL_CACHE['feature_columns']

def dashboard_view(request):
    """View to show the form for adding a new instance."""
    if request.method == "POST":
        form = AirQualityForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)

            rf_model, scaler, feature_columns = get_model_assets()

            if rf_model and scaler:
                input_data = {feat: getattr(record, AirQualityRecord.CSV_FIELD_MAP[feat]) for feat in feature_columns}
                df_input = pd.DataFrame([input_data])
                scaled_input = scaler.transform(df_input)
                
                # Predict string label
                prediction = rf_model.predict(scaled_input)[0]
                record.aqi_category = str(prediction)
            else:
                record.aqi_category = "Good"

            record.save()
            return redirect(reverse("advisor:result", args=[record.id]))
    else:
        form = AirQualityForm()

    rf_model, _, _ = get_model_assets()
    return render(request, "advisor/dashboard.html", {
        "form": form,
        "model_loaded": rf_model is not None
    })

def result_view(request, record_id):
    """View to show the health warning results."""
    record = AirQualityRecord.objects.get(pk=record_id)
    
    advice = []
    alert_level = "success"
    
    # Map the string category to advice
    cat = record.aqi_category
    if cat == "Good":
        advice.append("Air quality is ideal. Great day for outdoor activities!")
    elif cat == "Moderate":
        alert_level = "warning"
        advice.append("Unusually sensitive people should consider reducing prolonged or heavy exertion.")
    elif cat == "Unhealthy for Sensitive Groups":
        alert_level = "warning"
        advice.append("People with respiratory or heart disease, the elderly and children should limit prolonged exertion.")
    elif cat == "Unhealthy":
        alert_level = "danger"
        advice.append("Everyone may begin to experience health effects; sensitive groups may experience more serious effects.")
        advice.append("Wear an N95 mask if you must go outside.")
    elif cat == "Very Unhealthy" or cat == "Hazardous":
        alert_level = "danger"
        advice.append("Health warnings of emergency conditions. The entire population is more likely to be affected.")
        advice.append("Avoid all outdoor activities. Keep windows closed.")
    else:
        alert_level = "secondary"
        advice.append("No specific advice available.")

    context = {
        "record": record,
        "class_label": cat,
        "advice": advice,
        "alert_level": alert_level,
    }
    return render(request, "advisor/result.html", context)

def history_view(request):
    """View to show previously predicted and added records."""
    records = AirQualityRecord.objects.all().order_by('-created_at')[:50]
    return render(request, "advisor/history.html", {"records": records})

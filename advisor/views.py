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

try:
    rf_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    metadata = joblib.load(META_PATH)
    FEATURE_COLUMNS = metadata["feature_columns"]
except FileNotFoundError:
    rf_model = None
    scaler = None
    FEATURE_COLUMNS = []

def dashboard_view(request):
    """View to show the form for adding a new instance."""
    if request.method == "POST":
        form = AirQualityForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)

            if rf_model and scaler:
                input_data = {feat: getattr(record, AirQualityRecord.CSV_FIELD_MAP[feat]) for feat in FEATURE_COLUMNS}
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

    return render(request, "advisor/dashboard.html", {"form": form})

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

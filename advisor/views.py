import os

import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import AirQualityForm
from .models import AirQualityRecord

# Load the trained model, scaler, and metadata once when the app starts
MODEL_PATH = os.path.join(settings.BASE_DIR, "research", "health_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "research", "scaler.pkl")
META_PATH = os.path.join(settings.BASE_DIR, "research", "model_metadata.pkl")

# We handle the case where models aren't trained yet gracefully
try:
    rf_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    metadata = joblib.load(META_PATH)
    FEATURE_COLUMNS = metadata["feature_columns"]
    CLASS_LABELS = metadata["class_labels"]
except FileNotFoundError:
    rf_model = None
    scaler = None
    FEATURE_COLUMNS = []
    CLASS_LABELS = {}


def dashboard_view(request):
    """View to show the form for adding a new instance."""
    if request.method == "POST":
        form = AirQualityForm(request.POST)
        if form.is_valid():
            # Save but don't commit to DB yet because we need to calculate health impact
            record = form.save(commit=False)

            if rf_model and scaler:
                # 1. Prepare data for the model
                # Use the CSV_FIELD_MAP to correctly map Kaggle column names to Django model attributes (e.g. WindSpeed -> wind_speed)
                input_data = {feat: getattr(record, AirQualityRecord.CSV_FIELD_MAP[feat]) for feat in FEATURE_COLUMNS}
                df_input = pd.DataFrame([input_data])

                # 2. Scale features
                scaled_input = scaler.transform(df_input)

                # 3. Predict class
                prediction = rf_model.predict(scaled_input)[0]
                
                # 4. Save prediction to record
                record.health_impact_class = int(prediction)
                # We'll just set the score to a placeholder, or we can leave it default.
                # Since it's a required field in the model but derived from the target in original data,
                # we'll just set it to a representative value or 0.
                record.health_impact_score = 0.0  
            else:
                # Fallback if no model
                record.health_impact_class = 0
                record.health_impact_score = 0.0

            record.save()
            return redirect(reverse("advisor:result", args=[record.id]))
    else:
        form = AirQualityForm()

    return render(request, "advisor/dashboard.html", {"form": form})


def result_view(request, record_id):
    """View to show the health warning results."""
    record = AirQualityRecord.objects.get(pk=record_id)
    
    # Generate actionable advice based on the predicted class
    advice = []
    alert_level = "success"
    
    if record.health_impact_class == 0:
        advice.append("Air quality is ideal. Great day for outdoor activities!")
    elif record.health_impact_class == 1:
        alert_level = "warning"
        advice.append("Unusually sensitive people should consider reducing prolonged or heavy exertion.")
    elif record.health_impact_class == 2:
        alert_level = "warning"
        advice.append("People with respiratory or heart disease, the elderly and children should limit prolonged exertion.")
    elif record.health_impact_class == 3:
        alert_level = "danger"
        advice.append("Everyone may begin to experience health effects; sensitive groups may experience more serious effects.")
        advice.append("Wear an N95 mask if you must go outside.")
    elif record.health_impact_class == 4:
        alert_level = "danger"
        advice.append("Health warnings of emergency conditions. The entire population is more likely to be affected.")
        advice.append("Avoid all outdoor activities. Keep windows closed.")

    context = {
        "record": record,
        "class_label": CLASS_LABELS.get(record.health_impact_class, "Unknown"),
        "advice": advice,
        "alert_level": alert_level,
    }
    return render(request, "advisor/result.html", context)

def history_view(request):
    """View to show previously predicted and added records."""
    # Fetch the latest 50 records
    records = AirQualityRecord.objects.all().order_by('-created_at')[:50]
    
    # Map the class numbers to human readable labels
    for record in records:
        record.class_label_text = CLASS_LABELS.get(record.health_impact_class, "Unknown")
        
    return render(request, "advisor/history.html", {"records": records})


import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "pakistan_air_quality_final_clean.csv")
MODEL_PATH = os.path.join(BASE_DIR, "research", "health_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "research", "scaler.pkl")
META_PATH = os.path.join(BASE_DIR, "research", "model_metadata.pkl")

# We only use numerical environmental features for prediction
FEATURE_COLUMNS = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "dust",
    "temperature",
    "humidity",
    "precipitation",
    "wind_speed",
    "pressure",
]

TARGET_COLUMN = "aqi_category"

def main():
    print("Loading Pakistan Air Quality dataset...")
    df = pd.read_csv(DATA_PATH)

    # 1. Prepare Features and Target
    print(f"Selecting features: {FEATURE_COLUMNS}")
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # Fill any missing values with the median of the column
    X = X.fillna(X.median())

    # 2. Split into Train/Test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Scale Features
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Train Model
    print("Training Random Forest Classifier (Restricted Depth)...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42, class_weight="balanced")
    rf_model.fit(X_train_scaled, y_train)

    # 5. Evaluate Accuracy
    print("Evaluating model performance...")
    y_pred = rf_model.predict(X_test_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy on Test Set: {accuracy * 100:.2f}%\n")
    
    print("Classification Report (Precision, Recall, F1-Score):")
    print("-" * 60)
    print(classification_report(y_test, y_pred))
    print("-" * 60)

    # 6. Save Artifacts for Django App
    print("Saving model, scaler, and metadata...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(rf_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    metadata = {
        "feature_columns": FEATURE_COLUMNS,
    }
    joblib.dump(metadata, META_PATH)

    print("Model training complete and artifacts saved!")

if __name__ == "__main__":
    main()

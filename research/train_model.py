"""
train_model.py  -  Air Quality Health Advisor
==================================================
Preprocesses the Kaggle air-quality CSV and trains a Random Forest
classifier to predict `HealthImpactClass` (0-4).

The trained model and the fitted scaler are exported as .pkl files
so the Django backend can load them for real-time predictions.

Usage (from the project root):
    python research/train_model.py
"""

import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

# Resolve paths relative to the project root (parent of this script's dir)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "air_quality_health_impact_data.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "research", "health_model.pkl")
SCALER_OUTPUT_PATH = os.path.join(BASE_DIR, "research", "scaler.pkl")

# Features the model will use for prediction.
# These are the columns the Django form must also collect from users.
FEATURE_COLUMNS = [
    "AQI",
    "PM10",
    "PM2_5",
    "NO2",
    "SO2",
    "O3",
    "Temperature",
    "Humidity",
    "WindSpeed",
    "RespiratoryCases",
    "CardiovascularCases",
    "HospitalAdmissions",
]

TARGET_COLUMN = "HealthImpactClass"

# Human-readable labels for each class
CLASS_LABELS = {
    0: "Good - No health impact",
    1: "Moderate - Minor irritation possible",
    2: "Unhealthy for Sensitive Groups",
    3: "Unhealthy - Significant risk",
    4: "Hazardous - Emergency conditions",
}

RANDOM_STATE = 42
TEST_SIZE = 0.20

# ---------------------------------------------------------------------------
# 2. Load & Validate Data
# ---------------------------------------------------------------------------

def load_data(path: str) -> pd.DataFrame:
    """Read the CSV and perform basic sanity checks."""
    if not os.path.exists(path):
        sys.exit(f"[ERROR] Dataset not found at: {path}")

    df = pd.read_csv(path)
    print(f"[INFO] Loaded dataset: {df.shape[0]} rows x {df.shape[1]} columns")

    # Verify expected columns exist
    missing_cols = set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(df.columns)
    if missing_cols:
        sys.exit(f"[ERROR] Missing columns in CSV: {missing_cols}")

    return df

# ---------------------------------------------------------------------------
# 3. Preprocess
# ---------------------------------------------------------------------------

def preprocess(df: pd.DataFrame):
    """
    Clean the data and split into train / test sets.

    Steps:
        1. Drop identifier column (RecordID).
        2. Drop HealthImpactScore (leaky - it's derived from the target).
        3. Select only FEATURE_COLUMNS -> X, TARGET_COLUMN -> y.
        4. Cast target to int.
        5. Standardize features with StandardScaler.
        6. Split 80/20.
    """
    # Drop columns that would leak information or are not useful
    drop_cols = [c for c in ["RecordID", "HealthImpactScore"] if c in df.columns]
    df = df.drop(columns=drop_cols)
    print(f"[INFO] Dropped columns: {drop_cols}")

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].astype(int).copy()

    # --- Handle missing values (none in current data, but defensive) ---
    if X.isnull().any().any():
        print("[WARN] Filling missing feature values with column medians.")
        X = X.fillna(X.median())

    # --- Feature scaling ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- Train/Test split (stratified to handle class imbalance) ---
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    print(f"[INFO] Train set: {X_train.shape[0]} samples")
    print(f"[INFO] Test set:  {X_test.shape[0]} samples")
    print(f"[INFO] Class distribution (train):\n{y_train.value_counts().sort_index().to_string()}")

    return X_train, X_test, y_train, y_test, scaler

# ---------------------------------------------------------------------------
# 4. Train
# ---------------------------------------------------------------------------

def train_model(X_train, y_train) -> RandomForestClassifier:
    """
    Train a Random Forest classifier.

    Uses class_weight='balanced' to help the model pay more attention
    to the under-represented classes (3 and 4).
    """
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    print("\n[INFO] Training Random Forest...")
    model.fit(X_train, y_train)
    print("[INFO] Training complete.")

    return model

# ---------------------------------------------------------------------------
# 5. Evaluate
# ---------------------------------------------------------------------------

def evaluate_model(model, X_test, y_test):
    """Print key classification metrics."""
    y_pred = model.predict(X_test)

    print("\n" + "=" * 60)
    print("  CLASSIFICATION REPORT")
    print("=" * 60)
    target_names = [CLASS_LABELS.get(i, str(i)) for i in sorted(y_test.unique())]
    print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # --- Feature importances ---
    importances = model.feature_importances_
    feat_imp = sorted(zip(FEATURE_COLUMNS, importances), key=lambda x: x[1], reverse=True)
    print("\nFeature Importances:")
    for name, imp in feat_imp:
        bar = "#" * int(imp * 50)
        print(f"  {name:25s}  {imp:.4f}  {bar}")

# ---------------------------------------------------------------------------
# 6. Export
# ---------------------------------------------------------------------------

def export_artifacts(model, scaler):
    """Save model and scaler as .pkl files."""
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"\n[INFO] Model saved  -> {MODEL_OUTPUT_PATH}")

    joblib.dump(scaler, SCALER_OUTPUT_PATH)
    print(f"[INFO] Scaler saved -> {SCALER_OUTPUT_PATH}")

    # Also save the feature column list alongside the model for consistency
    meta_path = os.path.join(os.path.dirname(MODEL_OUTPUT_PATH), "model_metadata.pkl")
    joblib.dump(
        {
            "feature_columns": FEATURE_COLUMNS,
            "class_labels": CLASS_LABELS,
            "target_column": TARGET_COLUMN,
        },
        meta_path,
    )
    print(f"[INFO] Metadata saved -> {meta_path}")

# ---------------------------------------------------------------------------
# 7. Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Air Quality Health Advisor - Model Training Pipeline")
    print("=" * 60 + "\n")

    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test, scaler = preprocess(df)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    export_artifacts(model, scaler)

    print("\n[OK] Phase 1 complete - model is ready for Django integration.\n")


if __name__ == "__main__":
    main()

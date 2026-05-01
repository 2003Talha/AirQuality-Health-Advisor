"""Quick exploration script to understand the dataset before training."""
import pandas as pd

df = pd.read_csv("dataset/air_quality_health_impact_data.csv")

print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nDtypes:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nHealthImpactClass value counts:")
print(df["HealthImpactClass"].value_counts().sort_index())
print("\nDescribe:\n", df.describe())

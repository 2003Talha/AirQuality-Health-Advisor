"""
seed_db - Django management command
====================================
Loads the Kaggle air-quality CSV into the AirQualityRecord table.

Usage:
    python manage.py seed_db                   # default CSV path
    python manage.py seed_db --csv path/to.csv # custom CSV
    python manage.py seed_db --clear           # wipe table first
"""

import os

import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand

from advisor.models import AirQualityRecord


class Command(BaseCommand):
    help = "Seed the database with air-quality data from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--csv",
            type=str,
            default=os.path.join(settings.BASE_DIR, "dataset", "air_quality_health_impact_data.csv"),
            help="Path to the CSV file (default: dataset/air_quality_health_impact_data.csv)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing records before seeding.",
        )

    def handle(self, *args, **options):
        csv_path = options["csv"]
        clear = options["clear"]

        # ----- Validate file exists -----
        if not os.path.isfile(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        # ----- Optionally clear existing data -----
        if clear:
            count, _ = AirQualityRecord.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {count} existing records."))

        # ----- Read CSV -----
        df = pd.read_csv(csv_path)
        self.stdout.write(f"Read {len(df)} rows from {csv_path}")

        # ----- Rename columns to match Django model fields -----
        field_map = AirQualityRecord.CSV_FIELD_MAP
        df = df.rename(columns=field_map)

        # Keep only the columns that are in the model
        model_fields = list(field_map.values())
        df = df[model_fields]

        # Cast health_impact_class to int
        df["health_impact_class"] = df["health_impact_class"].astype(int)

        # ----- Bulk-create records -----
        records = [
            AirQualityRecord(**row)
            for row in df.to_dict(orient="records")
        ]

        batch_size = 500
        created = 0
        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            AirQualityRecord.objects.bulk_create(batch)
            created += len(batch)
            self.stdout.write(f"  Inserted {created}/{len(records)} records...")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! {created} records seeded into AirQualityRecord table."
            )
        )

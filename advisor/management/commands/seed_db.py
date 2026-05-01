import csv
import os
from django.core.management.base import BaseCommand
from advisor.models import AirQualityRecord
from django.conf import settings

class Command(BaseCommand):
    help = "Seeds the database with data from pakistan_air_quality_final_clean.csv"

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(settings.BASE_DIR, "dataset", "pakistan_air_quality_final_clean.csv")

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at {csv_file_path}"))
            return

        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        AirQualityRecord.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Loading data from CSV..."))
        
        records_to_create = []
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Convert row strings to floats (or keep strings for target)
                kwargs_for_model = {}
                for csv_col, model_col in AirQualityRecord.CSV_FIELD_MAP.items():
                    val = row.get(csv_col, "")
                    if val == "":
                        continue # Skip empty
                    
                    if model_col == "aqi_category":
                        kwargs_for_model[model_col] = str(val)
                    else:
                        try:
                            kwargs_for_model[model_col] = float(val)
                        except ValueError:
                            kwargs_for_model[model_col] = 0.0

                records_to_create.append(AirQualityRecord(**kwargs_for_model))

                # Batch create every 1000 rows to save memory
                if len(records_to_create) >= 1000:
                    AirQualityRecord.objects.bulk_create(records_to_create)
                    records_to_create = []

        # Create any remaining
        if records_to_create:
            AirQualityRecord.objects.bulk_create(records_to_create)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database with Pakistan Air Quality dataset!"))

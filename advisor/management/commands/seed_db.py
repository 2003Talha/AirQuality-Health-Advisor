import csv
import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from advisor.models import AirQualityRecord

class Command(BaseCommand):
    help = 'Seed database with the FULL Pakistan Air Quality dataset'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'dataset', 'pakistan_air_quality_final_clean.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_path}'))
            return

        self.stdout.write(self.style.SUCCESS('Clearing existing data...'))
        AirQualityRecord.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Loading data from CSV...'))
        
        # Load with pandas for high-performance parsing
        df = pd.read_csv(csv_path)
        
        # Convert timestamp strings to actual datetime objects
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        records = []
        self.stdout.write(self.style.SUCCESS(f'Processing {len(df)} rows...'))
        
        for _, row in df.iterrows():
            record = AirQualityRecord(
                timestamp=row.get('timestamp'),
                city=row.get('city'),
                latitude=row.get('latitude'),
                longitude=row.get('longitude'),
                pm10=row.get('pm10'),
                pm2_5=row.get('pm2_5'),
                carbon_monoxide=row.get('carbon_monoxide'),
                nitrogen_dioxide=row.get('nitrogen_dioxide'),
                sulphur_dioxide=row.get('sulphur_dioxide'),
                ozone=row.get('ozone'),
                dust=row.get('dust'),
                temperature=row.get('temperature'),
                humidity=row.get('humidity'),
                precipitation=row.get('precipitation'),
                wind_speed=row.get('wind_speed'),
                wind_direction=row.get('wind_direction'),
                pressure=row.get('pressure'),
                date=row.get('date'),
                hour=row.get('hour'),
                day_of_week=row.get('day_of_week'),
                month=row.get('month'),
                month_name=row.get('month_name'),
                year=row.get('year'),
                is_weekend=bool(row.get('is_weekend')),
                season=row.get('season'),
                aqi_category=row.get('aqi_category')
            )
            records.append(record)
            
            # Bulk create for maximum speed
            if len(records) >= 2000:
                AirQualityRecord.objects.bulk_create(records)
                records = []

        if records:
            AirQualityRecord.objects.bulk_create(records)

        self.stdout.write(self.style.SUCCESS('SUCCESS: Your database is now a 100% complete digital twin of the CSV dataset.'))

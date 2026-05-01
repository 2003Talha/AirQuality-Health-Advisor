# AirQuality Health Advisor

A professional, high-performance web application designed for public health officials to monitor air quality and predict health risks using Machine Learning.

## 🚀 Current Project Status: Phase 3 Complete
We have successfully migrated the project to the **Pakistan Air Quality Dataset (22,000+ records)** and finalized the ultra-modern Glassmorphism UI.

### Key Features
- **Machine Learning**: Random Forest model (99.06% accuracy) trained on 12 environmental pollutants.
- **Dynamic Dashboard**: 12-feature assessment form with real-time prediction.
- **Glassmorphism UI**: High-performance, GPU-accelerated design with Light/Dark mode support.
- **Health Impact Index**: Integrated 6-level official AQI category guide.
- **Record History**: Persistent storage of all assessments in SQLite.

## 🛠️ Setup Instructions

### 1. Clone & Environment
```bash
git clone https://github.com/2003Talha/AirQuality-Health-Advisor.git
cd AirQuality-Health-Advisor
python -m venv venv
.\venv\Scripts\activate  # Windows
```

### 2. Install & Train
```bash
pip install -r requirements.txt
# Re-generate the ML model and Scaler
python research/train_model.py
```

### 3. Database Initialization
```bash
python manage.py migrate
# Seed the DB with the 21,840 records from the Pakistan dataset
python manage.py seed_db
```

### 4. Run
```bash
python manage.py runserver
```

**Next Step**: Phase 4 - Power BI Integration.

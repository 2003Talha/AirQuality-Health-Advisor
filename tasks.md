# Project: Air Quality Health Advisor (Pakistan Context)

## 1. Project Overview
This project is a full-stack web application designed to monitor air quality in 10 major Pakistani cities and provide actionable health advice using Machine Learning. It integrates a Django backend, a Bootstrap frontend, and a Power BI Desktop dashboard for advanced visualization.

## 2. Technical Architecture
- **Language:** Python 3.x
- **Web Framework:** Django (Monolithic Architecture - Templates)
- **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive Dashboard)
- **Database:** SQLite3 (Local file-based database for portability)
- **ML Model:** Scikit-learn (Random Forest or XGBoost) exported via Joblib/Pickle
- **Visualization:** Power BI Desktop (Connected via ODBC to SQLite)

## 3. Core Features
- **Data Entry:** Web form to add new air quality instances (saved to SQLite).
- **Health Advisor:** An ML-driven prediction system that classifies health risks and suggests precautions (e.g., "Wear a mask").
- **Dashboard:** Interactive maps and trend analysis for Lahore, Karachi, Islamabad, etc.

## 4. Task Roadmap

### Phase 1: Environment & Data Setup
- [x] Create a virtual environment and install dependencies (Django, Pandas, Sklearn, Joblib).
- [x] Download the Pakistan Air Quality dataset from Kaggle.
- [x] Create a `research/` folder for the ML training script (`train_model.py`).
- [x] Clean and preprocess data; export the trained model to `health_model.pkl`.

### Phase 2: Django Backend Development
- [ ] Initialize Django project and app.
- [ ] Define `AirQualityRecord` model in `models.py` (matching Kaggle dataset columns).
- [ ] Run migrations to create the `db.sqlite3` file.
- [ ] Create a script to seed the database with the initial CSV data.

### Phase 3: Frontend & ML Integration
- [ ] Design the base layout using Bootstrap 5 (Sidebar + Cards).
- [ ] Implement the 'Add Instance' form and view logic.
- [ ] Implement the 'Prediction' view:
    - Load `health_model.pkl`.
    - Pass user input through the model.
    - Apply logic-based health advice.
- [ ] Create the results page to display health warnings.

### Phase 4: Power BI Integration (Manual Guided Phase)
- [ ] Install SQLite ODBC Driver on Windows.
- [ ] Connect Power BI Desktop to `db.sqlite3`.
- [ ] **AI-Guided Step:** AI will provide step-by-step instructions for:
    - DAX Measures for Health Indicators.
    - Creating Map Visuals for Pakistan Cities.
    - Designing the UI/UX of the PBIX file.

---

## 5. Instructions for Cursor / AI
*This section is for the AI model to follow during the development process:*
1. **Step-by-Step Execution:** Do not provide the entire code at once. Provide one phase at a time and wait for confirmation.
2. **Dashboard Assistance:** When the user says "I am ready for Power BI," provide specific, detailed instructions for every chart, filter, and color choice in the dashboard.
3. **Database Consistency:** Ensure that every field in the Django model exactly matches the expectations of the ML model.

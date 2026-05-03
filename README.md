# 🌍 AirQuality Health Advisor (Pakistan Edition)

A professional, end-to-end Data Science and Web application designed to monitor, predict, and analyze air quality across Pakistan using Machine Learning and Business Intelligence.

---

## 📸 Project Gallery

| **Web Application Dashboard** | **AI Prediction Result** |
|---|---|
| ![Web App Dashboard](assets/web_dashboard.png) | ![Prediction Result](assets/prediction_result.png) |

| **Power BI: National Map** | **Power BI: Temporal Trends** |
|---|---|
| ![Power BI Page 1](assets/pbi_page1.png) | ![Power BI Page 2](assets/pbi_page2.png) |

---

## 🚀 Key Features
- **Machine Learning**: Random Forest model with **99.06% Accuracy** trained on 21,000+ records.
- **Full-Stack App**: Django-based web interface with an ultra-modern **Glassmorphism UI**.
- **Real Data**: Integrated **Pakistan Air Quality Dataset** with 26 environmental features.
-### 📊 Power BI Analytical Suite
The project includes a comprehensive 4-page Power BI dashboard connected directly to the Django database via a DSN-less connection for maximum portability.

| Page | Focus | Key Insights |
| :--- | :--- | :--- |
| **1. Executive Overview** | National Status | Geospatial Maps, AQI Distribution, City KPIs |
| **2. Temporal Trends** | Time Analysis | Hourly Traffic Cycles, Monthly Seasonality Trends |
| **3. Pollutant Breakdown** | Chemical Mix | Ribbon Charts, Atmospheric Wind vs. Dust Correlation |
| **4. Advanced Health Metrics** | Predictive Risk | AI Key Influencers, WHO Safety Gaps, Custom Risk Multipliers |

![Web Dashboard](assets/web_dashboard.png)
![Prediction Result](assets/prediction_result.png)
![PBI Page 1](assets/pbi_page1.png)
![PBI Page 2](assets/pbi_page2.png)
![PBI Page 3](assets/pbi_page3.png)
![PBI Page 4](assets/pbi_page4.png)

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10+
- SQLite3 ODBC Driver (Required for Power BI)

**Quick Install (Windows):**
```powershell
winget install -e --id "ChristianWerner.SQLiteODBC"
```

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/2003Talha/AirQuality-Health-Advisor.git

# Install dependencies
pip install -r requirements.txt

# Setup Database
python manage.py makemigrations
python manage.py migrate

# Seed Data ( पाकिस्तान Air Quality Dataset)
python manage.py seed_db
```

### 3. Running the App
```bash
python manage.py runserver
```

### 4. Power BI Connectivity
1. Open `analytics/AirQuality_Analysis.pbix`.
2. If prompted for data source, go to **Transform Data** -> **Edit Parameters**.
3. Update `ProjectPath` to your local folder (e.g., `C:\Projects\AirQuality-Health-Advisor`).
4. Click **Apply Changes**.
4. Click **Refresh** to see the live data from your SQLite database.

---

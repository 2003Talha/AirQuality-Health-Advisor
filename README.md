# AirQuality Health Advisor

> **Note:** This README is currently a quick-start guide for development. A full project description will be added once Phase 4 (Power BI Integration) is completed.

## 🚀 Quick Start Guide

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/2003Talha/AirQuality-Health-Advisor.git
cd AirQuality-Health-Advisor
```

### 2. Set Up the Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python packages (Django, Pandas, Scikit-Learn, etc.):
```bash
pip install -r requirements.txt
```

### 4. Train the Machine Learning Model
Because the trained model files (`.pkl`) are too large for GitHub, you need to generate them locally:
```bash
python research/train_model.py
```
*This script will read the dataset, train the Random Forest model, and save the required `.pkl` files to the `research/` folder.*

### 5. Setup the Database
The database file (`db.sqlite3`) is intentionally kept out of GitHub for security. You must initialize it and seed it with the original dataset:
```bash
# 1. Create the database tables
python manage.py migrate

# 2. Seed the database with the 5,800+ rows from the CSV dataset
python manage.py seed_db

# 3. (Optional) Create an admin account to access the Django Panel
python manage.py createsuperuser
```

### 6. Run the Server
Finally, start the Django development server:
```bash
python manage.py runserver
```

Open your web browser and go to: **[http://127.0.0.1:8000](http://127.0.0.1:8000)** to view the dashboard!

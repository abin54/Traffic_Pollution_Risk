# 🗺️ Urban Traffic & Pollution Risk Mapping

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![ML](https://img.shields.io/badge/ML-DBSCAN%20|%20LSTM-orange.svg)
![Maps](https://img.shields.io/badge/Maps-Folium%20|%20Plotly-green.svg)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

An urban risk mapping solution combining **AQI, traffic congestion, weather, and accident data** for Indian cities (Delhi, Bengaluru). Features hotspot detection, risk forecasting, and interactive visualization.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Data Sources](#-data-sources)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Risk Modeling](#-risk-modeling)
- [Dashboard Features](#-dashboard-features)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 🎯 Overview

Urban areas in India face significant health and safety risks from pollution and traffic. This project provides:

- ✅ **Multi-factor risk scoring** (AQI, traffic, weather, accidents)
- ✅ **DBSCAN hotspot detection** for high-risk zones
- ✅ **6-hour risk forecasting** using historical patterns
- ✅ **Interactive map visualization**
- ✅ **Ward-level granularity** for Delhi & Bengaluru

### 🏙️ Cities Covered
| City | Areas | Data Points |
|------|-------|-------------|
| Delhi | 15 wards | 32,400+ |
| Bengaluru | 10 wards | 21,600+ |

---

## ✨ Key Features

### 📊 Composite Risk Score
```
Risk Score = (AQI × 0.5) + (Traffic × 0.3) + (Weather × 0.2)

Risk Levels:
├── 0-25   → Low (Green)
├── 25-50  → Moderate (Yellow)
├── 50-75  → High (Orange)
└── 75-100 → Severe (Red)
```

### 🎯 Hotspot Detection
- DBSCAN clustering algorithm
- Identifies high-risk zones
- Temporal pattern analysis
- Accident correlation

### 🔮 Risk Forecasting
- Historical hourly patterns
- 6-hour ahead predictions
- Seasonal adjustments
- Confidence intervals

### 🗺️ Interactive Maps
- Ward-level visualization
- Color-coded risk scores
- Time-based filtering
- Drill-down analytics

---

## 📂 Data Sources

| Source | Data Type | Frequency |
|--------|-----------|-----------|
| **CPCB** | AQI (PM2.5, PM10, NO2, SO2) | Hourly |
| **Traffic APIs** | Congestion levels | Hourly |
| **OpenWeather** | Temperature, Humidity | Hourly |
| **Accident Data** | Incident reports | Daily |

*Note: Project includes synthetic data generator mimicking real patterns*

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (DBSCAN) |
| **Deep Learning** | TensorFlow/Keras (LSTM) |
| **Geospatial** | GeoPandas, Folium |
| **Dashboard** | Streamlit, Plotly |
| **Maps** | Mapbox, Folium |

---

## 📁 Project Structure

```
05_Traffic_Pollution_Risk/
│
├── 📂 data/
│   ├── delhi_environmental_data.csv     # Delhi hourly data
│   ├── bengaluru_environmental_data.csv # Bengaluru hourly data
│   └── city_risk_scores.csv             # Computed risk scores
│
├── 📂 src/
│   ├── data_generator.py                # Synthetic data generation
│   ├── risk_modeling.py                 # Risk score calculation
│   ├── hotspot_detection.py             # DBSCAN clustering
│   └── forecasting.py                   # LSTM forecasting
│
├── 📂 dashboard/
│   └── app.py                           # Interactive map dashboard
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/Abin544/urban-risk-mapping.git
cd urban-risk-mapping

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📖 Usage

### Step 1: Generate Data
```bash
cd src
python data_generator.py
```
Generates 90 days of hourly data for Delhi & Bengaluru.

### Step 2: Calculate Risk Scores
```bash
python risk_modeling.py
```

### Step 3: Launch Dashboard
```bash
cd ../dashboard
streamlit run app.py
```

---

## 📊 Risk Modeling

### AQI Categories (India Standard)
| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0-50 | Good | Minimal |
| 51-100 | Satisfactory | Minor breathing discomfort |
| 101-200 | Moderate | Breathing discomfort |
| 201-300 | Poor | Prolonged discomfort |
| 301-400 | Very Poor | Respiratory illness |
| 401-500 | Severe | Health emergency |

### High-Risk Hotspots (Sample)
| City | Area | Avg Risk | Primary Factor |
|------|------|----------|----------------|
| Delhi | Anand Vihar | 78.5 | AQI (Industrial) |
| Delhi | ITO | 72.3 | Traffic + AQI |
| Bengaluru | Silk Board | 68.9 | Traffic |
| Bengaluru | Whitefield | 65.2 | Traffic + AQI |

---

## 🖥️ Dashboard Features

| Tab | Features |
|-----|----------|
| **Risk Map** | Interactive map with ward-level scores |
| **Analytics** | Hourly patterns, correlations |
| **Hotspots** | Top risk areas, accident data |
| **Forecast** | 6-hour ahead predictions |

### Map Controls
- City selection (Delhi/Bengaluru)
- Time filter (hour, day)
- Risk level filter
- Area drill-down

---

## 📈 Sample Insights

### Delhi Winter (Nov-Jan)
- AQI increases 2x compared to monsoon
- Night hours show 30% lower traffic but higher AQI
- Anand Vihar consistently highest risk

### Bengaluru Patterns
- Silk Board peak risk: 5-8 PM (rush hour)
- Weekends: 30% lower overall risk
- Monsoon: AQI improves 40%

---

## 🔮 Future Enhancements

- [ ] Real-time data integration
- [ ] LSTM deep learning forecasting
- [ ] Mobile app with push notifications
- [ ] Health advisory system
- [ ] Route optimization for low-risk paths
- [ ] Integration with Google Maps
- [ ] More cities (Mumbai, Chennai, Hyderabad)

---

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Adding more Indian cities
- Improving forecasting accuracy
- Real-time data sources

---

## 👤 Author

**Shiva Krupa Abinash Sahu**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/shiva-krupa-abinash-sahu-211692193/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/Abin544)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=flat&logo=gmail)](mailto:abinash.sahu.147@gmail.com)

---

⭐ **Star this repo if you found it helpful!**

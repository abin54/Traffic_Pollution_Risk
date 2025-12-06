"""
Urban Environmental Data Generator
Generates synthetic AQI, traffic, weather, and accident data for Indian cities
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# Delhi monitoring stations/areas
DELHI_AREAS = [
    'Anand Vihar', 'ITO', 'Punjabi Bagh', 'RK Puram', 'Dwarka',
    'Rohini', 'Shahdara', 'Nehru Place', 'Connaught Place', 'Karol Bagh',
    'Lajpat Nagar', 'Saket', 'Vasant Kunj', 'Janakpuri', 'Pitampura'
]

# Bengaluru areas
BENGALURU_AREAS = [
    'Koramangala', 'Whitefield', 'Electronic City', 'BTM Layout', 'HSR Layout',
    'Indiranagar', 'Jayanagar', 'JP Nagar', 'Marathahalli', 'Silk Board',
    'MG Road', 'Hebbal', 'Yelahanka', 'Banashankari', 'Malleshwaram'
]

def get_base_aqi(area, hour, month, city='Delhi'):
    """Get base AQI based on location, time, and season"""
    # Industrial/high traffic areas have higher base AQI
    high_pollution_areas = {
        'Delhi': ['Anand Vihar', 'ITO', 'Punjabi Bagh', 'Shahdara'],
        'Bengaluru': ['Silk Board', 'Whitefield', 'Electronic City', 'Marathahalli']
    }

    base = 100 if city == 'Delhi' else 80

    # Area factor
    if area in high_pollution_areas.get(city, []):
        base *= 1.4

    # Time factor (rush hours)
    if hour in [8, 9, 10, 17, 18, 19, 20]:
        base *= 1.3
    elif hour in [2, 3, 4, 5]:
        base *= 0.7

    # Seasonal factor (Delhi winter = high pollution)
    if city == 'Delhi':
        if month in [11, 12, 1]:  # Winter
            base *= 2.0
        elif month in [6, 7, 8]:  # Monsoon
            base *= 0.6

    return base

def get_traffic_congestion(area, hour, day_of_week, city='Delhi'):
    """Get traffic congestion level (0-100)"""
    base = 40

    # Rush hour effect
    if hour in [8, 9, 10]:
        base = 70
    elif hour in [17, 18, 19, 20]:
        base = 80
    elif hour in [0, 1, 2, 3, 4, 5]:
        base = 15

    # Weekend effect
    if day_of_week >= 5:
        base *= 0.7

    # Area-specific factors
    high_traffic_areas = {
        'Delhi': ['ITO', 'Connaught Place', 'Karol Bagh'],
        'Bengaluru': ['Silk Board', 'Marathahalli', 'MG Road', 'Koramangala']
    }

    if area in high_traffic_areas.get(city, []):
        base *= 1.3

    return min(base, 100)

def generate_hourly_data(city='Delhi', start_date='2024-01-01', days=365):
    """Generate hourly environmental data for a city"""
    areas = DELHI_AREAS if city == 'Delhi' else BENGALURU_AREAS

    records = []
    start = datetime.strptime(start_date, '%Y-%m-%d')

    for day_offset in range(days):
        current_date = start + timedelta(days=day_offset)
        month = current_date.month
        day_of_week = current_date.weekday()

        for hour in range(24):
            timestamp = current_date + timedelta(hours=hour)

            for area in areas:
                # AQI
                base_aqi = get_base_aqi(area, hour, month, city)
                aqi = max(20, base_aqi + np.random.normal(0, 20))

                # AQI components
                pm25 = aqi * np.random.uniform(0.8, 1.2)
                pm10 = pm25 * np.random.uniform(1.5, 2.5)
                no2 = np.random.uniform(20, 80) * (aqi / 100)
                so2 = np.random.uniform(5, 30) * (aqi / 100)

                # Traffic congestion
                traffic = get_traffic_congestion(area, hour, day_of_week, city)
                traffic = max(0, min(100, traffic + np.random.normal(0, 10)))

                # Weather
                if month in [12, 1, 2]:  # Winter
                    temp = np.random.uniform(8, 20)
                    humidity = np.random.uniform(60, 90)
                elif month in [4, 5, 6]:  # Summer
                    temp = np.random.uniform(30, 45)
                    humidity = np.random.uniform(20, 50)
                else:  # Monsoon/other
                    temp = np.random.uniform(22, 35)
                    humidity = np.random.uniform(50, 90)

                # Accident probability (higher in fog, rain, rush hour)
                accident_base = 0.02
                if hour in [8, 9, 17, 18, 19]:
                    accident_base *= 2
                if humidity > 80:  # Fog/rain
                    accident_base *= 1.5
                if traffic > 70:
                    accident_base *= 1.3

                has_accident = np.random.random() < accident_base

                # Health risk score
                health_risk = 0
                if aqi > 300:
                    health_risk = 100
                elif aqi > 200:
                    health_risk = 75
                elif aqi > 150:
                    health_risk = 50
                elif aqi > 100:
                    health_risk = 25
                else:
                    health_risk = 10

                # Adjust for vulnerable population
                if humidity < 30 or humidity > 85:
                    health_risk *= 1.2

                records.append({
                    'timestamp': timestamp,
                    'date': current_date.date(),
                    'hour': hour,
                    'day_of_week': day_of_week,
                    'month': month,
                    'city': city,
                    'area': area,
                    'aqi': round(aqi),
                    'pm25': round(pm25, 1),
                    'pm10': round(pm10, 1),
                    'no2': round(no2, 1),
                    'so2': round(so2, 1),
                    'traffic_congestion': round(traffic, 1),
                    'temperature': round(temp, 1),
                    'humidity': round(humidity, 1),
                    'has_accident': int(has_accident),
                    'health_risk_score': min(100, round(health_risk))
                })

    return pd.DataFrame(records)

def save_dataset(output_dir='../data'):
    """Generate and save datasets for Delhi and Bengaluru"""
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Delhi data (90 days)...")
    delhi_df = generate_hourly_data('Delhi', '2024-01-01', 90)
    delhi_df.to_csv(f'{output_dir}/delhi_environmental_data.csv', index=False)
    print(f"Saved: {len(delhi_df)} records")

    print("\nGenerating Bengaluru data (90 days)...")
    bengaluru_df = generate_hourly_data('Bengaluru', '2024-01-01', 90)
    bengaluru_df.to_csv(f'{output_dir}/bengaluru_environmental_data.csv', index=False)
    print(f"Saved: {len(bengaluru_df)} records")

    # Combined dataset
    combined = pd.concat([delhi_df, bengaluru_df])
    combined.to_csv(f'{output_dir}/city_environmental_data.csv', index=False)
    print(f"\nTotal records: {len(combined)}")

if __name__ == "__main__":
    save_dataset()

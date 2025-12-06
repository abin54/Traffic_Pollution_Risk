"""
Risk Modeling for Urban Traffic and Pollution
Calculates composite risk scores and identifies hotspots
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
import os

class UrbanRiskModeler:
    """Model urban health and accident risks"""

    def __init__(self):
        self.scaler = MinMaxScaler()

    def calculate_composite_risk(self, df):
        """Calculate composite risk score combining multiple factors"""
        df = df.copy()

        # Normalize individual risk factors
        risk_factors = ['aqi', 'traffic_congestion', 'humidity']
        weights = {'aqi': 0.5, 'traffic_congestion': 0.3, 'humidity': 0.2}

        # Scale factors
        for factor in risk_factors:
            df[f'{factor}_scaled'] = self.scaler.fit_transform(df[[factor]])

        # Calculate weighted composite score
        df['composite_risk'] = sum(
            df[f'{factor}_scaled'] * weight
            for factor, weight in weights.items()
        ) * 100

        # Categorize risk levels
        df['risk_level'] = pd.cut(
            df['composite_risk'],
            bins=[0, 25, 50, 75, 100],
            labels=['Low', 'Moderate', 'High', 'Severe']
        )

        return df

    def identify_hotspots(self, df, risk_threshold=70):
        """Identify high-risk areas using clustering"""
        high_risk = df[df['composite_risk'] >= risk_threshold].copy()

        if len(high_risk) == 0:
            return pd.DataFrame()

        # Group by area and calculate statistics
        hotspots = high_risk.groupby('area').agg({
            'composite_risk': ['mean', 'max', 'count'],
            'aqi': 'mean',
            'traffic_congestion': 'mean',
            'has_accident': 'sum'
        }).reset_index()

        hotspots.columns = ['area', 'avg_risk', 'max_risk', 'high_risk_hours',
                           'avg_aqi', 'avg_traffic', 'accidents']

        hotspots = hotspots.sort_values('avg_risk', ascending=False)
        hotspots['hotspot_rank'] = range(1, len(hotspots) + 1)

        return hotspots

    def calculate_hourly_pattern(self, df):
        """Calculate risk patterns by hour"""
        hourly = df.groupby('hour').agg({
            'composite_risk': 'mean',
            'aqi': 'mean',
            'traffic_congestion': 'mean',
            'has_accident': 'mean'
        }).reset_index()

        hourly['accident_rate'] = hourly['has_accident'] * 100  # Convert to percentage

        return hourly

    def calculate_daily_pattern(self, df):
        """Calculate risk patterns by day of week"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        daily = df.groupby('day_of_week').agg({
            'composite_risk': 'mean',
            'aqi': 'mean',
            'traffic_congestion': 'mean'
        }).reset_index()

        daily['day_name'] = daily['day_of_week'].map(lambda x: days[x])

        return daily


class RiskForecaster:
    """Simple risk forecasting"""

    def forecast_next_hours(self, df, area, hours=6):
        """Forecast risk for next N hours using historical patterns"""
        area_df = df[df['area'] == area].copy()

        # Get hourly averages
        hourly_avg = area_df.groupby('hour')['composite_risk'].mean()

        # Current hour
        current_hour = df['hour'].iloc[-1]

        # Forecast
        forecasts = []
        for i in range(1, hours + 1):
            future_hour = (current_hour + i) % 24
            forecast_risk = hourly_avg.get(future_hour, 50)
            forecasts.append({
                'hours_ahead': i,
                'hour': future_hour,
                'forecasted_risk': round(forecast_risk, 1)
            })

        return pd.DataFrame(forecasts)


def main():
    """Run risk modeling"""
    print("="*60)
    print("URBAN TRAFFIC & POLLUTION RISK MODELING")
    print("="*60)

    # Load data
    df = pd.read_csv('../data/city_environmental_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    print(f"Loaded {len(df)} records")
    print(f"Cities: {df['city'].unique()}")

    # Initialize modeler
    modeler = UrbanRiskModeler()

    # Calculate composite risk
    df = modeler.calculate_composite_risk(df)

    # Save processed data
    df.to_csv('../data/city_risk_scores.csv', index=False)
    print("\nSaved risk scores to ../data/city_risk_scores.csv")

    # Identify hotspots for each city
    for city in df['city'].unique():
        print(f"\n{'='*40}")
        print(f"HOTSPOTS - {city}")
        print('='*40)

        city_df = df[df['city'] == city]
        hotspots = modeler.identify_hotspots(city_df)

        if not hotspots.empty:
            print(hotspots[['hotspot_rank', 'area', 'avg_risk', 'avg_aqi', 'accidents']].head(10).to_string(index=False))

    # Hourly patterns
    print("\n" + "="*40)
    print("HOURLY RISK PATTERNS")
    print("="*40)
    hourly = modeler.calculate_hourly_pattern(df)
    print(hourly[['hour', 'composite_risk', 'aqi', 'traffic_congestion']].to_string(index=False))

if __name__ == "__main__":
    main()

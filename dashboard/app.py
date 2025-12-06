"""
Streamlit Dashboard for Urban Risk Mapping
Interactive map visualization with risk scores
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Urban Risk Map", page_icon="🗺️", layout="wide")

st.title("🗺️ Urban Traffic & Pollution Risk Map")
st.markdown("Real-time risk monitoring for Indian cities")

# Area coordinates (approximate)
AREA_COORDS = {
    'Delhi': {
        'Anand Vihar': (28.6469, 77.3164), 'ITO': (28.6289, 77.2405),
        'Punjabi Bagh': (28.6731, 77.1307), 'RK Puram': (28.5642, 77.1773),
        'Dwarka': (28.5921, 77.0460), 'Rohini': (28.7495, 77.0565),
        'Shahdara': (28.6731, 77.2890), 'Nehru Place': (28.5491, 77.2533),
        'Connaught Place': (28.6315, 77.2167), 'Karol Bagh': (28.6514, 77.1907)
    },
    'Bengaluru': {
        'Koramangala': (12.9352, 77.6245), 'Whitefield': (12.9698, 77.7499),
        'Electronic City': (12.8399, 77.6770), 'BTM Layout': (12.9166, 77.6101),
        'HSR Layout': (12.9116, 77.6389), 'Indiranagar': (12.9784, 77.6408),
        'Silk Board': (12.9173, 77.6229), 'MG Road': (12.9756, 77.6062),
        'Marathahalli': (12.9591, 77.6974), 'Hebbal': (13.0358, 77.5970)
    }
}

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('../data/city_risk_scores.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except:
        return None

df = load_data()

# Sidebar
st.sidebar.header("Settings")
if df is not None:
    city = st.sidebar.selectbox("City", df['city'].unique())
    date_filter = st.sidebar.date_input("Date", df['timestamp'].max().date())

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Risk Map", "📊 Analytics", "⚠️ Hotspots", "📈 Forecast"])

with tab1:
    st.header(f"Risk Map - {city if df is not None else 'Delhi'}")

    if df is not None:
        city_df = df[df['city'] == city]
        latest = city_df.groupby('area').last().reset_index()

        # Add coordinates
        coords = AREA_COORDS.get(city, {})
        latest['lat'] = latest['area'].map(lambda x: coords.get(x, (0, 0))[0])
        latest['lon'] = latest['area'].map(lambda x: coords.get(x, (0, 0))[1])
        latest = latest[latest['lat'] != 0]

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg AQI", f"{latest['aqi'].mean():.0f}")
        with col2:
            st.metric("Avg Traffic", f"{latest['traffic_congestion'].mean():.0f}%")
        with col3:
            st.metric("High Risk Areas", f"{len(latest[latest['composite_risk'] > 70])}")
        with col4:
            st.metric("Accidents Today", f"{city_df['has_accident'].sum()}")

        # Map
        fig = px.scatter_mapbox(
            latest,
            lat='lat', lon='lon',
            color='composite_risk',
            size='aqi',
            hover_name='area',
            hover_data=['aqi', 'traffic_congestion', 'composite_risk'],
            color_continuous_scale='RdYlGn_r',
            range_color=[0, 100],
            mapbox_style='carto-positron',
            zoom=10,
            title=f"{city} Risk Map"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Area details
        st.subheader("Area Details")
        display_cols = ['area', 'aqi', 'traffic_congestion', 'composite_risk', 'risk_level']
        st.dataframe(
            latest[display_cols].sort_values('composite_risk', ascending=False),
            use_container_width=True, hide_index=True
        )

with tab2:
    st.header("Risk Analytics")

    if df is not None:
        city_df = df[df['city'] == city]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Risk by Hour")
            hourly = city_df.groupby('hour')['composite_risk'].mean().reset_index()
            fig = px.line(hourly, x='hour', y='composite_risk', markers=True)
            fig.update_layout(xaxis_title="Hour", yaxis_title="Avg Risk Score")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("AQI vs Traffic Correlation")
            fig = px.scatter(city_df.sample(1000), x='traffic_congestion', y='aqi',
                           color='composite_risk', color_continuous_scale='RdYlGn_r')
            st.plotly_chart(fig, use_container_width=True)

        # Daily pattern
        st.subheader("Weekly Pattern")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily = city_df.groupby('day_of_week').agg({
            'composite_risk': 'mean', 'aqi': 'mean', 'traffic_congestion': 'mean'
        }).reset_index()
        daily['day'] = daily['day_of_week'].map(lambda x: days[x])

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Risk Score', x=daily['day'], y=daily['composite_risk']))
        fig.add_trace(go.Scatter(name='AQI', x=daily['day'], y=daily['aqi'], yaxis='y2'))
        fig.update_layout(
            yaxis=dict(title='Risk Score'),
            yaxis2=dict(title='AQI', overlaying='y', side='right'),
            legend=dict(x=0.1, y=1.1, orientation='h')
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Risk Hotspots")

    if df is not None:
        city_df = df[df['city'] == city]
        high_risk = city_df[city_df['composite_risk'] >= 70]

        if not high_risk.empty:
            hotspots = high_risk.groupby('area').agg({
                'composite_risk': 'mean',
                'aqi': 'mean',
                'has_accident': 'sum'
            }).reset_index()
            hotspots.columns = ['Area', 'Avg Risk', 'Avg AQI', 'Accidents']
            hotspots = hotspots.sort_values('Avg Risk', ascending=False)

            st.subheader("Top Hotspots")
            fig = px.bar(hotspots.head(10), x='Area', y='Avg Risk', color='Avg Risk',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(hotspots, use_container_width=True, hide_index=True)
        else:
            st.info("No high-risk areas currently identified")

with tab4:
    st.header("Risk Forecast")

    if df is not None:
        city_df = df[df['city'] == city]
        areas = city_df['area'].unique()

        selected_area = st.selectbox("Select Area", areas)

        if st.button("Generate 6-Hour Forecast"):
            # Simple forecast based on historical hourly averages
            area_df = city_df[city_df['area'] == selected_area]
            hourly_avg = area_df.groupby('hour')['composite_risk'].mean()

            current_hour = 12  # Simulated current hour
            forecasts = []
            for i in range(1, 7):
                h = (current_hour + i) % 24
                forecasts.append({
                    'Hours Ahead': i,
                    'Time': f"{h:02d}:00",
                    'Predicted Risk': round(hourly_avg.get(h, 50), 1)
                })

            forecast_df = pd.DataFrame(forecasts)

            st.subheader(f"6-Hour Forecast for {selected_area}")
            fig = px.line(forecast_df, x='Hours Ahead', y='Predicted Risk', markers=True)
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(forecast_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("**Urban Risk Mapping System** | Smart City Analytics | © 2024")

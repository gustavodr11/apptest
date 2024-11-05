import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Bereken het totale aantal vliegtuigen op elke luchthaven gedurende een maand
def calculate_aircraft_on_airport(selected_month):
    # Zorg ervoor dat de STD-kolom correct is geformatteerd als datetime
    df['STD'] = pd.to_datetime(df['STD'], errors='coerce')
    
    # Controleer of selected_month een pd.Timestamp object is
    if not isinstance(selected_month, pd.Timestamp):
        selected_month = pd.to_datetime(selected_month)
    
    # Filter de dataframe op vluchten binnen de geselecteerde maand
    month_filter = df['STD'].dt.to_period("M") == selected_month.to_period("M")
    month_data = df[month_filter]
    
    # Bereken de totale aankomsten en vertrekken per luchthaven gedurende de maand
    landed = month_data[month_data['LSV'] == 'L'].groupby('City')['TAR'].nunique().reset_index(name='Aantal_vliegtuigen')
    departed = month_data[month_data['LSV'] == 'S'].groupby('City')['TAR'].nunique().reset_index(name='Aantal_vertrokken')
    
    # Bereken het netto aantal vliegtuigen dat per luchthaven aanwezig was
    airport_traffic = pd.merge(landed, departed, on='City', how='outer').fillna(0)
    airport_traffic['Aantal_vliegtuigen'] = airport_traffic['Aantal_vliegtuigen'] - airport_traffic['Aantal_vertrokken']

    return airport_traffic

# Streamlit interface
st.subheader("Drukte op luchthavens in de tijd")

# Slider voor maandselectie
selected_month = st.slider("Selecteer een maand:", 
                           min_value=datetime(2019, 1, 1), 
                           max_value=datetime(2020, 12, 31), 
                           value=datetime(2019, 7, 1), 
                           format="YYYY-MM")

# Bereken het aantal vliegtuigen voor de geselecteerde maand
airport_traffic = calculate_aircraft_on_airport(selected_month)

# Bar plot weergeven
fig = px.bar(
    airport_traffic,
    x='City',
    y='Aantal_vliegtuigen',
    labels={'City': 'Luchthaven', 'Aantal_vliegtuigen': 'Aantal Vliegtuigen'},
    color='Aantal_vliegtuigen',
    color_continuous_scale=px.colors.sequential.Viridis
)

st.plotly_chart(fig)


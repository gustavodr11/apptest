import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

data = pd.read_excel("Data_verbruik_v8.xlsx")

st.subheader("Heatmap van Energieverbruik per Pand in Oostpoort Amsterdam")

df1 = pd.DataFrame(data)
df1 = df1.dropna(subset=['Latitude', 'Longitude'])

df1["Totaal verbruik per week (kWh)"] = df1[["Verbruik maandag", "Verbruik dinsdag", "Verbruik woensdag", 
                                           "Verbruik donderdag", "Verbruik vrijdag"]].sum(axis=1)

df1_grouped = df1.groupby(["pand", "Latitude", "Longitude"], as_index=False)["Totaal verbruik per week (kWh)"].sum()

map_center = [52.395762704268726, 4.789355012543267]  # Coördinaten van het midden van het terrein
m = folium.Map(location=map_center, zoom_start=15)

heat_data = [[row['Latitude'], row['Longitude'], row['Totaal verbruik per week (kWh)']] for index, row in df1_grouped.iterrows()]
HeatMap(heat_data, radius=24, max_zoom=13).add_to(m)

st_folium(m, width=700, height=500)


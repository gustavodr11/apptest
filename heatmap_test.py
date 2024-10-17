import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Laad de data
data = pd.read_excel("Data_verbruik_v7.xlsx")

# Streamlit layout
st.title("Heatmap van Energieverbruik per Pand in Oostpoort Amsterdam")

# Maak een dataframe van de data
df1 = pd.DataFrame(data)

# Filter de rijen waar latitude en longitude niet null zijn
df1 = df1.dropna(subset=['Latitude', 'Longitude'])

# Bereken het totale energieverbruik per pand over de week door de dagen bij elkaar op te tellen
df1["Totaal verbruik per week (kWh)"] = df1[["Verbruik maandag", "Verbruik dinsdag", "Verbruik woensdag", 
                                           "Verbruik donderdag", "Verbruik vrijdag"]].sum(axis=1)

# Groepeer de data op basis van Pand en coördinaat om het totale verbruik per pand te aggregeren
df1_grouped = df1.groupby(["pand", "Latitude", "Longitude"], as_index=False)["Totaal verbruik per week (kWh)"].sum()

# Maak een kaart met folium, gecentreerd op een gemiddelde locatie in Oostpoort Amsterdam
map_center = [df1_grouped["Latitude"].mean(), df1_grouped["Longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=13)

# Voeg energieverbruik toe aan de kaart als een heatmap
heat_data = [[row['Latitude'], row['Longitude'], row['Totaal verbruik per week (kWh)']] for index, row in df1_grouped.iterrows()]
HeatMap(heat_data, radius=32, max_zoom=13).add_to(m)

# Toon de heatmap in Streamlit
st_folium(m, width=700, height=500)
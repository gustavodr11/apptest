import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de data
df1 = pd.read_excel("Data_verbruik_v8.xlsx")

# Streamlit layout
st.subheader("Dagelijks Verbruik per Uur per Sector")

# Zorg ervoor dat er geen null waarden zijn in de kolommen die je nodig hebt
df1 = df1.dropna(subset=['Sector', 'Werkuren maandag', 'Verbruik maandag', 'Werkuren dinsdag', 'Verbruik dinsdag'])

# Bereken het verbruik per uur voor elke dag
df1['Verbruik per uur maandag'] = df1['Verbruik maandag'] / df1['Werkuren maandag']
df1['Verbruik per uur dinsdag'] = df1['Verbruik dinsdag'] / df1['Werkuren dinsdag']
df1['Verbruik per uur woensdag'] = df1['Verbruik woensdag'] / df1['Werkuren woensdag']
df1['Verbruik per uur donderdag'] = df1['Verbruik donderdag'] / df1['Werkuren donderdag']
df1['Verbruik per uur vrijdag'] = df1['Verbruik vrijdag'] / df1['Werkuren vrijdag']

# Zet de data in lang formaat voor Plotly
df_melted = pd.melt(df1, 
                    id_vars=['Sector'], 
                    value_vars=['Verbruik per uur maandag', 'Verbruik per uur dinsdag', 
                                'Verbruik per uur woensdag', 'Verbruik per uur donderdag', 
                                'Verbruik per uur vrijdag'], 
                    var_name='Dag', 
                    value_name='Verbruik per uur')

# Maak een lijn grafiek per sector
fig = px.line(df_melted, x='Dag', y='Verbruik per uur', color='Sector',
              title='Dagelijks Verbruik per Uur per Sector')

# Toon de grafiek in Streamlit
st.plotly_chart(fig)


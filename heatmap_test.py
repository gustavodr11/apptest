import streamlit as st
import pandas as pd
import plotly.express as px

# Fictieve data voor dagelijks, wekelijks en maandelijks energieverbruik (in kWh) per sector
data = {
    'Sector': ['Non-ferrobedrijven', 'Vervoer en opslag', 'Houtindustrie', 'Groothandel/hygiene', 
               'Voedings en genotsmiddelen', 'Auto-industrie', 'Farmaceutische industrie', 
               'Drankindustrie', 'Leidingen industrie'],
    'Maandag': [120, 85, 90, 100, 110, 95, 130, 75, 60],
    'Dinsdag': [125, 80, 85, 95, 105, 90, 125, 70, 65],
    'Woensdag': [115, 75, 95, 105, 120, 100, 135, 80, 55],
    'Donderdag': [130, 90, 100, 110, 115, 85, 140, 85, 70],
    'Vrijdag': [135, 95, 105, 115, 125, 100, 145, 90, 75],
    'Zaterdag': [140, 85, 110, 120, 130, 105, 150, 85, 80],
    'Zondag': [145, 90, 115, 125, 135, 110, 155, 95, 85],
    'Wekelijks Verbruik': [840, 595, 630, 700, 770, 665, 910, 525, 420],
    'Maandelijks Verbruik': [3600, 2550, 2700, 3000, 3300, 2850, 3900, 2250, 1800]
}

# DataFrame aanmaken
df = pd.DataFrame(data)

# Dagelijkse gegevens omzetten naar lange vorm voor gebruik in plot
df_dagelijks = df.melt(id_vars='Sector', value_vars=['Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag', 'Zondag'], 
                       var_name='Dag', value_name='Dagelijks Verbruik')

# Dropdownmenu voor selectie (dagelijks, wekelijks of maandelijks verbruik)
keuze = st.selectbox('Selecteer het type verbruik:', ['Dagelijks Verbruik', 'Wekelijks Verbruik', 'Maandelijks Verbruik'])

# Plot maken op basis van selectie
if keuze == 'Dagelijks Verbruik':
    # Lijnplot voor dagelijks verbruik
    fig = px.line(df_dagelijks, x='Dag', y='Dagelijks Verbruik', color='Sector', title=f'{keuze} per Dag per Sector', 
                  labels={'Dagelijks Verbruik': 'Verbruik (kWh)', 'Dag': 'Dag van de Week'})
else:
    # Staafdiagram voor wekelijkse of maandelijkse verbruik, met kleur per sector
    fig = px.bar(df, x='Sector', y=keuze, color='Sector', title=f'Energieverbruik per Sector ({keuze})', 
                 labels={keuze: 'Verbruik (kWh)'})

# Grafiek weergeven in Streamlit
st.plotly_chart(fig)





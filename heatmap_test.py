import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Laad de data
df = pd.read_excel("Data_verbruik_v8.xlsx")

# Functie om het stroomverbruik over de uren van de dag te verdelen op basis van de sector
def verdeel_verbruik_uren_sector(dag_verbruik, werkuren, sector, openingstijd=9):
    urenverdeling = np.zeros(24)  # Voor 24 uur op een dag

    if pd.notna(werkuren) and werkuren > 0:
        werkuren = int(werkuren)  # Zorg dat werkuren een integer is
        sluitingstijd = (openingstijd + werkuren) % 24  # Dynamische sluitingstijd

        # Definieer verbruikspatronen per sector
        if sector == 'Vervoer en opslag':
            urenverdeling[openingstijd:sluitingstijd] = (dag_verbruik * 0.7) / werkuren
            urenverdeling[sluitingstijd:openingstijd] = (dag_verbruik * 0.3) / (24 - werkuren)

        elif sector in ['Houtindustrie', 'Auto-industrie', 'Leidingen industrie']:
            urenverdeling[openingstijd:sluitingstijd] = (dag_verbruik * 0.9) / werkuren
            urenverdeling[sluitingstijd:openingstijd] = (dag_verbruik * 0.1) / (24 - werkuren)

        elif sector == 'Non-ferro metalen':
            piek_uur_start = (openingstijd + werkuren // 2 - 2) % 24  # Piek midden op de werkdag
            piek_uur_eind = (piek_uur_start + 4) % 24
            urenverdeling[openingstijd:piek_uur_start] = (dag_verbruik * 0.15) / (piek_uur_start - openingstijd)
            urenverdeling[piek_uur_start:piek_uur_eind] = (dag_verbruik * 0.7) / 4
            urenverdeling[piek_uur_eind:sluitingstijd] = (dag_verbruik * 0.15) / (sluitingstijd - piek_uur_eind)
            urenverdeling[sluitingstijd:openingstijd] = 0  # Geen verbruik 's nachts

        elif sector == 'Groothandel/hygiene':
            piek_uur = min(sluitingstijd, openingstijd + 6)
            urenverdeling[openingstijd:piek_uur] = (dag_verbruik * 0.5) / (piek_uur - openingstijd)
            urenverdeling[piek_uur:sluitingstijd] = (dag_verbruik * 0.5) / (sluitingstijd - piek_uur)
            urenverdeling[sluitingstijd:openingstijd] = 0  # Geen verbruik 's nachts

        elif sector == 'Voedings en genotsmiddelen':
            urenverdeling[openingstijd:sluitingstijd] = (dag_verbruik * 0.9) / werkuren
            urenverdeling[sluitingstijd:openingstijd] = (dag_verbruik * 0.1) / (24 - werkuren)

        elif sector in ['Media', 'Farmaceutische industrie']:
            urenverdeling[:] = dag_verbruik / 24

        elif sector == 'Drankindustrie':
            piek_uur_start = max(sluitingstijd - 5, openingstijd)
            urenverdeling[openingstijd:piek_uur_start] = (dag_verbruik * 0.5) / (piek_uur_start - openingstijd)
            urenverdeling[piek_uur_start:sluitingstijd] = (dag_verbruik * 0.5) / (sluitingstijd - piek_uur_start)
            urenverdeling[sluitingstijd:openingstijd] = 0  # Geen verbruik 's nachts

    return urenverdeling

# Initializeer een dictionary voor het verbruik per sector per uur
sector_uurverbruik = {sector: np.zeros(24) for sector in df['Sector'].unique()}

# Loop door de bedrijven en bereken het stroomverbruik per uur
for index, row in df.iterrows():
    werkuren_per_dag = {
        'maandag': row['Werkuren maandag'],
        'dinsdag': row['Werkuren dinsdag'],
        'woensdag': row['Werkuren woensdag'],
        'donderdag': row['Werkuren donderdag'],
        'vrijdag': row['Werkuren vrijdag'],
        'zaterdag': row['Werkuren zaterdag'],
        'zondag': row['Werkuren zondag']
    }
    
    verbruik_per_dag = {
        'maandag': row['Verbruik maandag'],
        'dinsdag': row['Verbruik dinsdag'],
        'woensdag': row['Verbruik woensdag'],
        'donderdag': row['Verbruik donderdag'],
        'vrijdag': row['Verbruik vrijdag'],
        'zaterdag': row['Verbruik zaterdag'],
        'zondag': row['Verbruik zondag']
    }
    
    sector = row['Sector']  # Haal de sector van het bedrijf op
    openingstijd = 9  # Je kunt dit eventueel dynamisch per bedrijf bepalen als dit in je dataset staat

    # Verdeel het verbruik voor elke dag over de uren
    for dag in werkuren_per_dag.keys():
        werkuren = werkuren_per_dag[dag]
        dag_verbruik = verbruik_per_dag[dag]
        uurverdeling = verdeel_verbruik_uren_sector(dag_verbruik, werkuren, sector, openingstijd)
        
        # Voeg het verbruik per uur toe aan de totale verdeling voor de sector
        sector_uurverbruik[sector] += uurverdeling

# Zet de data in een geschikt formaat voor Plotly
uren = list(range(24))
verbruik_data = []

for sector, uurverbruik in sector_uurverbruik.items():
    for uur, verbruik in zip(uren, uurverbruik):
        verbruik_data.append({'Sector': sector, 'Uur': uur, 'Stroomverbruik (kWh)': verbruik})

df_plot = pd.DataFrame(verbruik_data)

# Plot met Plotly
fig = px.line(df_plot, x='Uur', y='Stroomverbruik (kWh)', color='Sector', title='Dagverdeling van Stroomverbruik per Sector')

# Toon de grafiek in Streamlit
st.plotly_chart(fig)



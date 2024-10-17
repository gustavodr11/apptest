import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Functie voor het toewijzen van verbruikspatronen aan sectoren
def verdeel_verbruik_uren(dag_verbruik, werkuren, patroon, openingstijd=9):
    urenverdeling = np.zeros(24)
    if pd.notna(werkuren) and werkuren > 0:
        werkuren = int(werkuren)
        sluitingstijd = (openingstijd + werkuren) % 24

        # Algemene verdeling op basis van patroon
        if len(patroon) == 2:
            urenverdeling[openingstijd:sluitingstijd] = (dag_verbruik * patroon[0]) / werkuren
            urenverdeling[sluitingstijd:openingstijd] = (dag_verbruik * patroon[1]) / (24 - werkuren)
        elif len(patroon) == 3:
            piek_uur_start = (openingstijd + werkuren // 2 - 2) % 24
            piek_uur_eind = (piek_uur_start + 4) % 24
            urenverdeling[openingstijd:piek_uur_start] = (dag_verbruik * patroon[0]) / (piek_uur_start - openingstijd)
            urenverdeling[piek_uur_start:piek_uur_eind] = (dag_verbruik * patroon[1]) / 4
            urenverdeling[piek_uur_eind:sluitingstijd] = (dag_verbruik * patroon[2]) / (sluitingstijd - piek_uur_eind)
    return urenverdeling

# Verbruikspatronen voor sectoren
sector_patronen = {
    'Vervoer en opslag': (0.7, 0.3),
    'Houtindustrie': (0.9, 0.1),
    'Non-ferrobedrijven': (0.9, 0.1),
    'Groothandel/hygiene': (0.5, 0.5),
    'Voedings en genotsmiddelen': (0.9, 0.1),
    'Farmaceutische industrie': (1, 0),
    'Drank industrie': (0.5, 0.5),
    'Auto-industrie': (0.9, 0.1),
    'Leidingen industrie': (0.9, 0.1)
}

# Lees de data in
df = pd.read_excel("Data_verbruik_v8.xlsx")

# Initializeer een dictionary voor het verbruik per sector per uur
sector_uurverbruik = {sector: np.zeros(24) for sector in df['Sector'].unique()}

# Verdeel het verbruik over de uren van de dag per sector
for _, row in df.iterrows():
    werkuren_per_dag = row[['Werkuren maandag', 'Werkuren dinsdag', 'Werkuren woensdag', 
                            'Werkuren donderdag', 'Werkuren vrijdag', 'Werkuren zaterdag', 
                            'Werkuren zondag']]

    verbruik_per_dag = row[['Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 
                            'Verbruik donderdag', 'Verbruik vrijdag', 'Verbruik zaterdag', 
                            'Verbruik zondag']]

    sector = row['Sector']
    patroon = sector_patronen.get(sector, (0.9, 0.1))  # Val terug op een standaard patroon

    # Bereken het verbruik per uur voor elke dag
    for werkuren, dag_verbruik in zip(werkuren_per_dag, verbruik_per_dag):
        sector_uurverbruik[sector] += verdeel_verbruik_uren(dag_verbruik, werkuren, patroon)

# Streamlit weergave met Matplotlib
st.title('Dagverdeling van Stroomverbruik per Sector')

plt.figure(figsize=(12, 8))
for sector, uurverbruik in sector_uurverbruik.items():
    plt.plot(range(24), uurverbruik, marker='o', label=sector)

plt.title('Dagverdeling van Stroomverbruik per Sector')
plt.xlabel('Uur van de Dag')
plt.ylabel('Totaal Stroomverbruik (kWh)')
plt.xticks(range(24), [f'{i}:00' for i in range(24)], rotation=45)
plt.legend(title='Sectoren', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

st.pyplot(plt)




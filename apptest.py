

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Titel van de app
st.title("Interactieve Plotly Grafieken met Streamlit")

# Beschrijving
st.markdown("""
Deze applicatie genereert willekeurige data en toont interactieve Plotly-grafieken.
Gebruik de dropdown-menu's om de weergegeven variabelen te selecteren.
""")

# Sidebar voor instellingen
st.sidebar.header("Instellingen")

# Opties voor datageneratie
num_points = st.sidebar.slider("Aantal datapunten", min_value=50, max_value=1000, value=200, step=50)

# Genereren van willekeurige data
np.random.seed(42)  # Voor reproduceerbaarheid
df = pd.DataFrame({
    'Datum': pd.date_range(start='2023-01-01', periods=num_points, freq='D'),
    'Categorie': np.random.choice(['A', 'B', 'C', 'D'], size=num_points),
    'Waarde 1': np.random.randn(num_points).cumsum(),
    'Waarde 2': np.random.randn(num_points).cumsum(),
    'Waarde 3': np.random.randn(num_points).cumsum()
})

# Toon de dataset
st.subheader("Willekeurige Dataset")
st.dataframe(df)

# Dropdown-menu voor het selecteren van de y-as variabele
y_axis = st.selectbox(
    "Selecteer de variabele voor de Y-as",
    options=['Waarde 1', 'Waarde 2', 'Waarde 3'],
    index=0
)

# Dropdown-menu voor het selecteren van de categoriegroep
category = st.selectbox(
    "Selecteer de categorie om te groeperen",
    options=['Categorie', None],
    index=0
)

# Maak een Plotly-lijn grafiek
if category:
    fig = px.line(
        df, 
        x='Datum', 
        y=y_axis, 
        color=category,
        title=f"Lijn Grafiek van {y_axis} per {category}"
    )
else:
    fig = px.line(
        df, 
        x='Datum', 
        y=y_axis, 
        title=f"Lijn Grafiek van {y_axis}"
    )

# Interactieve dropdown binnen de Plotly-grafiek
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Lijn",
                     method="restyle",
                     args=["type", "scatter"]),
                dict(label="Stap",
                     method="restyle",
                     args=["type", "step"],
                     ),
                dict(label="Bar",
                     method="restyle",
                     args=["type", "bar"])
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.0,
            xanchor="left",
            y=1.15,
            yanchor="top"
        ),
    ]
)

# Toon de grafiek
st.plotly_chart(fig, use_container_width=True)

# Extra: Staafdiagram als tweede plot
st.subheader("Staafdiagram van Gemiddelde Waarden per Categorie")

# Bereken gemiddelde per categorie
df_avg = df.groupby('Categorie')[['Waarde 1', 'Waarde 2', 'Waarde 3']].mean().reset_index()

# Dropdown-menu voor het selecteren van de gemiddelde variabele
avg_variable = st.selectbox(
    "Selecteer de variabele voor de gemiddelde staafdiagram",
    options=['Waarde 1', 'Waarde 2', 'Waarde 3'],
    index=0
)

# Maak een Plotly staafdiagram
bar_fig = px.bar(
    df_avg,
    x='Categorie',
    y=avg_variable,
    title=f"Gemiddelde van {avg_variable} per Categorie",
    labels={avg_variable: f"Gemiddelde {avg_variable}"}
)

# Toon de staafdiagram
st.plotly_chart(bar_fig, use_container_width=True)

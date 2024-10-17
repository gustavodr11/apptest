import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de data
data = pd.read_excel("Data_verbruik_v8.xlsx")

# Streamlit layout
st.title("Dagverdeling van Stroomverbruik per Sector")

# Maak een dataframe van de data
df1 = pd.DataFrame(data)

# Zorg ervoor dat er geen null waarden zijn in de kolommen die je nodig hebt
df1 = df1.dropna(subset=['Sector', 'Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 'Verbruik donderdag', 'Verbruik vrijdag'])

# Zet de data in lang formaat voor Plotly (dagverdeling)
df_melted = pd.melt(df1, 
                    id_vars=['Sector'], 
                    value_vars=['Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 
                                'Verbruik donderdag', 'Verbruik vrijdag'], 
                    var_name='Dag', 
                    value_name='Stroomverbruik (kWh)')

# Maak een lijn grafiek per sector voor de dagverdeling van stroomverbruik
fig = px.line(df_melted, x='Dag', y='Stroomverbruik (kWh)', color='Sector',
              title='Dagverdeling van Stroomverbruik per Sector')

# Toon de grafiek in Streamlit
st.plotly_chart(fig)



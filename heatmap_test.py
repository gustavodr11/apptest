import pandas as pd
import plotly.express as px
import streamlit as st

# Lees de data in
df1 = pd.read_excel("Data_verbruik_v8.xlsx")

# Selecteer alleen de relevante kolommen
df_verbruik = df1[['Sector', 'Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 
                   'Verbruik donderdag', 'Verbruik vrijdag', 'Verbruik zaterdag', 'Verbruik zondag']]

# Smelt de data om dagen in rijen te krijgen
df_melted = df_verbruik.melt(id_vars=['Sector'], 
                             var_name='Dag', 
                             value_name='Verbruik (kWh)')

# Maak een lijn grafiek met Plotly
fig = px.line(df_melted, 
              x='Dag', 
              y='Verbruik (kWh)', 
              color='Sector',
              title='Dagelijks energieverbruik per sector')

# Weergeef de grafiek in Streamlit
st.plotly_chart(fig)



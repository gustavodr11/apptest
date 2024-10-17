import streamlit as st
import pandas as pd
import plotly.express as px


    df2 = pd.read_excel('Data_verbruik_v8.xlsx')

    # Kolomnamen specificeren die je wilt gebruiken
    sector_col = 'Sector'
    daily_columns = ['Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 'Verbruik donderdag', 'Verbruik vrijdag', 'Verbruik zaterdag', 'Verbruik zondag']
    weekly_col = 'Week verbruik'
    monthly_col = 'Maand verbruik)'

    # Dagelijkse gegevens omzetten naar lange vorm voor gebruik in plot
    df_dagelijks = df2.melt(id_vars=sector_col, value_vars=daily_columns, 
                            var_name='Dag', value_name='Dagelijks Verbruik')

    # Dropdownmenu voor selectie (dagelijks, wekelijks of maandelijks verbruik)
    keuze = st.selectbox('Selecteer het type verbruik:', ['Dagelijks Verbruik', weekly_col, monthly_col])

    # Maak de visualisatie op basis van de kolomkeuze
    if keuze == 'Dagelijks Verbruik':
        # Lijnplot voor dagelijks verbruik
        fig = px.line(df_dagelijks, x='Dag', y='Dagelijks Verbruik', color=sector_col, 
                      title=f'{keuze} per dag per sector', 
                      labels={'Dagelijks Verbruik': 'Verbruik (kWh)', 'Dag': 'Dag van de week'})
    else:
        # Staafdiagram voor wekelijkse of maandelijkse verbruik
        fig = px.bar(df2, x=sector_col, y=keuze, color=sector_col, 
                     title=f'Energieverbruik per sector ({keuze})', 
                     labels={keuze: 'Verbruik (kWh)'})

    # Grafiek weergeven in Streamlit
    st.plotly_chart(fig)





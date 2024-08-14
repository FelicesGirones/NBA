# -----------------------------------------LIBRERÍAS----------------------------------------------#

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# -------------------------------------------DATOS------------------------------------------------#

df_player_stats = pd.read_csv(r'C:\Users\sfeli\Documents\Upgradehub\DATA\NBA\Datasets\player_stats.csv')
df_team_stats= pd.read_csv(r'C:\Users\sfeli\Documents\Upgradehub\DATA\NBA\Datasets\team_stats.csv')

# -------------------------------------------ARIMA------------------------------------------------#

model_path = '\ARIMA_models'

# -----------------------------------CONFIGURACIÓN DE LA PÁGINA-----------------------------------#

css = """
<style>
body {
    font-family: 'Arial Black', sans-serif;
}
</style>
"""

html_content = f"""
<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
    <h1 style='color: #3366FF; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-size: 48px;'>
        Regular Season
    </h1>
</div>
"""

def display():
    st.markdown(css, unsafe_allow_html=True)  
    st.markdown(html_content, unsafe_allow_html=True)

    # ---------------------------------------------TABS------------------------------------------------#
    tab1, tab2, tab3, = st.tabs(
        [   'Offensive and defensive statistics',
            'Total Points Forecast',
            'Player Stats'])    

    # -----------------------------TAB1-----------------------------#
    with tab1:
        st.subheader('Discover the evolution of offensive and defensive statistics between 2013 and 2023')
        with st.expander('Offensive statistics'):
            
            #Realizamos la suma y media de las variables de las variables ofensivas por temporada
            season_stats = df_player_stats.groupby('Season').agg({
            '3P': 'sum','3PA': 'sum','3P%': 'mean','2P': 'sum','2PA': 'sum','2P%': 'mean','FT': 'sum','FTA': 'sum','FT%': 'mean','ORB': 'sum','AST': 'sum'}).reset_index()

            #Filtros de visualización para estadísticas ofensivas
            opciones = ['2P', '3P', 'FT', 'ORB', 'AST']
            seleccion = st.selectbox('Choose an offensive statistic:',opciones)

            if seleccion == '2P':
                metricas = ['2P', '2PA', '2P%']
            elif seleccion == '3P':
                metricas = ['3P', '3PA', '3P%']
            elif seleccion == 'FT':
                metricas = ['FT', 'FTA', 'FT%']
            else:
                metricas = [seleccion]

            #Crearmos y mostramos el primer gráfico (líneas) para estadísticas ofensivas
            fig = go.Figure()

            for metrica in metricas:
                if metrica in ['2P', '2PA', '3P', '3PA', 'FT', 'FTA', 'ORB', 'AST']:
                    fig.add_trace(go.Scatter(x=season_stats['Season'], y=season_stats[metrica], mode='lines+markers', name=f'{metrica}', line=dict(color='blue')))
                elif metrica in ['2P%', '3P%', 'FT%']:
                    fig.add_trace(go.Scatter(x=season_stats['Season'], y=season_stats[metrica] * 100, mode='lines+markers', name=f'{metrica}', line=dict(color='orange'), yaxis='y2'))

            fig.update_layout(
                title=f'Evolution of {seleccion} per season',
                xaxis=dict(
                    title='',
                    showline=False,
                    showgrid=False,
                    zeroline=False,
                    tickmode='linear',
                    tickvals=season_stats['Season'],),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    zeroline=False,),
                yaxis2=dict(
                    title='Percentages (%)',
                    overlaying='y',
                    side='right',
                    showline=False,
                    showgrid=False,
                    zeroline=False,),
                template='plotly_dark',
                showlegend=True)

            st.plotly_chart(fig)

            #Crearmos y mostramos el segundo gráfico (dispersión) para estadísticas ofensivas
            if seleccion in ['2P', '3P', 'FT', 'ORB', 'AST']:
                max_stats = df_player_stats.loc[df_player_stats.groupby('Season')[seleccion].idxmax()]
                
                scatter_fig = px.scatter(
                    max_stats,
                    x='Season',
                    y=seleccion,
                    size=seleccion,
                    color=seleccion,
                    text='Player',
                    title=f'Player with the highest {seleccion} per Season',
                    labels={'Season': 'Temporada', seleccion: seleccion},
                    size_max=60,
                    color_continuous_scale=px.colors.sequential.Viridis,
                    template='plotly_dark')

                scatter_fig.update_layout(
                    xaxis=dict(
                        title='',
                        showline=False,
                        showgrid=False,
                        zeroline=False,
                        tickmode='linear',
                        tickvals=max_stats['Season'],),
                    yaxis=dict(
                        title='',
                        showline=False,
                        showgrid=False,
                        zeroline=False,),
                    template='plotly_dark')

                st.plotly_chart(scatter_fig)   
                
        with st.expander('Defensive statistics'):
            
    #Realizamos la suma de las variables defensivas por temporada
            season_stats_defensive = df_player_stats.groupby('Season').agg({'DRB': 'sum', 'STL': 'sum', 'BLK': 'sum', 'PF': 'sum'}).reset_index()

            #Filtros de visualización para estadísticas defensivas
            opciones_defensivas = ['DRB', 'STL', 'BLK', 'PF']
            seleccion_defensiva = st.selectbox('Choose an offensive defensive:', opciones_defensivas)

            #Creamos y mostramos el gráfico (líneas) para estadísticas defensivas
            fig_defensivo = go.Figure()

            fig_defensivo.add_trace(go.Scatter(x=season_stats_defensive['Season'], 
                                            y=season_stats_defensive[seleccion_defensiva], 
                                            mode='lines+markers', 
                                            name=f'{seleccion_defensiva}', 
                                            line=dict(color='blue')))

            fig_defensivo.update_layout(
                title=f'Evolution of {seleccion_defensiva} per season',
                xaxis=dict(
                    title='',
                    showline=False,
                    showgrid=False,
                    zeroline=False,
                    tickmode='linear',
                    tickvals=season_stats_defensive['Season']),
                yaxis=dict(
                    showline=False,
                    showgrid=False,
                    zeroline=False),
                template='plotly_dark',
                showlegend=True)

            st.plotly_chart(fig_defensivo)

            #Creamos y mostramos el segundo gráfico (dispersión) para estadísticas defensivas
            max_stats_defensivas = df_player_stats.loc[df_player_stats.groupby('Season')[seleccion_defensiva].idxmax()]

            scatter_fig_defensivo = px.scatter(
                max_stats_defensivas,
                x='Season',
                y=seleccion_defensiva,
                size=seleccion_defensiva,
                color=seleccion_defensiva,
                text='Player',
                title=f'Player with the highest {seleccion_defensiva} per season',
                labels={'Season': 'Temporada', seleccion_defensiva: seleccion_defensiva},
                size_max=60,
                color_continuous_scale=px.colors.sequential.Viridis,
                template='plotly_dark')

            scatter_fig_defensivo.update_layout(
                xaxis=dict(
                    title='',
                    showline=False,
                    showgrid=False,
                    zeroline=False,
                    tickmode='linear',
                    tickvals=max_stats_defensivas['Season']),
                yaxis=dict(
                    title='',
                    showline=False,
                    showgrid=False,
                    zeroline=False),
                template='plotly_dark')

            st.plotly_chart(scatter_fig_defensivo)                             
    # -----------------------------TAB2-----------------------------#
    with tab2:
        st.subheader('Total Wins Forecast')

        #Función ARIMA
        def arima_forecast(model_fit, future_years):
            forecast = model_fit.forecast(steps=len(future_years))
            future_df = pd.DataFrame({
                'Año': future_years,
                'Predicción': forecast})
            return future_df
        
        #Definimos el rango de años futuros
        future_years = np.arange(2024, 2030)

        #Listamos los equipos del Este y creamos filtros para seleccionar la conferencia y los equipos
        teams_east = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DET', 'IND', 'MIA', 'MIL', 'NYK', 'ORL', 'PHI', 'TOR', 'WAS']
        teams_west = ['DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MEM', 'MIN', 'NOH', 'OKC', 'PHO', 'POR', 'SAC', 'SAS', 'UTA']

        conference = st.radio('', ('Eastern Conference', 'Western Conference'))

        if conference == 'Eastern Conference':
            team_options = ['Select a team'] + teams_east
        else:
            team_options = ['Select a team'] + teams_west
        
        team_selected = st.selectbox('', options=team_options)
        
        if team_selected != 'Select a team':
            model_file = os.path.join(model_path, f'model_{team_selected}.pkl')

            if os.path.exists(model_file):
                
                model_fit = joblib.load(model_file) #Cargamos el modelo ARIMA para el equipo seleccionado
                future_df = arima_forecast(model_fit, future_years)

                #Creamos el gráfico
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=future_df['Año'],
                    y=future_df['Predicción'],
                    mode='lines',
                    line=dict(color='orange'),
                    name=f'Predicción {team_selected}'))
                fig.update_layout(
                    title=f'Future Wins in the Regular Season for {team_selected}',
                    xaxis_title='Year',
                    yaxis_title='Predicted Wins',
                    template='plotly_dark')
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False)

                st.plotly_chart(fig)
    # -----------------------------TAB3-----------------------------#
    with tab3:        
        st.subheader('Navigate through the players statistics between 2013 and 2023')
        
        #Definimos la función para dibujar la cancha
        def dibujar_cancha(ax=None, lw=2, lineas_exteriores=False):
            if ax is None:
                ax = plt.gca()

            aro = Circle((0, 0), radius=7.5, linewidth=lw, color='#FFFFFF', fill=False)
            tablero = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color='#FFFFFF')
            caja_exterior = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color='#FFFFFF', fill=False)
            caja_interior = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color='#FFFFFF', fill=False)
            arco_tiro_libre_superior = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color='#FFFFFF', fill=False)
            arco_tiro_libre_inferior = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color='#FFFFFF', linestyle='dashed')
            zona_restringida = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color='#FFFFFF')
            esquina_tres_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color='#FFFFFF')
            esquina_tres_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color='#FFFFFF')
            arco_tres_puntos = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color='#FFFFFF')
            arco_central_exterior = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color='#FFFFFF')
            arco_central_interior = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color='#FFFFFF')

            elementos_cancha = [aro, tablero, caja_exterior, caja_interior, arco_tiro_libre_superior, arco_tiro_libre_inferior, zona_restringida, esquina_tres_a, esquina_tres_b, arco_tres_puntos, arco_central_exterior, arco_central_interior]

            if lineas_exteriores:
                lineas_exteriores = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color='#FFFFFF', fill=False)
                elementos_cancha.append(lineas_exteriores)

            for element in elementos_cancha:
                ax.add_patch(element)
            return ax

        #Convertimos el % en porcentajes y redondeamos valores
        def convertir_porcentaje(porcentaje):
            return int(porcentaje * 100)
        def redondear(valor):
            return int(round(valor))

        #Agregamos marcadores en la cancha y definimos las posiciones en el campo
        def agregar_marcadores(ax, stats):
            posiciones = {
                '3P': (0, 265),
                '2P': (150, 0),
                'FT': (0, 170),
                'PTS': (180, 350),}
            
            if show_player_info:
                posiciones.update({
                    'Pos': (180, 340),
                    'Age': (180, 330),
                    'G': (180, 320),
                    'MP': (180, 310),})
                
            for key, (x, y) in posiciones.items():
                if key in ['3P', '2P', 'FT']:
                    texto = f"{key}: {stats[key]}\n{key}A: {stats[f'{key}A']}\n{key}%: {convertir_porcentaje(stats[f'{key}%'])}%"
                    color = '#FF6600'
                elif key == 'PTS':
                    texto = f"{key}: {stats[key]}"
                    color = '#3366FF'
                elif key in ['Pos', 'Age', 'G', 'MP']:
                    texto = f"{key}: {stats[key]}"
                    color = '#00CC99'
                
                ax.text(x, y, texto, color=color, ha='center', va='center', fontsize=12, weight='bold', bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.5'))

        #Filtros de visualización
        season = st.selectbox('Select the season', df_player_stats['Season'].unique())
        df_season = df_player_stats[df_player_stats['Season'] == season]

        if st.checkbox('Click to search by player'):
            player = st.selectbox('Select one player', df_season['Player'].unique())
            filtered_data = df_season[df_season['Player'] == player].iloc[0]
            show_player_info = True
        else:
            df_season_numeric = df_season.drop(columns=['Player', 'Season'])
            mean_values = df_season_numeric.mean(numeric_only=True).round(2)
            filtered_data = mean_values
            show_player_info = False

        #Crearmos y mostramos el gráfico
        fig, ax = plt.subplots(figsize=(12, 11))
        fig.patch.set_facecolor('black')
        dibujar_cancha(ax, lw=3, lineas_exteriores=True)
        agregar_marcadores(ax, filtered_data)
        ax.set_xlim(-250, 250)
        ax.set_ylim(-50, 450)
        ax.axis('off')

        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.subheader("Offensive Statistics")
            st.write(f"ORB: {redondear(filtered_data['ORB'])}")
            st.write(f"AST: {redondear(filtered_data['AST'])}")
            st.write(f"OWS: {redondear(filtered_data['OWS'])}")

        with col2:
            st.pyplot(fig)

        with col3:
            st.subheader("Defensive Statistics")
            st.write(f"DRB: {redondear(filtered_data['DRB'])}")
            st.write(f"STL: {redondear(filtered_data['STL'])}")
            st.write(f"BLK: {redondear(filtered_data['BLK'])}")
            st.write(f"TOV: {redondear(filtered_data['TOV'])}")
            st.write(f"PF: {redondear(filtered_data['PF'])}")
            st.write(f"DWS: {redondear(filtered_data['DWS'])}")

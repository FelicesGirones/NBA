# -----------------------------------------LIBRERÍAS----------------------------------------------#

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------DATOS------------------------------------------------#

df_draft = pd.read_csv(r'/Datasets/draft_picks.csv')
df_top_20_pick = pd.read_csv(r'/Datasets/top_20_pick.csv')
df_pick = pd.read_csv(r'/Datasets/df_pick.csv')

# ----------------------------------------IMAGENES------------------------------------------------#

img_2= '\img\draft.jpg'

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
        Draft
    </h1>
</div>
"""

def display():
    st.markdown(css, unsafe_allow_html=True)  
    st.markdown(html_content, unsafe_allow_html=True) 


    # ---------------------------------------------TABS------------------------------------------------#
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [   'What is the NBA draft?',
            'The First Pick',
            'Evolution of the draft by teams',
            'Picks by team',
            'USA Colleges vs World'])    

    # -----------------------------TAB1-----------------------------#
    with tab1:
        st.header('What is the NBA draft?')
        col1, col2 = st.columns(2) 
        
        with col1:
            
            st.write('It is the process of player selection by franchises that seeks to reduce the level differences between the teams, taking into account the ranking from the previous year in the selection order.')
            st.write('The worse the ranking, the more chances of getting to choose first. Through this mechanism, the 30 franchises select a total of 60 players who come from teams of American universities or leagues from the rest of the world.')
            st.write('The system starts from a very clear premise: the worst teams from the previous campaign have a higher probability of choosing earlier in the Draft, thus being able to choose the most promising players.')
            st.write('However, the rules are more complex with the aim of avoiding tanking (losing on purpose to increase the chances of choosing higher up)')
       
        with col2:
             st.image(img_2, width=500, caption='Sports Illustrated', use_column_width=True)             
    # -----------------------------TAB2-----------------------------#
    with tab2:
        st.write('Discover who has taken the fist pick since 1961')
        with st.expander('By teams'):
                       
            #Filtramos por el primer Pick y hacemos el conteo por equipo
            numero_1_draft = df_draft[df_draft['Pick'] == 1]
            conteo_equipos = numero_1_draft['Team'].value_counts()

            #Creamos el DataFrame
            conteo_equipos_df = pd.DataFrame({'Equipo': conteo_equipos.index, 'Número de veces': conteo_equipos.values})

            #Paleta de colores
            color_palette = px.colors.sequential.Viridis

            #Creamos el gráfico
            fig = px.bar(conteo_equipos_df, 
                        x='Equipo', 
                        y='Número de veces', 
                        title='',
                        labels={'Equipo': 'Team', 'Número de veces': 'Number of times'},
                        color='Número de veces',
                        color_continuous_scale=color_palette,
                        template='plotly_dark')

            #Configuramos el gráfico
            fig.update_traces(marker_line_width=0, marker_line_color='black')
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)
            fig.update_layout(yaxis_title='', xaxis_title='')
            fig.update_layout(coloraxis_colorbar=dict(title='', tickvals=[]), showlegend=False)

            #Mostramos el gráfico
            st.plotly_chart(fig)
    
        with st.expander('By Colleges'):
                       
            #Filtramos por el primer Pick excluyendo los jugadores de fuera de USA y hacemos el conteo por equipo mostrando el top 30
            numero_1_draft = df_draft[(df_draft['Pick'] == 1) & (df_draft['College'] != 'Out US')]
            conteo_colleges = numero_1_draft['College'].value_counts().nlargest(30)

            #Creamos el DataFrame
            top_colleges_df = pd.DataFrame({'College': conteo_colleges.index, 'Número de veces': conteo_colleges.values})

            #Paleta de colores
            color_palette = px.colors.sequential.Viridis

            #Creamos el gráfico
            fig = px.bar(top_colleges_df, 
                        x='College', 
                        y='Número de veces', 
                        title='',
                        labels={'College': 'College', 'Número de veces': 'Number of times'},
                        color='Número de veces',
                        color_continuous_scale=color_palette,
                        template='plotly_dark')

            #Configuramos el gráfico
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)
            fig.update_layout(yaxis_title='', xaxis_title='')
            fig.update_xaxes(tickangle=45, tickmode='array')

            #Mostramos el gráfico
            st.plotly_chart(fig)                     
    # -----------------------------TAB3-----------------------------#
    with tab3:
    
        st.write('Select one or more teams to explore the evolution. This will represent the Win Share generated during the regular seasons, place your cursor on the graph to discover the players and some relevant statistics.')

        #Botones para seleccionar equipo
        if 'selected_teams' not in st.session_state:
            st.session_state.selected_teams = []
        if st.button('Reset selections'):
            st.session_state.selected_teams = []
        teams = df_draft['Team'].unique().tolist()
        cols = st.columns(10)

        for index, team in enumerate(teams):
            col = cols[index % 10]
            
            if col.button(team, key=team):
                if team not in st.session_state.selected_teams:
                    st.session_state.selected_teams.append(team)
                else:
                    st.session_state.selected_teams.remove(team)

        #Filtramos el DataFrame según la selección
        filtered_df = df_draft[df_draft['Team'].isin(st.session_state.selected_teams)]

        #Creamos el gráfico
        if st.session_state.selected_teams and not filtered_df.empty:
            fig = px.line(filtered_df, 
                        x='Year', 
                        y='WS',
                        color='Team',
                        hover_name=filtered_df['Player'],
                        hover_data={
                            'Year': True,
                            'Minutes Played per game': True,
                            'PTS per game': True,
                            'TBR per game': True,
                            'Pick': True,
                            'AST per game': True
                        },
                        labels={'Year': 'Year', 'WS': 'Wins Shares'},
                        title='',
                        template='plotly_dark')

            #Configuramos el gráfico
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(range=[0, None], showticklabels=False)

            #Mostramos el gráfico
            st.plotly_chart(fig)
        else:
            st.write('Select at least one Team to display the statistics')        
    # -----------------------------TAB4-----------------------------#
    with tab4:
        st.write('Select one or more picks to see the average team statistics based on the draft choice. Select your favorite statistic to know if the average of the team’s choices is above or below their competitors.') 

        #Selector
        pick_numbers = st.multiselect("Select Draft Picks:", options=["Resetore"] + list(df_pick['Pick'].unique()))

        if "Resetore" not in pick_numbers and pick_numbers:
            filtered_data = df_pick[df_pick['Pick'].isin(pick_numbers)]

            #Transformamos los datos
            melted_data = filtered_data.melt(id_vars='Team', value_vars=['PTS per game', 'TBR per game', 'AST per game'])

            #Creamos el gráfico
            fig = px.bar(melted_data, x='Team', y='value', color='variable',
                        color_discrete_map={
                            'PTS per game': '#1f77b4',
                            'TBR per game': '#ff7f0e',
                            'AST per game': '#2ca02c'   
                        },
                        title='',
                        labels={'value': 'Valor', 'variable': ''})

            #Configuramos el gráfico
            fig.update_layout(yaxis_title='', xaxis_title='')
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)

            #Mostramos el gráfico
            st.plotly_chart(fig)
        else:
            st.write('Select at least one Pick to display the statistics')            
    # -----------------------------TAB5-----------------------------#
    with tab5:
        st.write('In this section, we will propose a hypothesis based on players drafted in the top 20 positions, as they should be the best players from their promotion. We will consider per-game metrics for a better comparison of the data, making it possible to compare new rookies with experienced veteran players.')
        st.markdown("<p style='font-size:20px; color:#3366FF;'><strong>Null Hypothesis</strong></p>",unsafe_allow_html=True)
        st.write('There is no difference in performance metrics between players who have attended American Colleges and those from universities outside the USA.')
        st.markdown("<p style='font-size:20px; color:#FF6600;'><strong>Alternative Hypothesis</strong></p>",unsafe_allow_html=True)
        st.write('Players from American universities have better performance metrics than the rest.')
        
        with st.expander('Click on the drop-down menu to view the data distribution', expanded=False):
            
            #Renombramos las columnas
            df_top_20_pick.rename(columns={
                'WS': 'Win Shares',
                'PTS per game': 'Points per Game',
                'TBR per game': 'Total Rebounds per Game',
                'AST per game': 'Assists per Game'}, inplace=True)

            columns_of_interest = ['Win Shares', 'Points per Game', 'Total Rebounds per Game', 'Assists per Game']

            #Creamos el gráfico
            for column in columns_of_interest:
                fig = px.violin(
                    df_top_20_pick,
                    y=column,
                    x='College',
                    color='College',
                    box=True,
                    points='all')
                
                #Configuramos el gráfico
                fig.update_layout(
                    title=f'Data Distribution and Comparison of {column}',
                    xaxis_title=None,
                    yaxis_title=None,
                    paper_bgcolor='black',
                    plot_bgcolor='black',
                    font_color='white',
                    legend_title=None,
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01))

                for trace in fig.data:
                    if trace.name == 'US':
                        trace.marker.color = 'royalblue'
                    else:
                        trace.marker.color = 'darkorange'
                
                fig.update_xaxes(
                    showline=False, 
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False)
                fig.update_yaxes(
                    showline=False, 
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False)

                #Mostramos el gráfico
                st.plotly_chart(fig)
        
        st.markdown("<p style='font-size:25px; color:#00CC99;'><strong>Conclusion</strong></p>",unsafe_allow_html=True)
        st.write('Based on the results of the Mann-Whitney U test, the p-value is less than the significance level (0.05). Therefore, we do not find sufficient evidence to reject the null hypothesis for any of the performance metrics considered.')
        st.write('Given that the results of the statistical tests show no significant differences between the two groups in any of the performance metrics, there is not enough evidence to reject the null hypothesis (H0). Therefore, we conclude that there are no significant differences in performance between players from American universities and the rest of the world.')    
# -----------------------------------------LIBRERÍAS----------------------------------------------#

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from ortools.linear_solver import pywraplp
from sklearn.ensemble import RandomForestRegressor

# -------------------------------------------DATOS------------------------------------------------#

df_player_salary = pd.read_csv(r'Datasets\salary_2024.csv')

# ----------------------------------------IMAGENES------------------------------------------------#
img_3= 'img\ball.jpg'

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
        Craft your team
    </h1>
</div>
"""

def display():
    st.markdown(css, unsafe_allow_html=True)  
    st.markdown(html_content, unsafe_allow_html=True)

    # ---------------------------------------------TABS------------------------------------------------#
    tab1, tab2, tab3= st.tabs(
        [   'Basic notions to take into account',
            'Some tips before starting',
            'Craft your team'])    

    # -----------------------------TAB1-----------------------------#
    with tab1:
        
        col1, col2 = st.columns(2) 
        
        with col1:
            st.header('NBA Luxury Tax')
            st.write('The NBA has implemented a salary cap of $136 million per team. Under the new agreement, there are now three distinct levels for luxury tax payments:')
       
            st.subheader('Initial Luxury Tax Level ($165 million)')
            st.write('Teams exceeding $165 million in salary will be subject to the luxury tax.')

            st.subheader('Level 1 Luxury Tax ($172 million)')
            st.write("""
            Teams that surpass $172 million will face the following conditions:
            - **No signings** of buyout market players with contracts exceeding the mid-level exception ($12.4 million).
            - **Salary matching** in trades must be up to 110% (previously 125%).
            - Teams can still use the mid-level exception worth $5 million.
            """)

            st.subheader('Super-Luxury Tax ($182.5 million)')
            st.write("""
            For teams exceeding $182.5 million in salary:
            - The mid-level exception cannot be used.
            - Sign-and-trade deals are prohibited.
            - If a team exceeds $182.5 million on the last day of the regular season, it will be prohibited from trading its first-round draft pick for seven years starting July 2024 (referred to as a "frozen pick").
            - If the team exceeds $182.5 million in two of the next four years, its draft pick will be automatically moved to the 30th spot in the first round, regardless of its performance in the previous season.
            """)

            st.header('NBA Roster Regulations Overview')

            st.write('The NBA has specific regulations regarding roster sizes during the regular season, including maximum and minimum limits, and special considerations for player categories.')

            st.subheader('Roster Size Limits')
            st.write("""
            - Maximum Roster Size: Teams can have up to 15 players on their roster, including active and inactive players. Players on two-way contracts are not counted towards this limit.
            - Training Camp: Teams can have up to 20 players during training camp to assist with roster decisions before the season starts.
            - Two-Way Contracts: Teams can include up to 2 players on two-way contracts in addition to the 15 roster players, allowing a total of up to 17 players.
            - Minimum Roster Size: Teams must maintain at least 13 players on their active roster. This requirement was raised from 12 active and 1 inactive starting in the 2011-12 season.
            """)

            st.subheader('Roster Exceptions')
            st.write("""
            - Injury Exceptions: If multiple players are injured, the NBA allows a temporary roster of 16 players with a maximum of 4 inactive due to medical issues. Once a player recovers, the team must cut a player to return to the 15-player limit.
            - Game Day Requirements: For any game, teams must have 8 active players and 2 inactive players. This list must be submitted up to 60 minutes before the game starts.
            """)

            st.subheader('Special Player Categories')
            st.write("""
            - Suspended List: Players on the Suspended List do not count towards the 15-player limit.
            - NBA Draft List: Players on the NBA Draft List, not yet signed, are not counted towards the roster limit.
            - Voluntarily Retired List: Players who retire while under contract do not count towards the 15-player limit.
            - Armed Services List: Players serving in the armed forces are excluded from the 15-player limit.
            - G League Assignment: Players assigned to an affiliated G League team are considered inactive during their assignment.
            """)
       
        with col2:
             st.image(img_3,caption='Image source: Olympics', use_column_width=True)                      
    # -----------------------------TAB2-----------------------------#
    with tab2:
        
        st.subheader('NBA Salaries by Team for the 2023-2024 Season')
        with st.expander('Click on the drop-down menu to view whether the salaries are under the cap or exceeding the thresholds', expanded=False):
            #Agrupamos y sumamos los salarios por equipo
            salary_summary = df_player_salary.groupby('Team')['Salary'].sum().reset_index()

            #Ordenamos de mayor a menor
            salary_summary = salary_summary.sort_values(by='Salary', ascending=False)

            #Calculamos la media de los salarios
            mean_salary = round(salary_summary['Salary'].mean(),0)

            #Paleta de colores
            color_palette = px.colors.sequential.Viridis

            #Crearmos el gráfico
            fig = px.bar(salary_summary, 
                        x='Team', 
                        y='Salary', 
                        title='',
                        labels={'Team': 'Team', 'Salary': 'Salary'},
                        color='Salary',
                        color_continuous_scale=color_palette,
                        template='plotly_dark')

            #Añadimos líneas para mejorar la comprensión de los datos
            fig.add_hline(y=mean_salary, line_dash="dash", line_color="blue", 
                        annotation_text=f'Average teams salary: ${mean_salary:,.0f}', annotation_position="bottom right")

            fig.add_hline(y=136000000, line_dash="dash", line_color="green", 
                        annotation_text='Salary Cap: $136,000,000', annotation_position="bottom right")

            fig.add_hline(y=172000000, line_dash="dash", line_color="orange", 
                        annotation_text='Luxury Tax: $172,000,000', annotation_position="top right")

            fig.add_hline(y=182500000, line_dash="dash", line_color="red", 
                        annotation_text='Super-Luxury Tax: $182,500,000', annotation_position="top right")

            #Configuramos y mostramos el gráfico
            fig.update_yaxes(tickprefix="$", showgrid=False, gridwidth=0)
            fig.update_traces(marker_line_width=0, marker_line_color='black')
            fig.update_layout(yaxis_title='', xaxis_title='')
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)
            fig.update_layout(coloraxis_colorbar=dict(title='', tickvals=[]))

            st.plotly_chart(fig)
        
        st.subheader('Importance of the statistics that define a salary')  
          
        with st.expander("Click on the drop-down menu to see the importance of the statistics that define each player's salary. This can help you determine the metrics for crafting your team.", expanded=False):    
            
            #Seleccionamos las columnas de interés
            columns_of_interest = ['FG', 'FGA', 'FG%', '3P', '3PA',
                                '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%',
                                'ORB', 'DRB', 'AST', 'STL', 'BLK', 'PF', 'PTS',
                                'OWS', 'DWS', 'WS', 'Salary']

            df_rf = df_player_salary[columns_of_interest]

            #Definimos la variable objetivo y las variables predictoras
            y = df_rf['Salary']
            X = df_rf.drop(['Salary'], axis=1)

            #Inicializamos y ajustamos el modelo Random Forest
            model = RandomForestRegressor()
            model.fit(X, y)

            #Obtenemos la importancia de las características
            feature_importances = model.feature_importances_
            feature_importances_percent = 100.0 * (feature_importances / feature_importances.sum())
            feature_importances_percent_rounded = np.round(feature_importances_percent)
            indices = np.argsort(feature_importances_percent_rounded)[::-1]

            #Preparamos datos para la visualización
            importance_df = pd.DataFrame({
                'Feature': X.columns[indices],
                'Importance (%)': feature_importances_percent_rounded[indices]})

            #Creamos el gráfico de barras
            fig = px.bar(importance_df, 
                        x='Feature', 
                        y='Importance (%)',
                        labels={'Feature': 'Metric', 'Importance (%)': 'Importance (%)'},
                        color='Importance (%)',
                        color_continuous_scale='Viridis',
                        template='plotly_dark')

            #Configuramos y mostramos el gráfico

            fig.update_layout(yaxis_title='', xaxis_title='')
            fig.update_xaxes(showgrid=False, gridwidth=0)
            fig.update_yaxes(showgrid=False, gridwidth=0)

            st.plotly_chart(fig)            
    # -----------------------------TAB3-----------------------------#            
    with tab3:
                
        with st.expander('Glossary', expanded=False):
            
            #Creamos un glosario y lo dividimos en columnas
            glossary = {
                'FG': 'Field Goals',
                'FGA': 'Field Goal Attempts',
                'FG%': 'Field Goal Percentage',
                '3P': '3-Point Field Goals',
                '3PA': '3-Point Field Goal Attempts',
                '3P%': '3-Point Field Goal Percentage',
                '2P': '2-Point Field Goals',
                '2PA': '2-Point Field Goal Attempts',
                '2P%': '2-Point Field Goal Percentage',
                'FT': 'Free Throws',
                'FTA': 'Free Throw Attempts',
                'FT%': 'Free Throw Percentage',
                'ORB': 'Offensive Rebounds',
                'DRB': 'Defensive Rebounds',
                'AST': 'Assists',
                'STL': 'Steals',
                'BLK': 'Blocks',
                'PF': 'Personal Fouls',
                'PTS': 'Points',
                'OWS': 'Offensive Win Shares',
                'DWS': 'Defensive Win Shares',
                'WS': 'Win Shares'}

            cols = st.columns(9)

            keys = list(glossary.keys())
            values = list(glossary.values())

            num_items_per_col = len(keys) // 8
            if len(keys) % 8 != 0:
                num_items_per_col += 1

            for i, col in enumerate(cols):
                start_idx = i * num_items_per_col
                end_idx = min(start_idx + num_items_per_col, len(keys))
                items = list(zip(keys[start_idx:end_idx], values[start_idx:end_idx]))

                with col:
                    for key, value in items:
                        st.write(f'**{key}:** {value}')
        
        with st.expander('Set the Parameters', expanded=True):

            #Slider para seleccionar el presupuesto máximo
            max_salary = st.slider(
                'Select the maximum salary',
                min_value=100000000,  
                max_value=200000000,  
                value=136000000,      
                step=1000000)          

            #Slider para seleccionar el número mínimo de jugadores
            min_players = st.slider('Select the minimum number of players', 5, 20, 10)
            #Slider para seleccionar el número máximo de jugadores
            max_players = st.slider('Select the maximum number of players', 5, 20, 15)

            #Estadísticas
            all_stats = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 
                        'ORB', 'DRB', 'AST', 'STL', 'BLK', 'PF', 'PTS', 'OWS', 'DWS', 'WS']

            #Valores ponderados de las estadísticas predeterminados
            default_weights = {
                'PTS': 19, 'FG': 10, 'FGA': 11, 'FT': 10, 'AST': 5, 'WS': 6, 'OWS': 4,
                'FTA': 4, 'FT%': 4, 'PF': 3, '3P%': 3, 'STL': 3, 'ORB': 3, '2PA': 2,
                'DRB': 2, 'DWS': 1, '2P%': 2, 'FG%': 2, 'BLK': 1, '3P': 2, '3PA': 1,
                '2P': 2}
            
            #Opciones en el selectbox
            options = ['-- Select Statistics --'] + all_stats + ['Reset to Default']

            #Selector múltiple para elegir estadísticas al gusto
            selected_stats = st.multiselect('Select statistics to include in the model', options, default=all_stats)

            #Reseteamos a valores ponderados
            if 'Reset to Default' in selected_stats:
                selected_stats = all_stats
                weight_inputs = default_weights
            else:
                #Ajustamos valores ponderados según las estadísticas seleccionadas
                selected_weights = {stat: default_weights.get(stat, 0) for stat in selected_stats}
                weight_inputs = {}
                for stat in selected_stats:
                    if stat != 'Reset to Default':
                        weight = st.number_input(f'Weight for {stat}', min_value=0, max_value=100, value=selected_weights[stat])
                        weight_inputs[stat] = weight

                #Verificamos que la suma de valores ponderados es 100, establecemos alerta para que el usuario lo pueda ajustar
                if sum(weight_inputs.values()) != 100:
                    st.warning(f'Total weight must be 100. Current total weight is {sum(weight_inputs.values())}.')
                    weight_inputs = default_weights

            #Aseguramos que estén actualizados
            weight_inputs = {stat: min(max(weight_inputs.get(stat, 0), 0), 100) for stat in selected_stats}

        ####Iniciamos el problema de optimización lineal####
        
        class Player:
            def __init__(self, name, pos, salary, stats):
                self.name = name
                self.pos = pos
                self.salary = salary
                self.stats = stats

        def create_team(df):
            players = {}
            for index, row in df.iterrows():
                stats = {stat: row[stat] for stat in selected_stats if stat in weight_inputs}
                players[row['Player']] = Player(row['Player'], row['Pos'], row['Salary'], stats)
            return players

        def create_solver():
            return pywraplp.Solver.CreateSolver('GLOP')

        def define_variables(solver, players):
            return {name: solver.IntVar(0, 1, name) for name in players}

        def add_constraints(solver, vars, players, max_salary, min_positions, min_players, max_players):
            
            #Restricción de presupuesto
            salary_constraint = solver.Constraint(0, max_salary)
            for player_name, player in players.items():
                salary_constraint.SetCoefficient(vars[player_name], player.salary)
            
            #Restricción número mínimo de jugadores
            num_players_constraint_min = solver.Constraint(min_players, solver.infinity())
            for var in vars.values():
                num_players_constraint_min.SetCoefficient(var, 1)
            
            #Restricción número máximo de jugadores
            num_players_constraint_max = solver.Constraint(0, max_players)
            for var in vars.values():
                num_players_constraint_max.SetCoefficient(var, 1)
            
            #Restricciones de posiciones para que el equipo sea balanceado
            for pos, min_count in min_positions.items():
                pos_constraint = solver.Constraint(min_count, solver.infinity())
                for player_name, player in players.items():
                    if player.pos == pos:
                        pos_constraint.SetCoefficient(vars[player_name], 1)

        def set_objective(solver, vars, players):
            #Usamos los valores ponderados definidos por el usuario
            objective = solver.Objective()
            for player_name, player in players.items():
                weighted_score = sum(weight_inputs.get(stat, 0) * player.stats[stat] for stat in player.stats)
                objective.SetCoefficient(vars[player_name], weighted_score)
            objective.SetMaximization()

        def solve_and_print(solver, vars, players):
            global optim_team_stats
            status = solver.Solve()
            if status == pywraplp.Solver.OPTIMAL:
                selected_players = [player_name for player_name, var in vars.items() if var.solution_value() == 1]
                total_salary = sum(players[player_name].salary for player_name in selected_players)
                total_stats = {stat: 0 for stat in selected_stats}
                
                for player_name in selected_players:
                    player = players[player_name]
                    for stat in player.stats:
                        total_stats[stat] += player.stats[stat]
                
                #Señalamos al usuario puntos clave del convenio de salarios
                if total_salary < 136000000:
                    salary_category = "You are below the maximum salary cap. Come on, invest more in your team!"
                elif total_salary == 136000000:
                    salary_category = "You have reached the maximum salary cap. You will not pay extra taxes for it."
                elif 136000000 < total_salary <= 172000000:
                    salary_category = "You have exceeded the salary cap; therefore, you are under Luxury Tax rules."
                else:
                    salary_category = "You need to cut wasteful spending to ensure that franchise stability is not compromised!"

                #Mostramos el salario total 
                st.markdown(
                    f"<p style='font-size:20px; color:#3366FF;'><strong>Total team salary:</strong></p>"
                    f"<p>${total_salary:,.0f}: {salary_category}</p>",
                    unsafe_allow_html=True)
             
                #Mostramos número de jugadores y límites de la liga
                num_players = len(selected_players)
                if num_players < 13:
                    player_status = "The number of players is below the threshold, you should consider adding more players to the team."
                elif 13 <= num_players <= 15:
                    player_status = "The number of players is at an optimal level"
                elif 16 <= num_players <= 17:
                    player_status = "Be careful! Make sure that two players are under a two-way contract"
                else:
                    player_status = "You need to reduce the number of players!"


                st.markdown(
                    f"<p style='font-size:20px; color:#3366FF;'><strong>Number of players:</strong></p>"
                    f"<p>{num_players}: {player_status}</p>",
                    unsafe_allow_html=True)
                
                #Mostramos el equipo
                st.markdown(
                    "<p style='font-size:20px; color:#3366FF;'><strong>Team:</strong></p>",
                    unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                for i, player_name in enumerate(selected_players):
                    player = players[player_name]
                    if i % 3 == 0:
                        col1.write(f' - {player.name}: {player.pos}, Salary: ${player.salary:,.0f}')
                    elif i % 3 == 1:
                        col2.write(f' - {player.name}: {player.pos}, Salary: ${player.salary:,.0f}')
                    else:
                        col3.write(f' - {player.name}: {player.pos}, Salary: ${player.salary:,.0f}')
                
                #Mostramos las estadísticas
                st.markdown(
                    "<p style='font-size:20px; color:#3366FF;'><strong>Team statistics:</strong></p>",
                    unsafe_allow_html=True)
                cols = st.columns(7)

                stats_list = list(total_stats.items())
                num_stats = len(stats_list)
                stats_per_col = (num_stats + 6) // 7

                for i, (stat, value) in enumerate(stats_list):
                    stat_display = f' - {stat}: {round(value)}'
                    cols[i // stats_per_col].write(stat_display)

                #Guardamos las estadísticas del equipo optimizado para la comparación posterior
                optim_team_stats = total_stats

            else:
                st.markdown(
                    "<p style='font-size:22px; color:#FF0000;'><strong>An optimal solution was not found</strong></p>",
                    unsafe_allow_html=True)

        #Llamamos a a la función principal
        players = create_team(df_player_salary)
        min_positions = {'PF': 2, 'C': 2, 'SG': 2, 'PG': 2, 'SF': 2}  # Restricciones de posiciones

        solver = create_solver()
        vars = define_variables(solver, players)
        add_constraints(solver, vars, players, max_salary, min_positions, min_players, max_players)
        set_objective(solver, vars, players)
        solve_and_print(solver, vars, players)

        ####COMPARATIVA DEL EQUIPO SELECCIONADO####

        #Seleccionamos un equipo para comparar, y realizamos filtros y cálculos para que sean comparables
        team_names = df_player_salary['Team'].unique()
        html_string = "<p style='font-size:25px; color:#FF6600;'>Select a team to compare</p>"      
        st.markdown(html_string, unsafe_allow_html=True)
        selected_team = st.selectbox('Choose an NBA team from the 2023-2024 season', team_names)

        if selected_team:
            team_df = df_player_salary[df_player_salary['Team'] == selected_team]
            total_salary = team_df['Salary'].sum()
            num_team_players = team_df.shape[0]
            
            #Mostramos el salario total, número de jugadores y estadísticas del equipo seleccionado
            st.markdown(
                f"<p style='font-size:20px; color:#3366FF;'><strong>Total salary of selected team ({selected_team}):</strong></p>"
                f"<p>${total_salary:,.0f}</p>",
                unsafe_allow_html=True)
            st.markdown(
                f"<p style='font-size:20px; color:#3366FF;'><strong>Number of players in selected team ({selected_team}):</strong></p>"
                f"<p>{num_team_players}</p>",
                unsafe_allow_html=True)

            selected_team_stats = {stat: round(team_df[stat].sum()) for stat in selected_stats}
            
            selected_stats = ['FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'AST', 'STL', 'BLK', 'PF', 'PTS',
                            'FG%', '3P%', '2P%', 'FT%', 'OWS', 'DWS', 'WS']
            selected_team_stats = {stat: round(team_df[stat].sum(), 2) if stat in team_df.columns else 0 for stat in selected_stats}

            #Dividimos las estadísticas para mostrar distintos gráficos
            count_stats = ['FG', 'FGA', '3P', '3PA', '2P', '2PA', 'FT', 'FTA', 'ORB', 'DRB', 'AST', 'STL', 'BLK', 'PF', 'PTS']
            percentage_stats = ['FG%', '3P%', '2P%', 'FT%']
            pie_stats = ['OWS', 'DWS', 'WS']

            stats_df1 = pd.DataFrame({
                'Statistic': count_stats,
                'Selected Team': [selected_team_stats[stat] for stat in count_stats],
                'Crafted Team': [optim_team_stats.get(stat, 0) for stat in count_stats]})
            
            #Gráfico 1:
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=stats_df1['Statistic'],
                y=stats_df1['Selected Team'],
                name=f'{selected_team}',
                marker_color='#3366FF'))            
            fig1.add_trace(go.Bar(
                x=stats_df1['Statistic'],
                y=stats_df1['Crafted Team'],
                name='Crafted Team',
                marker_color='#FF6600'))            
            fig1.update_layout(
                title=f'{selected_team} vs Crafted Team Statistics',
                xaxis_title='Statistic',
                yaxis_title='',
                barmode='group',
                legend_title_text='Team Comparison')
            
            fig1.update_xaxes(showgrid=False, gridwidth=0)
            fig1.update_yaxes(showgrid=False, gridwidth=0)
            fig1.update_yaxes(range=[0, None], showticklabels=False)

            st.plotly_chart(fig1)

        #Gráfico 2, 4 pies:
            pie_percentage_stats = ['FG%', '3P%', '2P%', 'FT%']          
            colors = ['#3366FF', '#FF6600']
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                fig_pie_fg = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['FG%'], optim_team_stats.get('FG%', 0)],
                    marker_colors=colors,
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie_fg.update_layout(title_text=f'{selected_team} vs Crafted Team FG% Comparison')
                st.plotly_chart(fig_pie_fg)

            with col2:
                fig_pie_3p = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['3P%'], optim_team_stats.get('3P%', 0)],
                    marker_colors=colors,
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie_3p.update_layout(title_text=f'{selected_team} vs Crafted Team 3P% Comparison')
                st.plotly_chart(fig_pie_3p)

            with col3:
                fig_pie_2p = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['2P%'], optim_team_stats.get('2P%', 0)],
                    marker_colors=colors,
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie_2p.update_layout(title_text=f'{selected_team} vs Crafted Team 2P% Comparison')
                st.plotly_chart(fig_pie_2p)

            with col4:
                fig_pie_ft = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['FT%'], optim_team_stats.get('FT%', 0)],
                    marker_colors=colors,
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie_ft.update_layout(title_text=f'{selected_team} vs Crafted Team FT% Comparison')
                st.plotly_chart(fig_pie_ft)

            #Gráfico 3, 3 pies:
            col1, col2, col3 = st.columns(3)

            with col1:
                fig_pie1 = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['OWS'], optim_team_stats.get('OWS', 0)],
                    marker_colors=['#3366FF', '#FF6600'],
                    textinfo='percent',  
                    insidetextorientation='horizontal',
                    textposition='inside',  
                    insidetextfont=dict(color='black')))
                
                fig_pie1.update_layout(title_text=f'{selected_team} vs Crafted Team Offensive Win Shares Comparison')
                st.plotly_chart(fig_pie1)

            with col2:
                fig_pie2 = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['DWS'], optim_team_stats.get('DWS', 0)],
                    marker_colors=['#3366FF', '#FF6600'],
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie2.update_layout(title_text=f'{selected_team} vs Crafted Team Defensive Win Shares Comparison')
                st.plotly_chart(fig_pie2)

            with col3:
                fig_pie3 = go.Figure(go.Pie(
                    labels=[f'{selected_team}', 'Crafted Team'],
                    values=[selected_team_stats['WS'], optim_team_stats.get('WS', 0)],
                    marker_colors=['#3366FF', '#FF6600'],
                    textinfo='percent',
                    insidetextorientation='horizontal',
                    textposition='inside',
                    insidetextfont=dict(color='black')))
                
                fig_pie3.update_layout(title_text=f'{selected_team} vs Crafted Team Win Shares Comparison')
                st.plotly_chart(fig_pie3)
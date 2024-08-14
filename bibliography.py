# -----------------------------------------LIBRERÍAS----------------------------------------------#
import streamlit as st

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
        Bibliography
    </h1>
</div>
"""

def display():
    st.markdown(css, unsafe_allow_html=True)  
    st.markdown(html_content, unsafe_allow_html=True) 

    #Texto para la bibliografía
    bibliography_text = """
    <div style="margin-top: 20px; text-align: center;">
        <p style="font-size: 18px;">
            To carry out this project, the following sources of information have been used: <br>
             https://www.nba.com<br>
             https://www.basketball-reference.com <br>
             https://espndeportes.espn.com <br>
             https://spain.id.nba.com<br>
        </p>
    </div>
    """
    st.markdown(bibliography_text, unsafe_allow_html=True)    
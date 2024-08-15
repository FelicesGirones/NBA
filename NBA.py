# -----------------------------------------LIBRERÍAS----------------------------------------------#
import streamlit as st
import base64
import draft
import regular_season
import team
import bibliography
import introduction

import pandas as pd
import plotly.express as px

# ----------------------------------------IMAGENES------------------------------------------------#

img_1= 'img/floor.jpg'
img_5= 'img/logo.jpg'
gif_path = 'img/Gift.gif'

# -----------------------------------CONFIGURACIÓN DE LA PÁGINA-----------------------------------#

st.set_page_config(page_title='NBA', 
                   layout='wide', 
                   page_icon='🏀')

#CSS para aplicar la fuente Arial Black
css = """
<style>
body {
    font-family: 'Arial Black', sans-serif;
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

#GIF
with open(gif_path, "rb") as gif_file:
    gif_data = gif_file.read()
    gif_base64 = base64.b64encode(gif_data).decode("utf-8")

#TITULO
html_content = f"""
<div style="display: flex; align-items: center; justify-content: center; margin-top: 20px;">
    <img src="data:image/gif;base64,{gif_base64}" style="width: 100px; height: auto; margin-right: 20px;"/>
    <h1 style='color: #FF6600; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-size: 80px;'>
        NBA Analysis
    </h1>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)

# -------------------------------------------FONDO------------------------------------------------#

def add_bg_from_local(image_file, position):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    st.markdown(
        f"""
        <style>
            .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: {position};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local(img_1, position="top")

# ------------------------------------------MODULOS-----------------------------------------------#

st.sidebar.image(img_5,caption='Image source: Polideportes', use_column_width=True)

if 'module' not in st.session_state:
    st.session_state.module = 'home'

if st.sidebar.button("Introduction"):
    st.session_state.module = 'Introduction'
elif st.sidebar.button("Draft"):
    st.session_state.module = 'Draft'    
elif st.sidebar.button("Regular Season"):
    st.session_state.module = 'Regular Season'
elif st.sidebar.button("Craft your team"):
    st.session_state.module = 'Craft your team'
elif st.sidebar.button("Bibliography"):
    st.session_state.module = 'Bibliography'    

if st.session_state.module == 'Introduction':
    introduction.display()
    st.sidebar.button("🔙 Return Home", on_click=lambda: setattr(st.session_state, 'module', 'home'))
elif st.session_state.module == 'Draft':
    draft.display()
    st.sidebar.button("🔙 Return Home", on_click=lambda: setattr(st.session_state, 'module', 'home'))        
elif st.session_state.module == 'Regular Season':
    regular_season.display()
    st.sidebar.button("🔙 Return Home", on_click=lambda: setattr(st.session_state, 'module', 'home'))
elif st.session_state.module == 'Craft your team':
    team.display()
    st.sidebar.button("🔙 Return Home", on_click=lambda: setattr(st.session_state, 'module', 'home'))    
elif st.session_state.module == 'Bibliography':
    bibliography.display()
    st.sidebar.button("🔙 Return Home", on_click=lambda: setattr(st.session_state, 'module', 'home'))      
    
if 'module' not in st.session_state:
    st.session_state.module = 'home'

# -----------------------------------------LIBRERÍAS----------------------------------------------#
import streamlit as st

# ----------------------------------------IMAGENES------------------------------------------------#

img_4= 'img\map.png'

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
        Introduction
    </h1>
</div>
"""

def display():
    st.markdown(css, unsafe_allow_html=True)  
    st.markdown(html_content, unsafe_allow_html=True) 
    
# -------------------------------------------CONTENIDO--------------------------------------------#  
  
    col1, col2 = st.columns(2) 
    
    with col1:
        st.markdown("""
        <div style="font-size: 20px; color: white;">
            The NBA, founded in 1949 from the merger of the BAA and NBL but considering 1946 as its origin, consists of 30 teams and is the premier professional basketball league globally. After merging with the ABA in 1976, the NBA now runs its regular season from October to April, with playoffs culminating in the NBA Finals in June. As of 2020, NBA players are the highest-paid athletes on average. The league, affiliated with USA Basketball and headquartered in Manhattan, is the world's third-wealthiest sports league by revenue. The Boston Celtics hold the most championships, with 18 titles, including their recent victory over the Dallas Mavericks in the 2024 Finals.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.image(img_4,caption='Image source: Hoopsbasket', use_column_width=True)

if __name__ == "__main__":
    display() 
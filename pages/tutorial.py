import streamlit as st
import pathlib
from st_image_button import st_image_button


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/tutorial.css")
load_css(css_path)


if st_image_button("","home.png","50px","outlined"):    
    st.switch_page("pages/start.py")

st.html("""
    <div style='background-color: #FFA100; padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: white; font-size: 50px;'>Game Report</h1>
    </div>
""")

st.html("""
    <div style="background-color: white; padding: 10px; border-radius: 10px; border: 3px solid #FFA100;font-family: 'IBM Plex Sans', sans-serif;">
        <p style='font-size: 14px;font-weight: bold; line-height: 1.6; text-align: justify; color: #FFA100;'>
            Use this section of the application to report the actions of your team during a new game. 
            The tool proposed to record all the moments is new and innovative, letting you save every direction that the ball has taken along the match.
            <br><br>
            If it is your first time with the app, look quickly at the tutorial proposed just below, otherwise skip it and start concentrating!
        </p>
    </div>
""")

   



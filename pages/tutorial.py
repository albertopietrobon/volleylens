import streamlit as st
import pathlib
from st_image_button import st_image_button

if "page" not in st.session_state:
    st.session_state.page = 0

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/tutorial.css")
load_css(css_path)


if st_image_button("","home.png","50px","outlined"):    
    st.session_state.page = 0
    st.switch_page("pages/start.py")
    

st.html("""
    <div style='background-color: #FFA100; padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: white; font-size: 50px;'>Game Report</h1>
    </div>
""")

st.html("""
    <div style="background-color: white; padding: 10px; font-family: 'Rockwell Condensed', sans-serif;">
        <p style='font-size: 20px;font-weight: bold; line-height: 1.6; text-align: justify; color: black;'>
            Use this section of the application to report the actions of your team during a new game. 
            The tool proposed to record all the moments is new and innovative, letting you save every direction that the ball has taken along the match.
            <br><br>
            If it is your first time with the app, look quickly at the tutorial proposed just below, otherwise skip it and start concentrating!
        </p>
    </div>
""")

st.html("""
    <div style='background-color: #C7C7C7; padding: 10px; border-radius: 10px; text-align: left;'>
        <h1 style='color: white; font-size: 24px;'>Tutorial</h1>
    </div>
""")




# Lista delle immagini
tutorial_images = ["im1.jpg", "im2.jpg", "im3.jpg", "im4.jpg","im5.jpg", "im6.jpg", "im7.jpg", "im8.jpg"]
with st.container(border=True):
    immagine = st.image(tutorial_images[st.session_state.page], use_container_width=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Back", use_container_width=True, key="indietro") and st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()

with col2:
    if st.button("Skip", use_container_width=True, key="skip"):
        st.session_state.page = 0
        st.switch_page("pages/data.py")  # Cambia pagina

av = ">>"
with col3:
    if st.button(f"Next", use_container_width=True, key="avanti") and st.session_state.page < len(tutorial_images) - 1:
        st.session_state.page += 1
        st.rerun()


   



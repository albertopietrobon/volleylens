import streamlit as st
import pandas as pd
import pathlib
from PIL import Image

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/w_player.css")
load_css(css_path)

# SCELTA PLAYER IN CASO DI PUNTO GUADAGNATO
if "player_selected" not in st.session_state:
     st.session_state.player_selected = ""

st.subheader("Select the player involved")



col1,col2,col3,col4 = st.columns(4,vertical_alignment="center")

with col1:
    image1 = Image.open(f"{st.session_state.game_roster[0]}.png")
    st.image(image1,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[0]}",key="bot1",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[0]
        st.switch_page("pages/w_court.py")

with col2:
    image2 = Image.open(f"{st.session_state.game_roster[1]}.png")
    st.image(image2,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[1]}",key="bot2",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[1]
        st.switch_page("pages/w_court.py")

with col3:
    image3 = Image.open(f"{st.session_state.game_roster[2]}.png")
    st.image(image3,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[2]}",key="bot3",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[2]
        st.switch_page("pages/w_court.py")

with col4:
    image4 = Image.open(f"{st.session_state.game_roster[3]}.png")
    st.image(image4,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[3]}",key="bot4",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[3]
        st.switch_page("pages/w_court.py")



col5,col6,col7,col8 = st.columns(4,vertical_alignment="center")

with col5:
    image5 = Image.open(f"{st.session_state.game_roster[4]}.png")
    st.image(image5,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[4]}",key="bot5",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[4]
        st.switch_page("pages/w_court.py")

with col6:
    image6 = Image.open(f"{st.session_state.game_roster[5]}.png")
    st.image(image6,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[5]}",key="bot6",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[5]
        st.switch_page("pages/w_court.py")

with col7:
    image7 = Image.open(f"{st.session_state.game_roster[6]}.png")
    st.image(image7,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[6]}",key="bot7",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[6]
        st.switch_page("pages/w_court.py")

with col8:
    image8 = Image.open(f"{st.session_state.game_roster[7]}.png")
    st.image(image8,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[7]}",key="bot8",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[7]
        st.switch_page("pages/w_court.py")



col9,col10,col11,col12 = st.columns(4,vertical_alignment="center")

with col9:
    image9 = Image.open(f"{st.session_state.game_roster[8]}.png")
    st.image(image9,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[8]}",key="bot9",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[8]
        st.switch_page("pages/w_court.py")

with col10:
    image10 = Image.open(f"{st.session_state.game_roster[9]}.png")
    st.image(image10,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[9]}",key="bot10",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[9]
        st.switch_page("pages/w_court.py")

with col11:
    image11 = Image.open(f"{st.session_state.game_roster[10]}.png")
    st.image(image11,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[10]}",key="bot11",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[10]
        st.switch_page("pages/w_court.py")

with col12:
    image12 = Image.open(f"{st.session_state.game_roster[11]}.png")
    st.image(image12,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[11]}",key="bot12",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[11]
        st.switch_page("pages/w_court.py")



col13,col14,col15,col16 = st.columns(4,vertical_alignment="center")

with col14:
    image14 = Image.open(f"{st.session_state.game_roster[12]}.png")
    st.image(image14,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[12]}",key="bot13",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[12]
        st.switch_page("pages/w_court.py")

with col15:
    image15 = Image.open(f"{st.session_state.game_roster[13]}.png")
    st.image(image15,use_container_width=True)
    if st.button(f"{st.session_state.game_roster[13]}",key="bot14",use_container_width=True):
        st.session_state.player_selected = st.session_state.game_roster[13]
        st.switch_page("pages/w_court.py")

st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")

# Tasto score page
if st.button("Back"):
    st.session_state.point_scored = st.session_state.point_scored - 1
    st.switch_page("pages/score.py")
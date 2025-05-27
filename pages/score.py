import streamlit as st
import pandas as pd
import io   # per scaricare il file excel
from PIL import Image
import pathlib
from st_image_button import st_image_button

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/score.css")
load_css(css_path)

if "point_scored" not in st.session_state:
    st.session_state.point_scored = 0

if "point_lost" not in st.session_state:
    st.session_state.point_lost = 0

if "n_set" not in st.session_state:
    st.session_state.n_set = 1

col1, col2, col3 = st.columns(3, vertical_alignment='center')
st.markdown(
                """
                <style>
                .risultato {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    font-size: 30px
                }
                </style>
                """,
                unsafe_allow_html=True
            )

with col1:
    home = Image.open("Numia Vero Volley Milano.png")
    st.image(home,use_container_width=True)
with col2:
    risultato1 = f"SET {st.session_state.n_set}"
    st.markdown(f'<div class="risultato">{risultato1}</div>', unsafe_allow_html=True)
    risultato2 = f"{st.session_state.point_scored} - {st.session_state.point_lost}"
    st.markdown(f'<div class="risultato">{risultato2}</div>', unsafe_allow_html=True)
with col3:
    opp = Image.open(f"{st.session_state.game_opp}.png")
    st.image(opp,use_container_width=True)

col4, col5, col6, col7, col8 = st.columns(5, vertical_alignment='center')
with col5:
    if st.button("Point scored", key="p_scored", use_container_width=True):
        st.session_state.point_scored = st.session_state.point_scored + 1
        st.switch_page("pages/w_point_type.py")

with col7:
    if st.button("Point lost", key="p_lost", use_container_width=True):
        st.session_state.point_lost = st.session_state.point_lost + 1
        st.switch_page("pages/l_player.py")

col9, col10, col11 = st.columns(3, vertical_alignment='center')
with col9:
    if st.button("Delete last point", key="delete_point", use_container_width=True):
        if st.session_state.current_row != 0 :
            if st.session_state.df.loc[st.session_state.current_row-1,"score"] == "S":
                st.session_state.point_scored = st.session_state.point_scored - 1
            elif st.session_state.df.loc[st.session_state.current_row-1,"score"] == "L":
                st.session_state.point_lost = st.session_state.point_lost - 1

            st.session_state.df.loc[st.session_state.current_row-1,"score"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"point_type"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"player"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"attack_zone"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"serve_zone"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"defense_zone"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"block_zone"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"out_zone"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"our_score"]= None
            st.session_state.df.loc[st.session_state.current_row-1,"opp_score"]= None

            st.session_state.current_row = st.session_state.current_row -1
            st.rerun()

with col11:
    #passa al prossimo set
    if st.button("Next Set", key="next_set", use_container_width=True):
        if st.session_state.n_set <=4:
            if st.session_state.n_set == 1 :

                st.session_state.set1 = st.session_state.df

                st.session_state.df = pd.DataFrame({
                    "score": [None],
                    "point_type": [None],
                    "player": [None],
                    "attack_zone": [None],
                    "serve_zone": [None],
                    "defense_zone": [None],
                    "block_zone": [None],
                    "out_zone": [None],
                    "our_score": [None],  # Inizializza con 0
                    "opp_score": [None],  # Inizializza con 0
                })

                st.session_state.point_scored = 0
                st.session_state.point_lost = 0
                st.session_state.current_row = 0
            
            if st.session_state.n_set == 2 :

                st.session_state.set2 = st.session_state.df

                st.session_state.df = pd.DataFrame({
                    "score": [None],
                    "point_type": [None],
                    "player": [None],
                    "attack_zone": [None],
                    "serve_zone": [None],
                    "defense_zone": [None],
                    "block_zone": [None],
                    "out_zone": [None],
                    "our_score": [None],  # Inizializza con 0
                    "opp_score": [None],  # Inizializza con 0
                })

                st.session_state.point_scored = 0
                st.session_state.point_lost = 0
                st.session_state.current_row = 0

            if st.session_state.n_set == 3 :

                st.session_state.set3 = st.session_state.df

                st.session_state.df = pd.DataFrame({
                    "score": [None],
                    "point_type": [None],
                    "player": [None],
                    "attack_zone": [None],
                    "serve_zone": [None],
                    "defense_zone": [None],
                    "block_zone": [None],
                    "out_zone": [None],
                    "our_score": [None],  # Inizializza con 0
                    "opp_score": [None],  # Inizializza con 0
                })

                st.session_state.point_scored = 0
                st.session_state.point_lost = 0
                st.session_state.current_row = 0

            if st.session_state.n_set == 4 :

                st.session_state.set4 = st.session_state.df

                st.session_state.df = pd.DataFrame({
                    "score": [None],
                    "point_type": [None],
                    "player": [None],
                    "attack_zone": [None],
                    "serve_zone": [None],
                    "defense_zone": [None],
                    "block_zone": [None],
                    "out_zone": [None],
                    "our_score": [None],  # Inizializza con 0
                    "opp_score": [None],  # Inizializza con 0
                })

                st.session_state.point_scored = 0
                st.session_state.point_lost = 0
                st.session_state.current_row = 0
            
            st.session_state.n_set += 1
            st.rerun()
        else:
            st.error("Reached maximum number of sets!")

col12, col13, col14 = st.columns(3, vertical_alignment='center')

with col12:
    if st_image_button("","home.png","50px","outlined"):
        st.session_state.point_scored = 0
        st.session_state.point_lost = 0
        st.session_state.n_set = 1
        st.switch_page('pages/start.py')

with col14:
    if st.button("Save Game Report", key="save", use_container_width=True):
            st.success(f"Thank for your trial. The application is still in development.")
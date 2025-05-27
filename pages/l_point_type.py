import streamlit as st
import pandas as pd
import pathlib

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/l_point_type.css")
load_css(css_path)

st.subheader("Select the point cause")

st.write("\n\n")
col1, col2 = st.columns([0.4,0.6], vertical_alignment="center")
with col1:
    if st.button("Opponent point", key="opp_point", use_container_width=True):
        st.switch_page("pages/l_court_opp_point.py")
with col2:
    st.write("Point lost by the team due to opponent point.")

st.write("\n\n")
col3, col4 = st.columns([0.4,0.6], vertical_alignment="center")
with col3:
    if st.button("Team error", key="team_error", use_container_width=True):
        st.switch_page("pages/l_court_team_error.py")
with col4:
    st.write("Point lost by the team due to an error outside or on net during serve or attack.")

st.write("\n\n")
col5, col6 = st.columns([0.4,0.6], vertical_alignment="center")
with col5:
    if st.button("Foul", key="foul", use_container_width=True):
        st.session_state.df.loc[st.session_state.current_row,"score"]="L"
        st.session_state.df.loc[st.session_state.current_row,"point_type"]="foul"
        st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
        st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
        st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
        st.session_state.current_row += 1
        st.switch_page("pages/score.py")
with col6:
    st.write("Point lost by the team due to a foul (e.g. rotation fault, illegal substitution, etc.) committed by the player.")

st.write("\n\n")
col7, col8 = st.columns([0.4,0.6], vertical_alignment="center")
with col7:
    if st.button("Card", key="card", use_container_width=True):
        st.session_state.df.loc[st.session_state.current_row,"score"]="L"
        st.session_state.df.loc[st.session_state.current_row,"point_type"]="card"
        st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
        st.session_state.df.loc[st.session_state.current_row,"attack_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"serve_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"defense_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"block_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
        st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
        st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
        st.session_state.current_row += 1
        st.switch_page("pages/score.py")
with col8:
    st.write("Point lost by the team due to a card given to the player.")

st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")
st.write("\n\n")

# Tasto score page
if st.button("Back", key="back"):
    st.session_state.point_lost = st.session_state.point_lost - 1
    st.switch_page("pages/score.py")
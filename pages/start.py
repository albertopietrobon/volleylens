import streamlit as st
import pandas as pd
from PIL import Image
import pathlib
# PRIMA PAGINA, SCELTA TRA NEW GAME, GAME HISTORY E PLAYER STATS

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/home_page.css")
load_css(css_path)

logo = Image.open("logo2.jpg")
st.image(logo,use_container_width=True)


st.html("""
    <div style="background-color: white; padding: 30px;font-family: 'Rockwell Condensed', sans-serif;">
        <p style='font-size: 24px;font-weight: bold; line-height: 1.6; text-align: center; color: black;'>
            The app that follows volleyball coaches to improve their athletes and
            <br>
            MAKE THE RIGHT DECISION AT THE RIGHT MOMENT.
            <br><br>
            Create digital reports of new matches in real-time with an interactive volleyball court and then go to see the updated statistics of your players or team to 
            <br>
            BUILD EFFECTIVE TRAININGS.
            
        </p>
    </div>
""")

bot1,im1 = st.columns([0.7,0.3])
with bot1:
    new_game = st.button("**NEW GAME**\n\nKeep track of the main actions of your players during a match with a highly interactive tool for reporting.\n\n Use the gathered data to look at the player and team statistics.",key="new_game",use_container_width=True)
with im1:
    report = Image.open("report.jpeg")
    report = report.resize((report.width, 1000)) 
    st.image(report, use_container_width=True)


im2,bot2 = st.columns([0.3,0.7])
with im2:
    player = Image.open("player.jpg")
    player = player.resize((player.width, 1050)) 
    st.image(player,use_container_width=True)
with bot2:
    player_stats = st.button("**PLAYER STATS**\n\nLook at the statistics of your players focusing on the main fundamentals to prepare your future matches with deeper insights.",key="player_st",use_container_width=True)
bot3,im3 = st.columns([0.7,0.3])
with bot3:   
    game_history = st.button("**TEAM STATS**\n\nLook at the statistics of your team focusing on the points and errors occured during previous games.",key="team_st",use_container_width=True)
with im3:
    team = Image.open("team.jpg")
    team = team.resize((team.width, 1050)) 
    st.image(team,use_container_width=True)



if new_game:
    
    st.session_state.info_df = pd.DataFrame()

    st.session_state.df = pd.DataFrame({
        "score": [None],
        "point_type": [None],
        "player": [None],
        "attack_zone": [None],
        "serve_zone": [None],
        "defense_zone": [None],
        "block_zone": [None],
        "out_zone": [None],
        "our_score": [None],  
        "opp_score": [None],  
    })

    st.session_state.current_row = 0
    st.session_state.n_set = 1

    st.session_state.set1 = pd.DataFrame()
    st.session_state.set2 = pd.DataFrame()
    st.session_state.set3 = pd.DataFrame()
    st.session_state.set4 = pd.DataFrame()
    st.session_state.set5 = pd.DataFrame()

    st.switch_page("pages/tutorial.py")

if game_history:
    st.switch_page("pages/team_stats.py")

if player_stats:
   st.switch_page("pages/player_stats.py")
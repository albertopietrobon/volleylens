import streamlit as st
import pandas as pd
import numpy as np
import pathlib

# PAGINA CAMPO IN CASO DI PUNTO PERSO, TEAM ERROR

#recall the court.css file to create the court
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/l_court_team_error.css")
load_css(css_path)

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'point_att' not in st.session_state:
    st.session_state.point_att = '0'

if 'point_def' not in st.session_state:
    st.session_state.point_def = '0'


def click_step(i):
    st.session_state.step = i

def click_att(i):
    st.session_state.point_att = i

def click_def(i):
    st.session_state.point_def = i


def return_set_page():
    st.session_state.step = 0
    st.switch_page("pages/score.py")
    


if st.session_state.step == 0:

    #creation of the court
    col1,col2,col3,col4,col5=st.columns(5,gap="small")

    with col1:
        eb1 = st.button("out", key="ebutt1", on_click=click_def,args=['out_left'], use_container_width=True)

    with col2:
        eb2 = st.button("out", key="ebutt2", on_click=click_def,args=['out_1'], use_container_width=True)
        eb3 = st.button("1", key="ebutt3", use_container_width=True)
        eb4 = st.button("2", key="ebutt4", use_container_width=True)
        eb5 = st.button("block/net", key="ebutt5", on_click=click_def,args=['block_net_2'], use_container_width=True)
        eb6 = st.button("4", key="ebutt6", on_click=click_att,args=['att_4'], use_container_width=True)
        eb7 = st.button("5", key="ebutt7", on_click=click_att,args=['att_5'], use_container_width=True)
        eb8 = st.button("serve", key="ebutt8", on_click=click_att,args=['serve_5'], use_container_width=True)

    with col3:
        eb9 = st.button("out", key="ebutt9", on_click=click_def,args=['out_6'], use_container_width=True)
        eb10 = st.button("1", key="ebutt10", use_container_width=True)
        eb11 = st.button("2", key="ebutt11", use_container_width=True)
        eb12 = st.button("block/net", key="ebutt12", on_click=click_def,args=['block_net_3'], use_container_width=True)
        eb13 = st.button("4", key="ebutt13", on_click=click_att,args=['att_3'], use_container_width=True)
        eb14 = st.button("5", key="ebutt14", on_click=click_att,args=['att_6'], use_container_width=True)
        eb15 = st.button("serve", key="ebutt15", on_click=click_att,args=['serve_6'], use_container_width=True)

    with col4:
        eb16 = st.button("out", key="ebutt16", on_click=click_def,args=['out_5'], use_container_width=True)
        eb17 = st.button("1", key="ebutt17", use_container_width=True)
        eb18 = st.button("2", key="ebutt18", use_container_width=True)
        eb19 = st.button("block/net", key="ebutt19", on_click=click_def,args=['block_net_4'], use_container_width=True)
        eb20 = st.button("4", key="ebutt20", on_click=click_att,args=['att_2'], use_container_width=True)
        eb21 = st.button("5", key="ebutt21", on_click=click_att,args=['att_1'], use_container_width=True)
        eb22 = st.button("serve", key="ebutt22", on_click=click_att,args=['serve_1'], use_container_width=True)
    
    with col5:
        eb23 = st.button("out", key="ebutt23", on_click=click_def,args=['out_right'], use_container_width=True)

    col6,col7,col8=st.columns(3, vertical_alignment="center")
    with col6:
        if st.button("Back",key="back",use_container_width=True):
            st.session_state.point_lost = st.session_state.point_lost - 1
            st.switch_page("pages/score.py")
    with col8:
        confirm = st.button("Confirm point", key="confirm", on_click=click_step, args=[1], use_container_width=True)


if st.session_state.step == 1:

    if st.session_state.point_att != '0' and st.session_state.point_def !='0':
        st.info(f"You selected: error in {st.session_state.point_def} from {st.session_state.point_att} ({st.session_state.player_selected}).\n\nDo you want to save the action?")
        
        col9,col10,col11=st.columns(3, vertical_alignment="center")
        with col9:
            back = st.button("Back", key="back", on_click=click_step, args=[0], use_container_width=True)
        with col11:
            save = st.button("Save", key="save", on_click=click_step, args = [2], use_container_width=True)
        
    elif (st.session_state.point_att== '0') or (st.session_state.point_def== '0'):
        st.warning("Please go back. You are missing the point selection!")
        
        col12,col13,col14=st.columns(3, vertical_alignment="center")
        with col12:
            back = st.button("Back", key="back", on_click=click_step, args=[0], use_container_width=True)
        
        
if st.session_state.step == 2:
    # Salva i valori in base al tipo di azione

    st.session_state.df.loc[st.session_state.current_row,"score"]="L"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="team error"
    st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
    st.session_state.df.loc[st.session_state.current_row, "defense_zone"] = None
    st.session_state.df.loc[st.session_state.current_row,"our_score"]= st.session_state.point_scored
    st.session_state.df.loc[st.session_state.current_row,"opp_score"]= st.session_state.point_lost
    
    # Metodo per salvare le zone del campo sulla stessa riga dell'excel
    if 'att' in st.session_state.point_att:
        st.session_state.df.loc[st.session_state.current_row, "attack_zone"] = st.session_state.point_att
    else:
        st.session_state.df.loc[st.session_state.current_row, "attack_zone"] = None

    if 'serve' in st.session_state.point_att:
        st.session_state.df.loc[st.session_state.current_row, "serve_zone"] = st.session_state.point_att
    else:
        st.session_state.df.loc[st.session_state.current_row, "serve_zone"] = None

    if 'out' in st.session_state.point_def:
        st.session_state.df.loc[st.session_state.current_row, "out_zone"] = st.session_state.point_def
    else:
        st.session_state.df.loc[st.session_state.current_row, "out_zone"] = None

    if 'block_net' in st.session_state.point_def:
        st.session_state.df.loc[st.session_state.current_row, "block_zone"] = st.session_state.point_def
    else:
        st.session_state.df.loc[st.session_state.current_row, "block_zone"] = None




    # Reset delle variabili
    st.session_state.point_att = '0'
    st.session_state.point_def = '0'

    # Passa alla riga successiva
    st.session_state.current_row += 1

    return_set_page()

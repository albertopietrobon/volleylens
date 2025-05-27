import streamlit as st
import pandas as pd
import numpy as np
import pathlib

# PAGINA CAMPO IN CASO DI PUNTO GUADAGNATO

#recall the court.css file to create the court
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = pathlib.Path("assets/w_court.css")
load_css(css_path)

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'point_att' not in st.session_state:
    st.session_state.point_att = '0'

if 'point_def' not in st.session_state:
    st.session_state.point_def = '0'

if 'point_block' not in st.session_state:
    st.session_state.point_block = '0'

def click_step(i):
    st.session_state.step = i

def click_att(i):
    st.session_state.point_att = i
    st.session_state.point_block = '0'

def click_def(i):
    st.session_state.point_def = i
    st.session_state.point_block = '0'

def click_block(i):
    st.session_state.point_block = i
    st.session_state.point_att = '0'
    st.session_state.point_def = '0'

def return_set_page():
    st.session_state.step = 0
    st.switch_page("pages/score.py")
    


if st.session_state.step == 0:

    #creation of the court
    col1,col2,col3=st.columns(3,gap="small")

    with col1:
        b1 = st.button("1", key="butt1", on_click=click_def,args=['def_1'], use_container_width=True)
        b2 = st.button("2", key="butt2", on_click=click_def,args=['def_8'], use_container_width=True)
        b3 = st.button("3", key="butt3", on_click=click_def,args=['def_2'], use_container_width=True)
        b4 = st.button("block", key="butt4", on_click=click_block,args=['block_4'], use_container_width=True)
        b5 = st.button("5", key="butt5", on_click=click_att,args=['att_4'], use_container_width=True)
        b6 = st.button("6", key="butt6", on_click=click_att,args=['att_5'], use_container_width=True)
        b7 = st.button("serve", key="butt7", on_click=click_att,args=['serve_5'], use_container_width=True)

    with col2:
        b8 = st.button("8", key="butt8", on_click=click_def,args=['def_6'], use_container_width=True)
        b9 = st.button("9", key="butt9", on_click=click_def,args=['def_10'], use_container_width=True)
        b10 = st.button("10", key="butt10", on_click=click_def,args=['def_3'], use_container_width=True)
        b11 = st.button("block", key="butt11", on_click=click_block,args=['block_3'], use_container_width=True)
        b12 = st.button("12", key="butt12", on_click=click_att,args=['att_3'], use_container_width=True)
        b13 = st.button("13", key="butt13", on_click=click_att,args=['att_6'], use_container_width=True)
        b14 = st.button("serve", key="butt14", on_click=click_att,args=['serve_6'], use_container_width=True)

    with col3:
        b15 = st.button("15", key="butt15", on_click=click_def,args=['def_5'], use_container_width=True)
        b16 = st.button("16", key="butt16", on_click=click_def,args=['def_9'], use_container_width=True)
        b17 = st.button("17", key="butt17", on_click=click_def,args=['def_4'], use_container_width=True)
        b18 = st.button("block", key=f"butt18", on_click=click_block,args=['block_2'], use_container_width=True)
        b19 = st.button("19", key="butt19", on_click=click_att,args=['att_2'], use_container_width=True)
        b20 = st.button("20", key="butt20", on_click=click_att,args=['att_1'], use_container_width=True)
        b21 = st.button("serve", key=f"butt21", on_click=click_att,args=['serve_1'], use_container_width=True)

    col4,col5,col6=st.columns(3, vertical_alignment="center")
    with col4:
        if st.button("Back",key="back",use_container_width=True):
            st.session_state.point_scored = st.session_state.point_scored - 1
            st.switch_page("pages/score.py")
    with col6:
        confirm = st.button("Confirm point", key="confirm", on_click=click_step, args=[1], use_container_width=True)


if st.session_state.step == 1:

    if st.session_state.point_block != '0':
        st.info(f"You selected: point on {st.session_state.point_block} ({st.session_state.player_selected}).\n\nDo you want to save the action?")
        
        col7,col8,col9=st.columns(3, vertical_alignment="center")
        with col7:
            back = st.button("Back", key="back", on_click=click_step, args=[0], use_container_width=True)
        with col9:
            save = st.button("Save", key="save", on_click=click_step, args = [2], use_container_width=True)
        
    elif st.session_state.point_att != '0' and st.session_state.point_def != '0':
        st.info(f"You selected: point from {st.session_state.point_att} to {st.session_state.point_def} ({st.session_state.player_selected}).\n\nDo you want to save the action?")
        
        col10,col11,col12=st.columns(3, vertical_alignment="center")
        with col10:
            back = st.button("Back", key="back", on_click=click_step, args=[0], use_container_width=True)
        with col12:
            save = st.button("Save", key="save", on_click=click_step, args = [2], use_container_width=True)

    elif (st.session_state.point_att == '0' and st.session_state.point_def != '0' ) or (st.session_state.point_att != '0' and st.session_state.point_def == '0' ) or (st.session_state.point_att == '0' and st.session_state.point_def == '0' and st.session_state.point_block == '0'):
        st.warning("Please go back. You are missing the point selection!")
        
        col13,col14,col15=st.columns(3, vertical_alignment="center")
        with col13:
            back = st.button("Back", key="back", on_click=click_step, args=[0], use_container_width=True)
        
if st.session_state.step == 2:

    st.session_state.df.loc[st.session_state.current_row,"score"]="S"
    st.session_state.df.loc[st.session_state.current_row,"point_type"]="team point"
    st.session_state.df.loc[st.session_state.current_row,"player"]= st.session_state.player_selected
    st.session_state.df.loc[st.session_state.current_row,"out_zone"]= None
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

    if 'def' in st.session_state.point_def:
        st.session_state.df.loc[st.session_state.current_row, "defense_zone"] = st.session_state.point_def
    else:
        st.session_state.df.loc[st.session_state.current_row, "defense_zone"] = None

    if 'block' in st.session_state.point_block:
        st.session_state.df.loc[st.session_state.current_row, "block_zone"] = st.session_state.point_block
    else:
        st.session_state.df.loc[st.session_state.current_row, "block_zone"] = None

    # Reset delle variabili
    st.session_state.point_att = '0'
    st.session_state.point_def = '0'
    st.session_state.point_block = '0'

    # Passa alla riga successiva
    st.session_state.current_row += 1
    
    return_set_page()       

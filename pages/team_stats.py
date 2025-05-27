import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import glob
import plotly.graph_objects as go
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import streamlit.components.v1 as components
import altair as alt
from st_image_button import st_image_button

if "info_type" not in st.session_state:
    st.session_state.info_type = "errors"

if "fundamental_type" not in st.session_state:
    st.session_state.fundamental_type = "attack"

if "player" not in st.session_state:
    st.session_state.player = "Paola Egonu"

if "player_2" not in st.session_state:
    st.session_state.player_2 = "Paola Egonu"

if "date_choice" not in st.session_state:
    st.session_state.date_choice = "all"

def plot_volleyball_attack_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze,soglia_freq=0.01):
    
    if st.session_state.info_type == "points":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team attack distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0, court_length], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0, court_length], 'k--', linewidth=1) #6m verticale
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [5*court_length/6,5*court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
        1: (2*court_width/3,0), 
        2: (2*court_width/3,court_length/3),
        3: (court_width/3,court_length/3),
        4: (0,court_length/3), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            if 2 <= zone <= 4:
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            else:
                circle = plt.Rectangle((x, y),height=6,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+3, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Attack zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
        1: (0,court_length), 
        2: (0,2*court_length/3),
        3: (court_width/3,2*court_length/3),
        4: (2*court_width/3,2*court_length/3), 
        5: (2*court_width/3,court_length), 
        6: (court_width/3,court_length),
        8: (0,5*court_length/6),
        9: (2*court_width/3,5*court_length/6),
        10:(court_width/3,5*court_length/6)
        }

        cmap2 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,3), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (1.5,court_length/3+1.5), 
            5: (1.5,3), 
            6: (court_width/3+1.5,3)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (0+1.5,court_length-1.5), 
            2: (0+1.5,2*court_length/3-1.5),
            3: (court_width/3+1.5,2*court_length/3-1.5),
            4: (2*court_width/3+1.5,2*court_length/3-1.5), 
            5: (2*court_width/3+1.5,court_length-1.5), 
            6: (court_width/3+1.5,court_length-1.5),
            8: (0+1.5,5*court_length/6-1.5),
            9: (2*court_width/3+1.5,5*court_length/6-1.5),
            10:(court_width/3+1.5,5*court_length/6-1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='green', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
    
    elif st.session_state.info_type == "errors":

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team attack distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0, court_length/2+1], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0, court_length/2+1], 'k--', linewidth=1) #6m verticale
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/2+1,court_length/2+1], 'k--', linewidth=1) 
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)
        plt.plot([-1,court_width+1], [court_length/2,court_length/2], 'k--', linewidth=1)
        plt.plot([-1,-1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width+1,court_width+1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([-1,court_width+1], [court_length+1,court_length+1], 'k--', linewidth=1)
        plt.plot([0,0], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width,court_width], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width/3,court_width/3], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([2*court_width/3,2*court_width/3], [court_length, court_length+1], 'k--', linewidth=1)

        # Coordinate delle zone di attack
        zone_coords_att = {
        1: (2*court_width/3,0), 
        2: (2*court_width/3,court_length/3),
        3: (court_width/3,court_length/3),
        4: (0,court_length/3), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            if 2 <= zone <= 4:
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            else:
                circle = plt.Rectangle((x, y),height=6,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+3, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Attack zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (0,court_length+1), 
            2: (0,court_length/2+1),
            3: (court_width/3,court_length/2+1),
            4: (2*court_width/3,court_length/2+1), 
            5: (2*court_width/3,court_length+1), 
            6: (court_width/3,court_length+1),
            7: (-1,court_length+1),
            8: (court_width,court_length+1)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 7<= zone <= 8:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-10,width=1, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+0.5, y-5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,3), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (1.5,court_length/3+1.5), 
            5: (1.5,3), 
            6: (court_width/3+1.5,3)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (1.5,court_length+0.5), 
            2: (1.5,court_length/2+0.5),
            3: (court_width/3+1+1.5,court_length/2+0.5),
            4: (2*court_width/3+1.5,court_length/2+0.5), 
            5: (2*court_width/3+1.5,court_length+0.5), 
            6: (court_width/3+1.5,court_length+0.5),
            7: (-0.5,court_length-4),
            8: (court_width+0.5,court_length-4)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
def plot_volleyball_serve_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze,soglia_freq=0.01):
    
    if st.session_state.info_type == "points":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team serve distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [court_length/2, court_length], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [court_length/2, court_length], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width/3,court_width/3], [-1,0], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [-1,0], 'k--', linewidth=1) #6m verticale
        plt.plot([0,0], [-1,0], 'k--', linewidth=1) #3m verticale
        plt.plot([0,court_width], [-1,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width ,court_width], [-1,0], 'k--', linewidth=1)
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [5*court_length/6,5*court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
        1: (2*court_width/3,0), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():

            if 5<= zone <= 6:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if zone == 1:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Serving zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
        1: (0,court_length), 
        2: (0,2*court_length/3),
        3: (court_width/3,2*court_length/3),
        4: (2*court_width/3,2*court_length/3), 
        5: (2*court_width/3,court_length), 
        6: (court_width/3,court_length),
        8: (0,5*court_length/6),
        9: (2*court_width/3,5*court_length/6),
        10:(court_width/3,5*court_length/6)
        }

        cmap2 = plt.cm.summer  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ace zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,-0.5), 
            5: (1.5,-0.5), 
            6: (court_width/3+1.5,-0.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (0+1.5,court_length-1.5), 
            2: (0+1.5,2*court_length/3-1.5),
            3: (court_width/3+1.5,2*court_length/3-1.5),
            4: (2*court_width/3+1.5,2*court_length/3-1.5), 
            5: (2*court_width/3+1.5,court_length-1.5), 
            6: (court_width/3+1.5,court_length-1.5),
            8: (0+1.5,5*court_length/6-1.5),
            9: (2*court_width/3+1.5,5*court_length/6-1.5),
            10:(court_width/3+1.5,5*court_length/6-1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='green', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
    
    elif st.session_state.info_type == "errors":

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team serve distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0,-1], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([0,0], [0,-1], 'k--', linewidth=1) #3m verticale
        plt.plot([court_width, court_width], [0,-1], 'k--', linewidth=1) #6m verticale
        plt.plot([0, court_width], [-1,-1], 'k--', linewidth=1)
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/2+1,court_length/2+1], 'k--', linewidth=1) 
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)
        plt.plot([-1,court_width+1], [court_length/2,court_length/2], 'k--', linewidth=1)
        plt.plot([-1,-1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width+1,court_width+1], [court_length/2, court_length+1], 'k--', linewidth=1)
        plt.plot([-1,court_width+1], [court_length+1,court_length+1], 'k--', linewidth=1)
        plt.plot([0,0], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width,court_width], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([court_width/3,court_width/3], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([2*court_width/3,2*court_width/3], [court_length, court_length+1], 'k--', linewidth=1)

        # Coordinate delle zone di attack
        zone_coords_att = {
        1: (2*court_width/3,0), 
        5: (0,0), 
        6: (court_width/3,0)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():

            if 5<= zone <= 6:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if zone == 1:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Serve zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (0,court_length+1), 
            2: (0,court_length/2+1),
            3: (court_width/3,court_length/2+1),
            4: (2*court_width/3,court_length/2+1), 
            5: (2*court_width/3,court_length+1), 
            6: (court_width/3,court_length+1),
            7: (-1,court_length+1),
            8: (court_width,court_length+1)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 7<= zone <= 8:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-10,width=1, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+0.5, y-5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (2*court_width/3+1.5,-0.5), 
            5: (1.5,-0.5), 
            6: (court_width/3+1.5,-0.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (1.5,court_length+0.5), 
            2: (1.5,court_length/2+0.5),
            3: (court_width/3+1+1.5,court_length/2+0.5),
            4: (2*court_width/3+1.5,court_length/2+0.5), 
            5: (2*court_width/3+1.5,court_length+0.5), 
            6: (court_width/3+1.5,court_length+0.5),
            7: (-0.5,court_length-4),
            8: (court_width+0.5,court_length-4)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
def plot_volleyball_block_frequency(attack_frequencies):
    
    
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('off')
    ax.set_aspect('equal')
    plt.title(f'Team block distribution', fontsize=8)

    # Dimensioni del campo (proporzionali)
    court_width = 9
    court_length = 18

    # Disegna il campo
    rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=1.5, facecolor='lightgrey', alpha=1)
    ax.add_patch(rect)
    plt.plot([court_width/3,court_width/3], [0, court_length], 'k--', linewidth=0.5) #3m verticale
    plt.plot([2*court_width /3, 2*court_width /3], [0, court_length], 'k--', linewidth=0.5) #6m verticale
    plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=1) # Linea dei 3m nostra
    plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=1)  # Linea dei 3m avversaria
    plt.plot([0,court_width], [court_length/2-1,court_length/2-1], 'k--', linewidth=0.5) 
    plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=1.5)

    # Coordinate delle zone di attacco 
    zone_coords_att = { 
    2: (2*court_width/3,court_length/3+2),
    3: (court_width/3,court_length/3+2),
    4: (0,court_length/3+2), 
    }

    if st.session_state.info_type == "points":
        cmap1 = plt.cm.summer  # Scegli la colormap che preferisci
    elif st.session_state.info_type == "errors":
        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
    
    max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

    norm = plt.Normalize(vmin=0, vmax=max_freq1)
    sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
    sm1.set_array([])    

    for zone, freq in attack_frequencies.items():
        
        if 2 <= zone <= 4:
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            circle = plt.Rectangle((x, y),height=1,width=3, facecolor=color, edgecolor=None, alpha=1)
            ax.add_patch(circle)
            ax.text(x+1.5, y+0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=3)
    
    cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.4, location='right')
    cbar1.set_label('Block zone [%]',fontsize=6)
    cbar1.ax.tick_params(labelsize=3)

    st.pyplot(fig) 
def plot_volleyball_defense_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze,soglia_freq=0.01):
    
    if st.session_state.info_type == "errors":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team defense distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [0, court_length], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0, court_length], 'k--', linewidth=1) #6m verticale
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/6,court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
            1: (0,court_length), 
            2: (0,2*court_length/3),
            3: (court_width/3,2*court_length/3),
            4: (2*court_width/3,2*court_length/3), 
            5: (2*court_width/3,court_length), 
            6: (court_width/3,court_length)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():
            x, y = zone_coords_att[zone]
            color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
            if 2 <= zone <= 4:
                circle = plt.Rectangle((x, y),height=-3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            else:
                circle = plt.Rectangle((x, y),height=-6,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-3, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Attack zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (2*court_width/3,0), 
            2: (2*court_width/3,court_length/3),
            3: (court_width/3,court_length/3),
            4: (0,court_length/3), 
            5: (0,0), 
            6: (court_width/3,0),
            8: (2*court_width/3,court_length/6),
            9: (0,court_length/6),
            10:(court_width/3,court_length/6)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ending zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (0+1.5,court_length-1.5), 
            2: (0+1.5,2*court_length/3-1.5),
            3: (court_width/3+1.5,2*court_length/3-1.5),
            4: (2*court_width/3+1.5,2*court_length/3-1.5), 
            5: (2*court_width/3+1.5,court_length-1.5), 
            6: (court_width/3+1.5,court_length-1.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (2*court_width/3+1.5,0+1.5), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (0+1.5,court_length/3+1.5), 
            5: (0+1.5,0+1.5), 
            6: (court_width/3+1.5,0+1.5),
            8: (2*court_width/3+1.5,court_length/6+1.5),
            9: (0+1.5,court_length/6+1.5),
            10:(court_width/3+1.5,court_length/6+1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 
def plot_volleyball_receive_frequency(attack_frequencies,defense_frequencies,transizioni_frequenze,soglia_freq=0.01):
    
    
    if st.session_state.info_type == "errors":
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        ax.set_aspect('equal')
        plt.title(f'Team receive distribution', fontsize=14)

        # Dimensioni del campo (proporzionali)
        court_width = 9
        court_length = 18

        # Disegna il campo
        rect = plt.Rectangle((0,0), court_width, court_length, edgecolor='black',linewidth=3, facecolor='lightgrey', alpha=1)
        ax.add_patch(rect)
        plt.plot([court_width/3,court_width/3], [court_length, court_length+1], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [court_length, court_length+1], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width/3,court_width/3], [0,court_length/2], 'k--', linewidth=1) #3m verticale
        plt.plot([2*court_width /3, 2*court_width /3], [0,court_length/2], 'k--', linewidth=1) #6m verticale
        plt.plot([0,0], [court_length, court_length+1], 'k--', linewidth=1) #3m verticale
        plt.plot([0,court_width], [court_length+1,court_length+1], 'k--', linewidth=1) #6m verticale
        plt.plot([court_width ,court_width], [court_length, court_length+1], 'k--', linewidth=1)
        plt.plot([0,court_width], [court_length/3,court_length/3], 'k-', linewidth=2) # Linea dei 3m nostra
        plt.plot([0,court_width], [2*court_length/3,2*court_length/3], 'k-', linewidth=2)  # Linea dei 3m avversaria
        plt.plot([0,court_width], [court_length/6,court_length/6], 'k--', linewidth=1)  # Linea dei 6m avversaria
        plt.plot([0,court_width], [court_length/2,court_length/2], 'k-', linewidth=3)

        # Coordinate delle zone di attacco 
        zone_coords_att = {
            1: (0,court_length+1), 
            5: (2*court_width/3,court_length+1), 
            6: (court_width/3,court_length+1)
        }


        cmap1 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq1 = attack_frequencies.max() if not attack_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq1)
        sm1 = plt.cm.ScalarMappable(cmap=cmap1.reversed(), norm=norm)
        sm1.set_array([])    

        for zone, freq in attack_frequencies.items():

            if 5<= zone <= 6:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if zone == 1:
                x, y = zone_coords_att[zone]
                color = cmap1(1-freq / max_freq1) if max_freq1 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=-1,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y-0.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)

        
        cbar1 = plt.colorbar(sm1, ax=ax, orientation='vertical', pad=-0.5, location='right')
        cbar1.set_label('Serving zone [%]')
        cbar1.ax.tick_params(labelsize=8)

        # Coordinate delle zone di difesa 
        zone_coords_def = {
            1: (2*court_width/3,0), 
            2: (2*court_width/3,court_length/3),
            3: (court_width/3,court_length/3),
            4: (0,court_length/3), 
            5: (0,0), 
            6: (court_width/3,0),
            8: (2*court_width/3,court_length/6),
            9: (0,court_length/6),
            10:(court_width/3,court_length/6)
        }

        cmap2 = plt.cm.autumn  # Scegli la colormap che preferisci
        max_freq2 = defense_frequencies.max() if not defense_frequencies.empty else 1

        norm = plt.Normalize(vmin=0, vmax=max_freq2)
        sm2 = plt.cm.ScalarMappable(cmap=cmap2.reversed(), norm=norm)
        sm2.set_array([])    

        for zone, freq in defense_frequencies.items():
        
            if 1<= zone <= 6:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            if 8<= zone <= 10:
                x, y = zone_coords_def[zone]
                color = cmap2(1-freq / max_freq2) if max_freq2 > 0 else 'lightgray'
                circle = plt.Rectangle((x, y),height=3,width=3, facecolor=color, edgecolor=None, alpha=1)
                ax.add_patch(circle)
                ax.text(x+1.5, y+1.5, f'{freq:.2f}', ha='center', va='center', color='black', fontsize=8)
            
        
        cbar2 = plt.colorbar(sm2, ax=ax, orientation='vertical', pad=0.1, location='left')
        cbar2.set_label('Ace zone [%]')
        cbar2.ax.tick_params(labelsize=8)
        






        # Centri approssimativi delle zone di attacco (lato inferiore)
        zone_centers_att = {
            1: (0+1.5,court_length+1-0.5), 
            5: (2*court_width/3+1.5,court_length+1-0.5), 
            6: (court_width/3+1.5,court_length+1-0.5)
        }

        # Centri approssimativi delle zone di difesa (lato superiore)
        zone_centers_def = {
            1: (2*court_width/3+1.5,0+1.5), 
            2: (2*court_width/3+1.5,court_length/3+1.5),
            3: (court_width/3+1.5,court_length/3+1.5),
            4: (0+1.5,court_length/3+1.5), 
            5: (0+1.5,0+1.5), 
            6: (court_width/3+1.5,0+1.5),
            8: (2*court_width/3+1.5,court_length/6+1.5),
            9: (0+1.5,court_length/6+1.5),
            10:(court_width/3+1.5,court_length/6+1.5)
        }

        # Disegna le frecce
        max_freq_transizione = transizioni_frequenze.max().max() if not transizioni_frequenze.empty else 0.01 # Evita la divisione per zero

        for att_zone, row in transizioni_frequenze.iterrows():
            if att_zone in zone_centers_att:
                x_start, y_start = zone_centers_att[att_zone]
                for def_zone, freq in row.items():
                    if def_zone in zone_centers_def and freq > soglia_freq:
                        x_end, y_end = zone_centers_def[def_zone]
                        larghezza = 5* (freq / max_freq_transizione)  # Larghezza base scalata
                        scala_punta = 30 * (freq / max_freq_transizione)       # Scala della punta scalata

                        arrow = FancyArrowPatch(
                            (x_start, y_start), (x_end, y_end),
                            arrowstyle="-|>",
                            mutation_aspect=0.8,
                            mutation_scale=scala_punta,
                            connectionstyle="Arc3, rad=0.1",
                            fc='black', ec='orange', alpha=0.5,
                            lw=larghezza
                        )
                        ax.add_patch(arrow)
        st.pyplot(fig) 

def make_player_radar_chart(player_name, stats):
    metrics = ['Att%','Serve%','Block%']#,'Def error contribution','Rec error contribution']#'Att error contribution',
               #'Serve error contribution','Block error contribution','Att point contribution','Serve point contribution','Block point contribution']
    values = [stats[metric] for metric in metrics]
    values.append(values[0])  # Chiudi il radar plot
    angles = metrics + [metrics[0]]  # Chiudi il radar plot

    ideal_values = [100, 100, 100, 100]  # L'ultimo 100 chiude il grafico

    # Crea la figura del grafico radar usando Plotly.
    fig = go.Figure()


    # Aggiunge la traccia per la performance ideale.
    fig.add_trace(go.Scatterpolar(
        r=ideal_values,
        theta=angles,
        fill='toself',
        name='Ideal performance',
        line=dict(color='green'),  # Colore della linea per la performance ideale.
        opacity=0.2 #Possibilità di aggiungere trasparenza
    ))

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=angles,
        fill='toself',
        name=player_name,
        line=dict(color='green'),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Percentuali da 0 a 100
            )
        ),
        showlegend=True
    )
    return fig
def make_player_2_radar_chart(player_name,player_2_name, stats, stats_2):
    metrics = ['Att%','Serve%','Block%']#,'Def error contribution','Rec error contribution']#'Att error contribution',
               #'Serve error contribution','Block error contribution','Att point contribution','Serve point contribution','Block point contribution']
    values = [stats[metric] for metric in metrics]
    values.append(values[0])  # Chiudi il radar plot
    angles = metrics + [metrics[0]]  # Chiudi il radar plot

    values_2 = [stats_2[metric] for metric in metrics]
    values_2.append(values_2[0])  # Chiudi il radar plot
    



    ideal_values = [100, 100, 100, 100]  # L'ultimo 100 chiude il grafico

    # Crea la figura del grafico radar usando Plotly.
    fig = go.Figure()


    # Aggiunge la traccia per la performance ideale.
    fig.add_trace(go.Scatterpolar(
        r=ideal_values,
        theta=angles,
        fill='toself',
        name='Ideal performance',
        line=dict(color='green'),  # Colore della linea per la performance ideale.
        opacity=0.2 #Possibilità di aggiungere trasparenza
    ))

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=angles,
        fill='toself',
        name=player_name,
        line=dict(color='green'),
    ))

    fig.add_trace(go.Scatterpolar(
        r=values_2,
        theta=angles,
        fill='toself',
        name=player_2_name,
        line=dict(color='orange'),
        opacity=0.5
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]  # Percentuali da 0 a 100
            )
        ),
        showlegend=True
    )
    return fig

def get_image(zoom_ball):
    return OffsetImage(plt.imread("pallone_verde.png"), zoom=zoom_ball)  # Assicurati di avere "pallone_verde.png"
def get_image2(zoom_ball):
    return OffsetImage(plt.imread("pallone_grigio.png"), zoom=zoom_ball)  # Assicurati di avere "pallone_verde.png"
def get_image3(zoom_ball):
    return OffsetImage(plt.imread("pallone_rosso.png"), zoom=zoom_ball)  # Assicurati di avere "pallone_verde.png"
def bar_plot_points(bar_att):
    # Creazione delle posizioni x più interne
        x_positions = np.linspace(0.5, len(bar_att) - 1.5, len(bar_att))  # Distribuisce le colonne con margine ai lati

        # Creazione del grafico
        fig, ax = plt.subplots(figsize=(8, 6))

        for idx, (x, row) in enumerate(zip(x_positions, bar_att.itertuples())):
            points = row[2]  # Punti medi
            errors = row[3]

            int_points = int(points)  # Parte intera dei punti
            frac_points = points - int_points  # Parte frazionaria
            int_errors = int(errors)  # Parte intera degli errori
            frac_errors = errors - int_errors  # Parte frazionaria
            max_value = int(max(max(bar_att["Mean points x set"]), max(bar_att["Mean errors x set"]))) + 3
            zoom_ball = 3.3723*(max_value)**(-0.968)
            
            # Disegna i palloni interi usando l'immagine
            for y in range(1, int_points + 1):
                ab = AnnotationBbox(get_image(zoom_ball), (x, y-0.5), frameon=False, zorder=3)
                ax.add_artist(ab)
                ax.text(x, int_points + 1, f"{points:.1f}", ha='center', fontsize=12, fontweight='bold', zorder=3)

            # Se ci sono decimali, aggiungi il pallone tagliato
            if frac_points > 0:
                ab = AnnotationBbox(get_image(zoom_ball), (x, int_points + 0.5), frameon=False,zorder=3)
                ax.add_artist(ab)
                ax.add_patch(plt.Rectangle((x-0.5 , int_points+ frac_points), 0.9, 1, color='white', zorder=4))
                ax.text(x, int_points + frac_points + 1, f"{points:.1f}", ha='center', fontsize=12, fontweight='bold', zorder= 5)
            
            # Disegna i palloni interi usando l'immagine
            for y in range(1, int_errors + 1):
                ab = AnnotationBbox(get_image2(zoom_ball), (x+0.1, y-0.5), frameon=False, zorder=0)
                ax.add_artist(ab)
                
            # Se ci sono decimali, aggiungi il pallone tagliato
            if frac_errors > 0:
                ab = AnnotationBbox(get_image2(zoom_ball), (x+0.1, int_errors + 0.5), frameon=False, zorder=0)
                ax.add_artist(ab)
                ax.add_patch(plt.Rectangle((x-0.4, int_errors+ frac_errors), 1, 1, color='white', zorder=1))
                
        
            
        # Configurazione degli assi
        ax.set_xticks(x_positions)
        ax.set_xticklabels(bar_att["Set"])
        ax.set_yticks(range(1, int(max(max(bar_att["Mean points x set"]), max(bar_att["Mean errors x set"]))) + 4))
        ax.set_ylabel("Mean points per set")
        #ax.set_xlabel("Set")
        #ax.set_title("Distribuzione dei punti medi per set (con palloni spostati verso l'interno)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
def bar_plot_errors(bar_att):
    # Creazione delle posizioni x più interne
        x_positions = np.linspace(0.5, len(bar_att) - 1.5, len(bar_att))  # Distribuisce le colonne con margine ai lati

        # Creazione del grafico
        fig, ax = plt.subplots(figsize=(8, 6))

        for idx, (x, row) in enumerate(zip(x_positions, bar_att.itertuples())):
            points = row[2]  # Punti medi
            errors = row[3]

            int_points = int(points)  # Parte intera dei punti
            frac_points = points - int_points  # Parte frazionaria
            int_errors = int(errors)  # Parte intera degli errori
            frac_errors = errors - int_errors  # Parte frazionaria
            
            max_value = int(max(max(bar_att["Mean points x set"]), max(bar_att["Mean errors x set"]))) + 3
            zoom_ball = 3.3723*(max_value)**(-0.968)

            # Disegna i palloni interi usando l'immagine
            for y in range(1, int_points + 1):
                ab = AnnotationBbox(get_image2(zoom_ball), (x, y-0.5), frameon=False, zorder = 0)
                ax.add_artist(ab)
                
            # Se ci sono decimali, aggiungi il pallone tagliato
            if frac_points > 0:
                ab = AnnotationBbox(get_image2(zoom_ball), (x, int_points + 0.5), frameon=False, zorder = 0)
                ax.add_artist(ab)
                ax.add_patch(plt.Rectangle((x-0.5, int_points+ frac_points), 1, 1, color='white', zorder = 1))
                
            # Disegna i palloni interi usando l'immagine
            for y in range(1, int_errors + 1):
                ab = AnnotationBbox(get_image3(zoom_ball), (x+0.1, y-0.5), frameon=False, zorder = 3)
                ax.add_artist(ab)
                ax.text(x+0.1, int_errors + 1, f"{errors:.1f}", ha='center', fontsize=12, fontweight='bold', zorder=3)

                
            # Se ci sono decimali, aggiungi il pallone tagliato
            if frac_errors > 0:
                ab = AnnotationBbox(get_image3(zoom_ball), (x+0.1, int_errors + 0.5), frameon=False, zorder = 3)
                ax.add_artist(ab)
                ax.add_patch(plt.Rectangle((x-0.4, int_errors+ frac_errors), 0.9, 1, color='white', zorder=4))
                ax.text(x+0.1, int_errors + 1, f"{errors:.1f}", ha='center', fontsize=12, fontweight='bold', zorder=5)

        
            
        # Configurazione degli assi
        ax.set_xticks(x_positions)
        ax.set_xticklabels(bar_att["Set"])
        ax.set_yticks(range(1, int(max(max(bar_att["Mean points x set"]), max(bar_att["Mean errors x set"]))) + 4))
        ax.set_ylabel("Mean errors per set")
        #ax.set_xlabel("Set")
        #ax.set_title("Distribuzione dei punti medi per set (con palloni spostati verso l'interno)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
def bar_plot_def_errors(bar_att):
    # Creazione delle posizioni x più interne
        x_positions = np.linspace(0.5, len(bar_att) - 1.5, len(bar_att))  # Distribuisce le colonne con margine ai lati

        # Creazione del grafico
        fig, ax = plt.subplots(figsize=(8, 6))

        for idx, (x, row) in enumerate(zip(x_positions, bar_att.itertuples())):
            errors = row[2]

            int_errors = int(errors)  # Parte intera degli errori
            frac_errors = errors - int_errors  # Parte frazionaria
            
            max_value = int(max(bar_att["Mean errors x set"])) + 3
            zoom_ball = 3.3723*(max_value)**(-0.968)
    
            # Disegna i palloni interi usando l'immagine
            for y in range(1, int_errors + 1):
                ab = AnnotationBbox(get_image3(zoom_ball), (x, y-0.5), frameon=False, zorder = 3)
                ax.add_artist(ab)
                ax.text(x, int_errors + 1, f"{errors:.1f}", ha='center', fontsize=12, fontweight='bold', zorder=3)

                
            # Se ci sono decimali, aggiungi il pallone tagliato
            if frac_errors > 0:
                ab = AnnotationBbox(get_image3(zoom_ball), (x, int_errors + 0.5), frameon=False, zorder = 3)
                ax.add_artist(ab)
                ax.add_patch(plt.Rectangle((x-0.4, int_errors+ frac_errors), 0.9, 1, color='white', zorder=4))
                ax.text(x, int_errors + 1, f"{errors:.1f}", ha='center', fontsize=12, fontweight='bold', zorder=5)

        
            
        # Configurazione degli assi
        ax.set_xticks(x_positions)
        ax.set_xticklabels(bar_att["Set"])
        ax.set_yticks(range(1, int(max(bar_att["Mean errors x set"])) + 4))
        ax.set_ylabel("Mean errors per set")
        #ax.set_xlabel("Set")
        #ax.set_title("Distribuzione dei punti medi per set (con palloni spostati verso l'interno)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)
def result_visualization(df_games,match_index):
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
        st.markdown(
            """
            <style>
            .parziali {
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
                font-size: 10px
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        logo1,info,logo2=st.columns([0.2,0.6,0.2],vertical_alignment='center')
        with logo2:
            image2 = Image.open(f"{df_games.iloc[match_index,1]}.png")
            st.image(image2, use_container_width=True)
        with logo1:
            image1 = Image.open("Numia Vero Volley Milano.png")
            st.image(image1, use_container_width=True)
        with info:
            risultato = f"{df_games.iloc[match_index,2][0]} - {df_games.iloc[match_index,2][1]}"
            st.markdown(f'<div class="risultato">{risultato}</div>', unsafe_allow_html=True)
            #df_games.iloc[match_index,3][0] = tuple(map(int, df_games.iloc[match_index,3][0]))
            if len(df_games.iloc[match_index,3]) == 3:
                parziali1 = f"{df_games.iloc[match_index,3][0][0]} |  {df_games.iloc[match_index,3][1][0]}  | {df_games.iloc[match_index,3][2][0]}"
                st.markdown(f'<div class="parziali">{parziali1}</div>', unsafe_allow_html=True)
                parziali2 = f"{df_games.iloc[match_index,3][0][1]} |  {df_games.iloc[match_index,3][1][1]}  | {df_games.iloc[match_index,3][2][1]}"
                st.markdown(f'<div class="parziali">{parziali2}</div>', unsafe_allow_html=True)
            elif len(df_games.iloc[match_index,3]) == 4:
                parziali1 = f"{df_games.iloc[match_index,3][0][0]} |  {df_games.iloc[match_index,3][1][0]}  | {df_games.iloc[match_index,3][2][0]}  | {df_games.iloc[match_index,3][3][0]}"
                st.markdown(f'<div class="parziali">{parziali1}</div>', unsafe_allow_html=True)
                parziali2 = f"{df_games.iloc[match_index,3][0][1]} |  {df_games.iloc[match_index,3][1][1]}  | {df_games.iloc[match_index,3][2][1]}  | {df_games.iloc[match_index,3][3][1]}"
                st.markdown(f'<div class="parziali">{parziali2}</div>', unsafe_allow_html=True)
            elif len(df_games.iloc[match_index,3]) == 5:
                parziali1 = f"{df_games.iloc[match_index,3][0][0]} |  {df_games.iloc[match_index,3][1][0]}  | {df_games.iloc[match_index,3][2][0]}  | {df_games.iloc[match_index,3][3][0]}  | {df_games.iloc[match_index,3][4][0]}"
                st.markdown(f'<div class="parziali">{parziali1}</div>', unsafe_allow_html=True)
                parziali2 = f"{df_games.iloc[match_index,3][0][1]} |  {df_games.iloc[match_index,3][1][1]}  | {df_games.iloc[match_index,3][2][1]}  | {df_games.iloc[match_index,3][3][1]}  | {df_games.iloc[match_index,3][4][1]}"
                st.markdown(f'<div class="parziali">{parziali2}</div>', unsafe_allow_html=True)             
def match_history_att_point(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "team point"].dropna(subset=["attack_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "team point") & (alt.datum.attack_zone != None),
            alt.value("#00A600"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_serve_point(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "team point"].dropna(subset=["serve_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "team point") & (alt.datum.serve_zone != None),
            alt.value("#00A600"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_block_point(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "team point"].dropna(subset=["block_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "team point") & (alt.datum.block_zone != None),
            alt.value("#00A600"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_att_error(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "team error"].dropna(subset=["attack_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "team error") & (alt.datum.attack_zone != None),
            alt.value("#FF0000"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_serve_error(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "team error"].dropna(subset=["serve_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "team error") & (alt.datum.serve_zone != None),
            alt.value("#FF0000"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_block_error(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "opp point"].dropna(subset=["block_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "opp point") & (alt.datum.block_zone != None),
            alt.value("#FF0000"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_defense_error(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "opp point"].dropna(subset=["attack_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "opp point") & (alt.datum.attack_zone != None),
            alt.value("#FF0000"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)
def match_history_receive_error(inst_df):
    inst_df["points"] = inst_df["our_score"].astype(str) + "-" + inst_df["opp_score"].astype(str) + " (Set " + inst_df["n_set"].astype(str) + ")"

    green_counts = inst_df[inst_df["point_type"] == "opp point"].dropna(subset=["serve_zone"])
    count_df = green_counts.groupby("player").size().reset_index(name="green_bars")
    count_df = count_df.sort_values("green_bars", ascending=False)
    # 🔹 Mantieni l'ordine originale del DataFrame per evitare riordini
    inst_df["points"] = pd.Categorical(inst_df["points"], categories=inst_df["points"].unique(), ordered=True)
    inst_df["player"] = pd.Categorical(inst_df["player"], categories=count_df["player"], ordered=True)
    
    chart_punti = alt.Chart(inst_df).mark_bar().encode(
        x=alt.X("points", type="ordinal", title="Match history", sort=list(inst_df["points"].unique()), axis=alt.Axis(labelLimit=70)),
        y=alt.Y("player", type="nominal", title="Player", sort=list(count_df["player"])),
        color=alt.condition(
            (alt.datum.point_type == "opp point") & (alt.datum.serve_zone != None),
            alt.value("#FF0000"),  # Verde per attacchi validi
            alt.value("#F2F2F2")   # Grigio per tutti gli altri momenti
        ),
        tooltip=["player", "points", "score"]
    ).interactive()

    set_transitions = pd.DataFrame({
        "points": inst_df.groupby("n_set")["points"].first().values,  # Primo punteggio di ogni set
        "n_set": inst_df["n_set"].unique()  # Numero del set
    })

    # Creazione delle linee verticali per segnare i passaggi tra set
    set_lines = alt.Chart(set_transitions).mark_rule(color="black", strokeDash=[1,1]).encode(
        x=alt.X("points", type="ordinal"),
        tooltip=["n_set"]
    )

                    
    chart_finale = (chart_punti + set_lines).properties(width=1000)
    st.altair_chart(chart_finale)











#DATA EXTRACTION 1
excel_files = glob.glob("*.xlsx")

excels = pd.DataFrame({})
for file_names in excel_files:
    excels[file_names] = pd.read_excel(file_names, sheet_name=None)

if st_image_button("","home.png","50px","outlined"):     
    st.switch_page("pages/start.py")

st.html("""
    <div style='background-color: #FFA100; padding: 20px; border-radius: 10px; text-align: center;'>
        <h1 style='color: white; font-size: 50px;'>Team Statistics</h1>
    </div>
""")

col1,col2,col3 = st.columns(3, vertical_alignment='center',border=False)

with col2:

    image = Image.open(f"Numia Vero Volley Milano.png")
    st.image(image,use_container_width=True)


#STATS INIZIALIZATION

player_2_stats = {
        'Played matches':0,
        'Scored points': 0,
        'Lost points': 0,
        'Aces': 0,
        'Attack points': 0,
        'Block points': 0,
        'Fouls': 0,
        'Cards': 0,
        'Defense errors': 0,
        'Receive errors': 0,
        'Attack errors': 0,
        'Serve errors': 0,
        'Block errors': 0,
        'Att%': 0,
        'Serve%': 0,
        'Block%': 0,
        'Def error contribution': 0,
        'Rec error contribution': 0,
        'Att error contribution': 0,
        'Serve error contribution': 0,
        'Block error contribution': 0,
        'Att point contribution': 0,
        'Serve point contribution': 0,
        'Block point contribution': 0

}




player_stats_single_2 = {
    'Scored points': [],
    'Lost points': [],
    'Aces': [],
    'Attack points': [],
    'Block points': [],
    'Fouls': [],
    'Cards': [],
    'Defense errors': [],
    'Receive errors': [],
    'Attack errors': [],
    'Serve errors': [],
    'Block errors': [],
    'Att%': [],
    'Serve%': [],
    'Block%': [],

}



team_stats = {
    
    'Scored points': 0,
    'Lost points': 0,
    'Aces': 0,
    'Attack points': 0,
    'Block points': 0,
    'Fouls': 0,
    'Cards': 0,
    'Defense errors': 0,
    'Receive errors': 0,
    'Attack errors': 0,
    'Serve errors': 0,
    'Block errors': 0,
    'Att%': 0,
    'Serve%': 0,
    'Block%': 0,
}

team_stats_single = {
    
    'Scored points': [],
    'Lost points': [],
    'Aces': [],
    'Attack points': [],
    'Block points': [],
    'Fouls': [],
    'Cards': [],
    'Defense errors': [],
    'Receive errors': [],
    'Attack errors': [],
    'Serve errors': [],
    'Block errors': [],
    'Att%': [],
    'Serve%': [],
    'Block%': [],
    
}

all_games = {}

#DATA EXTRACION 2
for file_names in excels:
        
        match_info = excels[file_names]['Info']
        match_set1 = excels[file_names]['Set 1']
        match_set2 = excels[file_names]['Set 2']
        match_set3 = excels[file_names]['Set 3']
        match_set4 = excels[file_names]['Set 4']
        match_set5 = excels[file_names]['Set 5']
        
        our_sets = 0
        opp_sets = 0
       
        #game date
        date = match_info.loc[1,'Data']
        date_ok = date.strftime('%d-%m-%Y')
        #opponent
        opp = match_info.loc[1,'Opponent']
        #final result
        if not(match_set1.empty) and (match_set1.iloc[-1]['our_score'] > match_set1.iloc[-1]['opp_score']):
            our_sets+=1
            our_point_set1 = match_set1.iloc[-1]['our_score']
            opp_point_set1 = match_set1.iloc[-1]['opp_score']
        elif not(match_set1.empty) and (match_set1.iloc[-1]['our_score'] < match_set1.iloc[-1]['opp_score']):
            opp_sets+=1
            our_point_set1 = match_set1.iloc[-1]['our_score']
            opp_point_set1 = match_set1.iloc[-1]['opp_score']

        if not(match_set2.empty) and (match_set2.iloc[-1]['our_score'] > match_set2.iloc[-1]['opp_score']):
            our_sets+=1
            our_point_set2 = match_set2.iloc[-1]['our_score']
            opp_point_set2 = match_set2.iloc[-1]['opp_score']
        elif not(match_set2.empty) and (match_set2.iloc[-1]['our_score'] < match_set2.iloc[-1]['opp_score']):
            opp_sets+=1
            our_point_set2 = match_set2.iloc[-1]['our_score']
            opp_point_set2 = match_set2.iloc[-1]['opp_score']

        if not(match_set3.empty) and (match_set3.iloc[-1]['our_score'] > match_set3.iloc[-1]['opp_score']):
            our_sets+=1
            our_point_set3 = match_set3.iloc[-1]['our_score']
            opp_point_set3 = match_set3.iloc[-1]['opp_score']
        elif not(match_set3.empty) and (match_set3.iloc[-1]['our_score'] < match_set3.iloc[-1]['opp_score']) :
            opp_sets+=1
            our_point_set3 = match_set3.iloc[-1]['our_score']
            opp_point_set3 = match_set3.iloc[-1]['opp_score']

        if not(match_set4.empty) and (match_set4.iloc[-1]['our_score'] > match_set4.iloc[-1]['opp_score']) :
            our_sets+=1
            our_point_set4 = match_set4.iloc[-1]['our_score']
            opp_point_set4 = match_set4.iloc[-1]['opp_score']
        elif not(match_set4.empty) and (match_set4.iloc[-1]['our_score'] < match_set4.iloc[-1]['opp_score']) :
            opp_sets+=1
            our_point_set4 = match_set4.iloc[-1]['our_score']
            opp_point_set4 = match_set4.iloc[-1]['opp_score']

        if not(match_set5.empty) and (match_set5.iloc[-1]['our_score'] > match_set5.iloc[-1]['opp_score']):
            our_sets+=1
            our_point_set5 = match_set5.iloc[-1]['our_score']
            opp_point_set5 = match_set5.iloc[-1]['opp_score']
        elif not(match_set5.empty) and (match_set5.iloc[-1]['our_score'] < match_set5.iloc[-1]['opp_score']):
            opp_sets+=1
            our_point_set5 = match_set5.iloc[-1]['our_score']
            opp_point_set5 = match_set5.iloc[-1]['opp_score']
        
        #game summary
        all_games[date_ok] = {}
        all_games[date_ok]['Date'] =  date_ok
        all_games[date_ok]['Opponent'] = opp
        all_games[date_ok]['Final result'] = [our_sets,opp_sets]
        if not match_set5.empty :
            all_games[date_ok]['Final points'] = [(our_point_set1,opp_point_set1), (our_point_set2,opp_point_set2),
                                                (our_point_set3,opp_point_set3),(our_point_set4,opp_point_set4),(our_point_set5,opp_point_set5)]
        elif not match_set4.empty and match_set5.empty :
            all_games[date_ok]['Final points'] = [(our_point_set1,opp_point_set1), (our_point_set2,opp_point_set2),
                                                (our_point_set3,opp_point_set3),(our_point_set4,opp_point_set4)]
        else:
            all_games[date_ok]['Final points'] = [(our_point_set1,opp_point_set1), (our_point_set2,opp_point_set2),
                                                (our_point_set3,opp_point_set3)]
        
        
        #team stats for overall
        all_match2 = pd.concat([match_set1,match_set2,match_set3,match_set4,match_set5])
        all_match2 = all_match2[all_match2['player'].notna()]

        #team stats
        
        team_stats['Fouls'] += len(all_match2[all_match2['point_type']=='foul'])
        team_stats['Cards'] += len(all_match2[all_match2['point_type']=='card'])
        team_stats['Scored points'] += len(all_match2[all_match2['score']=='S'])
        team_stats['Lost points'] += len(all_match2[all_match2['score']=='L'])
        team_stats['Aces'] += len(all_match2[(all_match2['score']=='S') & (all_match2['serve_zone'].notna())])
        team_stats['Attack points'] += len(all_match2[(all_match2['score']=='S') & (all_match2['attack_zone'].notna())])
        team_stats['Block points'] += len(all_match2[(all_match2['score']=='S') & (all_match2['block_zone'].notna())])
        team_stats['Defense errors'] += len(all_match2[(all_match2['score']=='L') & (all_match2['defense_zone'].notna()) & (all_match2['attack_zone'].notna())])
        team_stats['Receive errors'] += len(all_match2[(all_match2['score']=='L') & (all_match2['defense_zone'].notna()) & (all_match2['serve_zone'].notna())])
        team_stats['Attack errors'] += len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'team error') & (all_match2['attack_zone'].notna())])
        team_stats['Serve errors'] += len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'team error') & (all_match2['serve_zone'].notna())])
        team_stats['Block errors'] += len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'opp point') & (all_match2['block_zone'].notna())])


        fouls= len(all_match2[all_match2['point_type']=='foul'])
        team_stats_single['Fouls'].append(fouls)
        cards= len(all_match2[all_match2['point_type']=='card'])
        team_stats_single['Cards'].append(cards)
        scored_points= len(all_match2[all_match2['score']=='S'])
        team_stats_single['Scored points'].append(scored_points)
        lost_points= len(all_match2[all_match2['score']=='L'])
        team_stats_single['Lost points'].append(lost_points)
        aces= len(all_match2[(all_match2['score']=='S') & (all_match2['serve_zone'].notna())])
        team_stats_single['Aces'].append(aces)
        attack_points= len(all_match2[(all_match2['score']=='S') & (all_match2['attack_zone'].notna())])
        team_stats_single['Attack points'].append(attack_points)
        block_points= len(all_match2[(all_match2['score']=='S') & (all_match2['block_zone'].notna())])
        team_stats_single['Block points'].append(block_points)
        defense_errors= len(all_match2[(all_match2['score']=='L') & (all_match2['defense_zone'].notna()) & (all_match2['attack_zone'].notna())])
        team_stats_single['Defense errors'].append(defense_errors)
        receive_errors= len(all_match2[(all_match2['score']=='L') & (all_match2['defense_zone'].notna()) & (all_match2['serve_zone'].notna())])
        team_stats_single['Receive errors'].append(receive_errors)
        attack_errors= len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'team error') & (all_match2['attack_zone'].notna())])
        team_stats_single['Attack errors'].append(attack_errors)
        serve_errors= len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'team error') & (all_match2['serve_zone'].notna())])
        team_stats_single['Serve errors'].append(serve_errors)
        block_errors= len(all_match2[(all_match2['score']=='L') & (all_match2['point_type'] == 'opp point') & (all_match2['block_zone'].notna())])
        team_stats_single['Block errors'].append(block_errors)
        



if (team_stats['Attack points']+team_stats['Attack errors']) !=0:
    team_stats['Att%'] =  team_stats['Attack points']/(team_stats['Attack points']+team_stats['Attack errors'])*100
else:
    team_stats['Att%'] = 0
if (team_stats['Aces']+team_stats['Serve errors']) !=0:
    team_stats['Serve%'] =  team_stats['Aces']/(team_stats['Aces']+team_stats['Serve errors'])*100
else:
    team_stats['Serve%'] = 0
if (team_stats['Block points']+team_stats['Block errors']) !=0:
    team_stats['Block%'] =  team_stats['Block points']/(team_stats['Block points']+team_stats['Block errors'])*100
else:
    team_stats['Block%'] = 0
 


p_ss = dict(list(team_stats_single.items())[:12])
p_ss = pd.DataFrame(p_ss)



for index, row in p_ss.iterrows():

    if (row['Attack points']+ row['Attack errors']) !=0:
        team_stats_single['Att%'].append(row['Attack points']/(row['Attack points']+row['Attack errors'])*100)
    else:
        team_stats_single['Att%'].append(0)
    if (row['Aces']+row['Serve errors']) !=0:
        team_stats_single['Serve%'].append(row['Aces']/(row['Aces']+row['Serve errors'])*100)
    else:
        team_stats_single['Serve%'].append(0)
    if (row['Block points']+row['Block errors']) !=0:
        team_stats_single['Block%'].append(row['Block points']/(row['Block points']+row['Block errors'])*100)
    else:
        team_stats_single['Block%'].append(0)
    




#CHOICE OF WHAT TO SEE
st.session_state.fundamental_type = st.segmented_control("Choose the type of fundamental:", ["overall","attack","serve","block","defense","receive"])


game_labels = []
for dates in all_games:
    label = f"{all_games[dates]['Date']} : {all_games[dates]['Opponent']} {all_games[dates]['Final result']}"
    game_labels.append(label)
game_labels.append('all games')
#################################################################################################à

if st.session_state.fundamental_type == "overall":
    

    col1,col2 = st.columns([0.6,0.4])
    with col1:
        compare_button = st.toggle("Compare with another player")
        
        if compare_button:
            st.session_state.player_2 = st.selectbox("Second player:",st.session_state.roster['Name'], placeholder="Second player...")
            
            for file_names in excels:
        
                match_info = excels[file_names]['Info']
                match_set1 = excels[file_names]['Set 1']
                match_set2 = excels[file_names]['Set 2']
                match_set3 = excels[file_names]['Set 3']
                match_set4 = excels[file_names]['Set 4']
                match_set5 = excels[file_names]['Set 5']
                
                
                #player and team stats for overall
                all_match_p2 = pd.concat([match_set1,match_set2,match_set3,match_set4,match_set5])

                #player stats
                all_match_p2 = all_match_p2[all_match_p2['player'] == st.session_state.player_2]
                if not all_match_p2.empty:
                    player_2_stats['Played matches'] += 1

                player_2_stats['Fouls'] += len(all_match_p2[all_match_p2['point_type']=='foul'])
                player_2_stats['Cards'] += len(all_match_p2[all_match_p2['point_type']=='card'])
                player_2_stats['Scored points'] += len(all_match_p2[all_match_p2['score']=='S'])
                player_2_stats['Lost points'] += len(all_match_p2[all_match_p2['score']=='L'])
                player_2_stats['Aces'] += len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['serve_zone'].notna())])
                player_2_stats['Attack points'] += len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['attack_zone'].notna())])
                player_2_stats['Block points'] += len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['block_zone'].notna())])
                player_2_stats['Defense errors'] += len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['defense_zone'].notna()) & (all_match_p2['attack_zone'].notna())])
                player_2_stats['Receive errors'] += len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['defense_zone'].notna()) & (all_match_p2['serve_zone'].notna())])
                player_2_stats['Attack errors'] += len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'team error') & (all_match_p2['attack_zone'].notna())])
                player_2_stats['Serve errors'] += len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'team error') & (all_match_p2['serve_zone'].notna())])
                player_2_stats['Block errors'] += len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'opp point') & (all_match_p2['block_zone'].notna())])
                
                fouls_2= len(all_match_p2[all_match_p2['point_type']=='foul'])
                player_stats_single_2['Fouls'].append(fouls_2)
                cards_2= len(all_match_p2[all_match_p2['point_type']=='card'])
                player_stats_single_2['Cards'].append(cards_2)
                scored_points_2= len(all_match_p2[all_match_p2['score']=='S'])
                player_stats_single_2['Scored points'].append(scored_points_2)
                lost_points_2= len(all_match_p2[all_match_p2['score']=='L'])
                player_stats_single_2['Lost points'].append(lost_points_2)
                aces_2= len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['serve_zone'].notna())])
                player_stats_single_2['Aces'].append(aces_2)
                attack_points_2= len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['attack_zone'].notna())])
                player_stats_single_2['Attack points'].append(attack_points_2)
                block_points_2= len(all_match_p2[(all_match_p2['score']=='S') & (all_match_p2['block_zone'].notna())])
                player_stats_single_2['Block points'].append(block_points_2)
                defense_errors_2= len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['defense_zone'].notna()) & (all_match_p2['attack_zone'].notna())])
                player_stats_single_2['Defense errors'].append(defense_errors_2)
                receive_errors_2= len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['defense_zone'].notna()) & (all_match_p2['serve_zone'].notna())])
                player_stats_single_2['Receive errors'].append(receive_errors_2)
                attack_errors_2= len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'team error') & (all_match_p2['attack_zone'].notna())])
                player_stats_single_2['Attack errors'].append(attack_errors_2)
                serve_errors_2= len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'team error') & (all_match_p2['serve_zone'].notna())])
                player_stats_single_2['Serve errors'].append(serve_errors_2)
                block_errors_2= len(all_match_p2[(all_match_p2['score']=='L') & (all_match_p2['point_type'] == 'opp point') & (all_match_p2['block_zone'].notna())])
                player_stats_single_2['Block errors'].append(block_errors_2)



            if (player_2_stats['Attack points']+player_2_stats['Attack errors']) !=0:
                player_2_stats['Att%'] =  player_2_stats['Attack points']/(player_2_stats['Attack points']+player_2_stats['Attack errors'])*100
            else:
                player_2_stats['Att%'] = 0
            if (player_2_stats['Aces']+player_2_stats['Serve errors']) !=0:
                player_2_stats['Serve%'] =  player_2_stats['Aces']/(player_2_stats['Aces']+player_2_stats['Serve errors'])*100
            else:
                player_2_stats['Serve%'] = 0
            if (player_2_stats['Block points']+player_2_stats['Block errors']) !=0:
                player_2_stats['Block%'] =  player_2_stats['Block points']/(player_2_stats['Block points']+player_2_stats['Block errors'])*100
            else:
                player_2_stats['Block%'] = 0
            

            
            p_ss2 = dict(list(player_stats_single_2.items())[:12])
            p_ss2 = pd.DataFrame(p_ss2)
            

            for index, row in p_ss2.iterrows():

                if (row['Attack points']+ row['Attack errors']) !=0:
                    player_stats_single_2['Att%'].append(row['Attack points']/(row['Attack points']+row['Attack errors'])*100)
                else:
                    player_stats_single_2['Att%'].append(0)
                if (row['Aces']+row['Serve errors']) !=0:
                    player_stats_single_2['Serve%'].append(row['Aces']/(row['Aces']+row['Serve errors'])*100)
                else:
                    player_stats_single_2['Serve%'].append(0)
                if (row['Block points']+row['Block errors']) !=0:
                    player_stats_single_2['Block%'].append(row['Block points']/(row['Block points']+row['Block errors'])*100)
                else:
                    player_stats_single_2['Block%'].append(0)
                
            radar_chart = make_player_2_radar_chart("Team",st.session_state.player_2, team_stats, player_2_stats)
            
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="The resulting shape of this radar chart gives a visual snapshot of strengths and weaknesses of the team over these three parameters. On the background is the representation of the ideal performance.
	                    - Att%: (team’s attack points)/(team’s attack points + team’s attack errors)*100
                        - Serve%: (team's aces)/(team’s aces + team's serve errors)*100
                        - Block%: (team’s block points)/(team’s block points + team’s block errors)*100">
                    Overall performance radar plot
                </span>
                """,
                unsafe_allow_html=True
            )

            st.plotly_chart(radar_chart)
        
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="The graph displays the relationship between two variables. It shows individual points plotted on a Cartesian coordinate system where each one shows the values of both variables for a specific observation. Variables can be freely chosen.">
                    Comparative statistics scatter plot
                </span>
                """,
                unsafe_allow_html=True
            )

            x_var = st.selectbox("Select the x-variable:",team_stats_single,placeholder="Select the x-variable...")
            y_var = st.selectbox("Select the y-variable:",team_stats_single,placeholder="Select the y-variable...")
            
            df1 = pd.DataFrame(team_stats_single)
            df1['Name'] = "Team"

            df2 = pd.DataFrame(player_stats_single_2)
            df2['Name'] = st.session_state.player_2

            chart1 = alt.Chart(pd.DataFrame(df1)).mark_circle(color="green",size=100).encode(x=x_var, y=y_var,tooltip=["Name",x_var,y_var])
            chart2 = alt.Chart(pd.DataFrame(df2)).mark_circle(color="orange",size=100).encode(x=x_var, y=y_var, tooltip=["Name",x_var,y_var])

            combined_chart = alt.layer(chart1, chart2).interactive()

            
            st.altair_chart(combined_chart)


        else:
            radar_chart = make_player_radar_chart("Team", team_stats)

            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="The resulting shape of this radar chart gives a visual snapshot of strengths and weaknesses of the team over these three parameters. On the background is the representation of the ideal performance.
	                    - Att%: (team’s attack points)/(team’s attack points + team’s attack errors)*100
                        - Serve%: (team's aces)/(team’s aces + team's serve errors)*100
                        - Block%: (team’s block points)/(team’s block points + team’s block errors)*100">
                    Overall performance radar plot
                </span>
                """,
                unsafe_allow_html=True
            ) 

            st.plotly_chart(radar_chart)

            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="The graph displays the relationship between two variables. It shows individual points plotted on a Cartesian coordinate system where each one shows the values of both variables for a specific observation. Variables can be freely chosen.">
                    Comparative statistics scatter plot
                </span>
                """,
                unsafe_allow_html=True
            )

            x_var = st.selectbox("Select the x-variable:",team_stats_single,placeholder="Select the x-variable...")
            y_var = st.selectbox("Select the y-variable:",team_stats_single,placeholder="Select the y-variable...")
            
            df1 = pd.DataFrame(team_stats_single)
            df1['Name'] = "Team"

            chart1 = alt.Chart(pd.DataFrame(df1)).mark_circle(color="green", size=100).encode(x=x_var, y=y_var,tooltip=["Name",x_var,y_var])
            
            st.altair_chart(chart1)
            
    
    with col2:
        player_stats_df = pd.DataFrame(team_stats, index=[0])

        player_stats_df = player_stats_df.T
        player_stats_df = player_stats_df.rename(columns={0: "Value"})  
        player_stats_df['General Stats'] = player_stats_df.index

        cols = ['General Stats', 'Value']
        player_stats_df = player_stats_df[cols]

        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")
        st.write("\n\n")


        st.dataframe(player_stats_df.head(7), hide_index=True)

############################################################################################

if st.session_state.fundamental_type == "attack":
    
    st.session_state.game_choice = st.selectbox("Select a game:",game_labels, placeholder='Select a game...')
    
    #caso di selezione di tutti i game
    if st.session_state.game_choice == 'all games':
        
        match_conc = pd.DataFrame()
        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        
        for file_names in excels:
        
            match1 = excels[file_names]['Set 1']
            match2 = excels[file_names]['Set 2']
            match3 = excels[file_names]['Set 3']
            match4 = excels[file_names]['Set 4']
            match5 = excels[file_names]['Set 5']

            match_conc = pd.concat([match_conc,match1,match2,match3,match4,match5])
            set1 = pd.concat([set1,match1])
            set2 = pd.concat([set2,match2])
            set3 = pd.concat([set3,match3])
            set4 = pd.concat([set4,match4])
            set5 = pd.concat([set5,match5])

            if not match1.empty:
                n1 +=1
            if not match2.empty:
                n2 +=1
            if not match3.empty:
                n3 +=1
            if not match4.empty:
                n4 +=1
            if not match5.empty:
                n5 +=1
    
        
    #caso di selezione di game singolo
    else:
        

        #info visualization
        match_index = game_labels.index(st.session_state.game_choice)
        
        df_games = pd.DataFrame.from_dict(all_games, orient="index")
        
        result_visualization(df_games,match_index)
                

        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()
        
        n1 = 1
        n2 = 1
        n3 = 1
        n4 = 1
        n5 = 1

        match = excels.iloc[:,match_index]

        match1 = match['Set 1']
        match2 = match['Set 2']
        match3 = match['Set 3']
        match4 = match['Set 4']
        match5 = match['Set 5']

        match_conc = pd.concat([match1,match2,match3,match4,match5])
        set1 = match1
        set2 = match2
        set3 = match3
        set4 = match4
        set5 = match5

        #INSTANCE CHART
        set11 = match1
        set22 = match2
        set33 = match3
        set44 = match4
        set55 = match5
        
        set11['n_set']=1
        set22['n_set']=2
        set33['n_set']=3
        set44['n_set']=4
        set55['n_set']=5

        inst_df = pd.concat([set11,set22,set33,set44,set55]).reset_index(drop=True)
        
         
        

    #CHARTS
    focus = match_conc[match_conc['player'].notna()]
    
    focus_att = focus[focus['attack_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":

        if st.session_state.game_choice != 'all games':

            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )

            match_history_att_point(inst_df)

        #COURT CHART
        focus_att = focus_att[(focus_att['score'] == 'S') & (focus_att['point_type'] == 'team point')]
        
        att = pd.DataFrame({
            'start_att' : focus_att['attack_zone'].str.extract(r'att_(\d+)')[0].dropna().astype(int),
            'end_att' : focus_att['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        att = att.reset_index(drop=True)

        #crea vettore con frequenza zone di attacco
        frequenza_attacchi = att['start_att'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_difese = att['end_att'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(att['start_att'], att['end_att'], normalize=True)

        st.markdown(
        """
        <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
        title="This chart is a discrete heatmap, showing the team’s attack distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
            Attack distribution chart
        </span>
        """,
        unsafe_allow_html=True
        )

        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_attack_frequency(frequenza_attacchi,frequenza_difese,frequenza_transizioni, soglia_freq=min_frequenza_threshold)
        

        #BAR CHART
        set1_att = set1[set1['player'].notna()]
        att_p1 = len(set1_att[(set1_att['point_type'] == 'team point') & (set1_att['attack_zone'].notna())])
        if n1 !=0:
            att_p1 = att_p1/n1
        else:
            att_p1 = 0
        set2_att = set2[set2['player'].notna()]
        att_p2 = len(set2_att[(set2_att['point_type'] == 'team point') & (set2_att['attack_zone'].notna())])
        if n2 !=0:
            att_p2 = att_p2/n2
        else:
            att_p2 = 0
        set3_att = set3[set3['player'].notna()]
        att_p3 = len(set3_att[(set3_att['point_type'] == 'team point') & (set3_att['attack_zone'].notna())])
        if n3 !=0:
            att_p3 = att_p3/n3
        else:
            att_p3 = 0
        set4_att = set4[set4['player'].notna()]
        att_p4 = len(set4_att[(set4_att['point_type'] == 'team point') & (set4_att['attack_zone'].notna())])
        if n4 !=0:
            att_p4 = att_p4/n4
        else:
            att_p4 = 0
        set5_att = set5[set5['player'].notna()]
        att_p5 = len(set5_att[(set5_att['point_type'] == 'team point') & (set5_att['attack_zone'].notna())])
        if n5 !=0:
            att_p5 = att_p5/n5
        else:
            att_p5 = 0

    
        att_e1 = len(set1_att[(set1_att['point_type'] == 'team error') & (set1_att['attack_zone'].notna())])
        if n1 !=0:
            att_e1 = att_e1/n1
        else:
            att_e1 = 0
        att_e2 = len(set2_att[(set2_att['point_type'] == 'team error') & (set2_att['attack_zone'].notna())])
        if n2 !=0:
            att_e2 = att_e2/n2
        else:
            att_e2 = 0
        att_e3 = len(set3_att[(set3_att['point_type'] == 'team error') & (set3_att['attack_zone'].notna())])
        if n3 !=0:
            att_e3 = att_e3/n3
        else:
            att_e3 = 0
        att_e4 = len(set4_att[(set4_att['point_type'] == 'team error') & (set4_att['attack_zone'].notna())])
        if n4 !=0:
            att_e4 = att_e4/n4
        else:
            att_e4 = 0
        att_e5 = len(set5_att[(set5_att['point_type'] == 'team error') & (set5_att['attack_zone'].notna())])
        if n5 !=0:
            att_e5 = att_e5/n5
        else:
            att_e5 = 0
        
        bar_att = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [att_p1, att_p2, att_p3, att_p4, att_p5],
            'Mean errors x set' : [att_e1, att_e2, att_e3, att_e4, att_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Attack-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_points(bar_att)

        



    elif st.session_state.info_type == "errors":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_att_error(inst_df)

        #COURT CHART
        focus_att = focus_att[(focus_att['score'] == 'L') & (focus_att['point_type'] == 'team error')]
        temp_index = pd.RangeIndex(len(focus_att))
        focus_att = focus_att.set_axis(temp_index)
        
        block_zone_extracted = focus_att['block_zone'].str.extract(r'block_net_(\d+)')[0].dropna().astype(int)

        out_zone_mapping = {
            'out_1': 1,
            'out_5': 5,
            'out_6': 6,
            'out_left': 7, 
            'out_right': 8 
        }

        out_zone_extracted_raw = focus_att['out_zone'].map(out_zone_mapping).dropna().astype(int, errors='ignore')

        start_att = focus_att['attack_zone'].str.extract(r'att_(\d+)')[0].dropna().astype(int)

        end_att_block = block_zone_extracted.reindex(start_att.index)
        end_att_out = out_zone_extracted_raw.reindex(start_att.index)

        end_att = pd.concat([end_att_block, end_att_out]).dropna().astype(int)
        att = pd.DataFrame({'start_att': start_att, 'end_att': end_att})

        att = att.dropna(subset=['end_att']).astype(int)
        att = att.reset_index(drop=True)
        
        #crea vettore con frequenza zone di attacco
        frequenza_attacchi = att['start_att'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_difese = att['end_att'].value_counts(normalize=True).sort_index().reindex(range(1, 9), fill_value=0)
        frequenza_transizioni = pd.crosstab(att['start_att'], att['end_att'], normalize=True)
    
        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s attack distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
                Attack distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_attack_frequency(frequenza_attacchi,frequenza_difese,frequenza_transizioni, soglia_freq=min_frequenza_threshold)
        

        #BAR CHART
        set1_att = set1[set1['player'].notna()]
        att_p1 = len(set1_att[(set1_att['point_type'] == 'team point') & (set1_att['attack_zone'].notna())])
        if n1 !=0:
            att_p1 = att_p1/n1
        else:
            att_p1 = 0
        set2_att = set2[set2['player'].notna()]
        att_p2 = len(set2_att[(set2_att['point_type'] == 'team point') & (set2_att['attack_zone'].notna())])
        if n2 !=0:
            att_p2 = att_p2/n2
        else:
            att_p2 = 0
        set3_att = set3[set3['player'].notna()]
        att_p3 = len(set3_att[(set3_att['point_type'] == 'team point') & (set3_att['attack_zone'].notna())])
        if n3 !=0:
            att_p3 = att_p3/n3
        else:
            att_p3 = 0
        set4_att = set4[set4['player'].notna()]
        att_p4 = len(set4_att[(set4_att['point_type'] == 'team point') & (set4_att['attack_zone'].notna())])
        if n4 !=0:
            att_p4 = att_p4/n4
        else:
            att_p4 = 0
        set5_att = set5[set5['player'].notna()]
        att_p5 = len(set5_att[(set5_att['point_type'] == 'team point') & (set5_att['attack_zone'].notna())])
        if n5 !=0:
            att_p5 = att_p5/n5
        else:
            att_p5 = 0

    
        att_e1 = len(set1_att[(set1_att['point_type'] == 'team error') & (set1_att['attack_zone'].notna())])
        if n1 !=0:
            att_e1 = att_e1/n1
        else:
            att_e1 = 0
        att_e2 = len(set2_att[(set2_att['point_type'] == 'team error') & (set2_att['attack_zone'].notna())])
        if n2 !=0:
            att_e2 = att_e2/n2
        else:
            att_e2 = 0
        att_e3 = len(set3_att[(set3_att['point_type'] == 'team error') & (set3_att['attack_zone'].notna())])
        if n3 !=0:
            att_e3 = att_e3/n3
        else:
            att_e3 = 0
        att_e4 = len(set4_att[(set4_att['point_type'] == 'team error') & (set4_att['attack_zone'].notna())])
        if n4 !=0:
            att_e4 = att_e4/n4
        else:
            att_e4 = 0
        att_e5 = len(set5_att[(set5_att['point_type'] == 'team error') & (set5_att['attack_zone'].notna())])
        if n5 !=0:
            att_e5 = att_e5/n5
        else:
            att_e5 = 0
        
        bar_att = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [att_p1, att_p2, att_p3, att_p4, att_p5],
            'Mean errors x set' : [att_e1, att_e2, att_e3, att_e4, att_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Attack-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_errors(bar_att)

#######################################################################################

if st.session_state.fundamental_type == "serve":

    st.session_state.game_choice = st.selectbox("Select a game:",game_labels, placeholder='Select a game...')
    
    #caso di selezione di tutti i game
    if st.session_state.game_choice == 'all games':
        
        match_conc = pd.DataFrame()
        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        
        for file_names in excels:
        
            match1 = excels[file_names]['Set 1']
            match2 = excels[file_names]['Set 2']
            match3 = excels[file_names]['Set 3']
            match4 = excels[file_names]['Set 4']
            match5 = excels[file_names]['Set 5']

            match_conc = pd.concat([match_conc,match1,match2,match3,match4,match5])
            set1 = pd.concat([set1,match1])
            set2 = pd.concat([set2,match2])
            set3 = pd.concat([set3,match3])
            set4 = pd.concat([set4,match4])
            set5 = pd.concat([set5,match5])

            if not match1.empty:
                n1 +=1
            if not match2.empty:
                n2 +=1
            if not match3.empty:
                n3 +=1
            if not match4.empty:
                n4 +=1
            if not match5.empty:
                n5 +=1
    
        
    #caso di selezione di game singolo
    else: 


        #info visualization
        match_index = game_labels.index(st.session_state.game_choice)
        
        df_games = pd.DataFrame.from_dict(all_games, orient="index")
        
        result_visualization(df_games,match_index)

        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()
        
        n1 = 1
        n2 = 1
        n3 = 1
        n4 = 1
        n5 = 1

        match = excels.iloc[:,match_index]

        match1 = match['Set 1']
        match2 = match['Set 2']
        match3 = match['Set 3']
        match4 = match['Set 4']
        match5 = match['Set 5']

        match_conc = pd.concat([match1,match2,match3,match4,match5])
        set1 = match1
        set2 = match2
        set3 = match3
        set4 = match4
        set5 = match5

        #INSTANCE CHART
        set11 = match1
        set22 = match2
        set33 = match3
        set44 = match4
        set55 = match5
        
        set11['n_set']=1
        set22['n_set']=2
        set33['n_set']=3
        set44['n_set']=4
        set55['n_set']=5

        inst_df = pd.concat([set11,set22,set33,set44,set55]).reset_index(drop=True)

    #COURT CHART  
    focus = match_conc[match_conc['player'].notna()]
    
    focus_serve = focus[focus['serve_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_serve_point(inst_df)

        focus_serve = focus_serve[(focus_serve['score'] == 'S') & (focus_serve['point_type'] == 'team point')]
        
        serve = pd.DataFrame({
            'start_serve' : focus_serve['serve_zone'].str.extract(r'serve_(\d+)')[0].dropna().astype(int),
            'end_serve' : focus_serve['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        serve = serve.reset_index(drop=True)

        #crea vettore con frequenza zone di servizio
        frequenza_servizi = serve['start_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_ace = serve['end_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(serve['start_serve'], serve['end_serve'], normalize=True)

        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s serve distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
                Serve distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )


        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_serve_frequency(frequenza_servizi,frequenza_ace,frequenza_transizioni, soglia_freq=min_frequenza_threshold)
        

        #BAR CHART
        set1_serve = set1[set1['player'].notna()]
        serve_p1 = len(set1_serve[(set1_serve['point_type'] == 'team point') & (set1_serve['serve_zone'].notna())])
        if n1 !=0:
            serve_p1 = serve_p1/n1
        else:
            serve_p1 = 0
        set2_serve = set2[set2['player'].notna()]
        serve_p2 = len(set2_serve[(set2_serve['point_type'] == 'team point') & (set2_serve['serve_zone'].notna())])
        if n2 !=0:
            serve_p2 = serve_p2/n2
        else:
            serve_p2 = 0
        set3_serve = set3[set3['player'].notna()]
        serve_p3 = len(set3_serve[(set3_serve['point_type'] == 'team point') & (set3_serve['serve_zone'].notna())])
        if n3 !=0:
            serve_p3 = serve_p3/n3
        else:
            serve_p3 = 0
        set4_serve = set4[set4['player'].notna()]
        serve_p4 = len(set4_serve[(set4_serve['point_type'] == 'team point') & (set4_serve['serve_zone'].notna())])
        if n4 !=0:
            serve_p4 = serve_p4/n4
        else:
            serve_p4 = 0
        set5_serve = set5[set5['player'].notna()]
        serve_p5 = len(set5_serve[(set5_serve['point_type'] == 'team point') & (set5_serve['serve_zone'].notna())])
        if n5 !=0:
            serve_p5 = serve_p5/n5
        else:
            serve_p5 = 0

    
        serve_e1 = len(set1_serve[(set1_serve['point_type'] == 'team error') & (set1_serve['serve_zone'].notna())])
        if n1 !=0:
            serve_e1 = serve_e1/n1
        else:
            serve_e1 = 0
        serve_e2 = len(set2_serve[(set2_serve['point_type'] == 'team error') & (set2_serve['serve_zone'].notna())])
        if n2 !=0:
            serve_e2 = serve_e2/n2
        else:
            serve_e2 = 0
        serve_e3 = len(set3_serve[(set3_serve['point_type'] == 'team error') & (set3_serve['serve_zone'].notna())])
        if n3 !=0:
            serve_e3 = serve_e3/n3
        else:
            serve_e3 = 0
        serve_e4 = len(set4_serve[(set4_serve['point_type'] == 'team error') & (set4_serve['serve_zone'].notna())])
        if n4 !=0:
            serve_e4 = serve_e4/n4
        else:
            serve_e4 = 0
        serve_e5 = len(set5_serve[(set5_serve['point_type'] == 'team error') & (set5_serve['serve_zone'].notna())])
        if n5 !=0:
            serve_e5 = serve_e5/n5
        else:
            serve_e5 = 0
        
        bar_serve = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [serve_p1, serve_p2, serve_p3, serve_p4, serve_p5],
            'Mean errors x set' : [serve_e1, serve_e2, serve_e3, serve_e4, serve_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Serve-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_points(bar_serve)




    elif st.session_state.info_type == "errors":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )   
            match_history_serve_error(inst_df)


        focus_serve = focus_serve[(focus_serve['score'] == 'L') & (focus_serve['point_type'] == 'team error')]
        temp_index = pd.RangeIndex(len(focus_serve))
        focus_serve = focus_serve.set_axis(temp_index)

        block_zone_extracted = focus_serve['block_zone'].str.extract(r'block_net_(\d+)')[0].dropna().astype(int)

        out_zone_mapping = {
            'out_1': 1,
            'out_5': 5,
            'out_6': 6,
            'out_left': 7, 
            'out_right': 8 
        }

        out_zone_extracted_raw = focus_serve['out_zone'].map(out_zone_mapping).dropna().astype(int, errors='ignore')
        start_serve = focus_serve['serve_zone'].str.extract(r'serve_(\d+)')[0].dropna().astype(int)
        end_serve_block = block_zone_extracted.reindex(start_serve.index)
        end_serve_out = out_zone_extracted_raw.reindex(start_serve.index)

        end_serve = pd.concat([end_serve_block, end_serve_out]).dropna().astype(int)
        serve = pd.DataFrame({'start_serve': start_serve, 'end_serve': end_serve})

        serve = serve.dropna(subset=['end_serve']).astype(int)
        serve = serve.reset_index(drop=True)
        
        #crea vettore con frequenza zone di attacco
        frequenza_servizi = serve['start_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_ace = serve['end_serve'].value_counts(normalize=True).sort_index().reindex(range(1, 9), fill_value=0)
        frequenza_transizioni = pd.crosstab(serve['start_serve'], serve['end_serve'], normalize=True)
    
        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s serve distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
                Serve distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_serve_frequency(frequenza_servizi,frequenza_ace,frequenza_transizioni, soglia_freq=min_frequenza_threshold)
        


        #BAR CHART
        set1_serve = set1[set1['player'].notna()]
        serve_p1 = len(set1_serve[(set1_serve['point_type'] == 'team point') & (set1_serve['serve_zone'].notna())])
        if n1 !=0:
            serve_p1 = serve_p1/n1
        else:
            serve_p1 = 0
        set2_serve = set2[set2['player'].notna()]
        serve_p2 = len(set2_serve[(set2_serve['point_type'] == 'team point') & (set2_serve['serve_zone'].notna())])
        if n2 !=0:
            serve_p2 = serve_p2/n2
        else:
            serve_p2 = 0
        set3_serve = set3[set3['player'].notna()]
        serve_p3 = len(set3_serve[(set3_serve['point_type'] == 'team point') & (set3_serve['serve_zone'].notna())])
        if n3 !=0:
            serve_p3 = serve_p3/n3
        else:
            serve_p3 = 0
        set4_serve = set4[set4['player'].notna()]
        serve_p4 = len(set4_serve[(set4_serve['point_type'] == 'team point') & (set4_serve['serve_zone'].notna())])
        if n4 !=0:
            serve_p4 = serve_p4/n4
        else:
            serve_p4 = 0
        set5_serve = set5[set5['player'].notna()]
        serve_p5 = len(set5_serve[(set5_serve['point_type'] == 'team point') & (set5_serve['serve_zone'].notna())])
        if n5 !=0:
            serve_p5 = serve_p5/n5
        else:
            serve_p5 = 0

    
        serve_e1 = len(set1_serve[(set1_serve['point_type'] == 'team error') & (set1_serve['serve_zone'].notna())])
        if n1 !=0:
            serve_e1 = serve_e1/n1
        else:
            serve_e1 = 0
        serve_e2 = len(set2_serve[(set2_serve['point_type'] == 'team error') & (set2_serve['serve_zone'].notna())])
        if n2 !=0:
            serve_e2 = serve_e2/n2
        else:
            serve_e2 = 0
        serve_e3 = len(set3_serve[(set3_serve['point_type'] == 'team error') & (set3_serve['serve_zone'].notna())])
        if n3 !=0:
            serve_e3 = serve_e3/n3
        else:
            serve_e3 = 0
        serve_e4 = len(set4_serve[(set4_serve['point_type'] == 'team error') & (set4_serve['serve_zone'].notna())])
        if n4 !=0:
            serve_e4 = serve_e4/n4
        else:
            serve_e4 = 0
        serve_e5 = len(set5_serve[(set5_serve['point_type'] == 'team error') & (set5_serve['serve_zone'].notna())])
        if n5 !=0:
            serve_e5 = serve_e5/n5
        else:
            serve_e5 = 0
        
        bar_serve = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [serve_p1, serve_p2, serve_p3, serve_p4, serve_p5],
            'Mean errors x set' : [serve_e1, serve_e2, serve_e3, serve_e4, serve_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Serve-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_errors(bar_serve)

######################################################################################

if st.session_state.fundamental_type == "block":

    st.session_state.game_choice = st.selectbox("Select a game:",game_labels, placeholder='Select a game...')
    
    #caso di selezione di tutti i game
    if st.session_state.game_choice == 'all games':
        
        match_conc = pd.DataFrame()
        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        
        for file_names in excels:
        
            match1 = excels[file_names]['Set 1']
            match2 = excels[file_names]['Set 2']
            match3 = excels[file_names]['Set 3']
            match4 = excels[file_names]['Set 4']
            match5 = excels[file_names]['Set 5']

            match_conc = pd.concat([match_conc,match1,match2,match3,match4,match5])
            set1 = pd.concat([set1,match1])
            set2 = pd.concat([set2,match2])
            set3 = pd.concat([set3,match3])
            set4 = pd.concat([set4,match4])
            set5 = pd.concat([set5,match5])

            if not match1.empty:
                n1 +=1
            if not match2.empty:
                n2 +=1
            if not match3.empty:
                n3 +=1
            if not match4.empty:
                n4 +=1
            if not match5.empty:
                n5 +=1
    
        
    #caso di selezione di game singolo
    else: 

        #info visualization
        match_index = game_labels.index(st.session_state.game_choice)
        
        df_games = pd.DataFrame.from_dict(all_games, orient="index")
        
        result_visualization(df_games,match_index)

        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()
        
        n1 = 1
        n2 = 1
        n3 = 1
        n4 = 1
        n5 = 1

        match = excels.iloc[:,match_index]

        match1 = match['Set 1']
        match2 = match['Set 2']
        match3 = match['Set 3']
        match4 = match['Set 4']
        match5 = match['Set 5']

        match_conc = pd.concat([match1,match2,match3,match4,match5])
        set1 = match1
        set2 = match2
        set3 = match3
        set4 = match4
        set5 = match5

        #INSTANCE CHART
        set11 = match1
        set22 = match2
        set33 = match3
        set44 = match4
        set55 = match5
        
        set11['n_set']=1
        set22['n_set']=2
        set33['n_set']=3
        set44['n_set']=4
        set55['n_set']=5

        inst_df = pd.concat([set11,set22,set33,set44,set55]).reset_index(drop=True)

    #COURT CHART  
    focus = match_conc[match_conc['player'].notna()]
    
    focus_block = focus[focus['block_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", ['points','errors'])
    
    if st.session_state.info_type == "points":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_block_point(inst_df)


        focus_block = focus_block[(focus_block['score'] == 'S') & (focus_block['point_type'] == 'team point')]

        block = pd.DataFrame({
            'start_block' : focus_block['block_zone'].str.extract(r'block_(\d+)')[0].dropna().astype(int),
        })

        block = block.reset_index(drop=True)
        
        frequenza_blocchi = block['start_block'].value_counts(normalize=True).sort_index().reindex(range(1, 5), fill_value=0)

        # Esegui la funzione per visualizzare il grafico

        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s block distribution on the field.">
                Block distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        plot_volleyball_block_frequency(frequenza_blocchi)


        #BAR CHART
        set1_block = set1[set1['player'].notna()]
        block_p1 = len(set1_block[(set1_block['point_type'] == 'team point') & (set1_block['block_zone'].notna())])
        if n1 !=0:
            block_p1 = block_p1/n1
        else:
            block_p1 = 0
        set2_block = set2[set2['player'].notna()]
        block_p2 = len(set2_block[(set2_block['point_type'] == 'team point') & (set2_block['block_zone'].notna())])
        if n2 !=0:
            block_p2 = block_p2/n2
        else:
            block_p2 = 0
        set3_block = set3[set3['player'].notna()]
        block_p3 = len(set3_block[(set3_block['point_type'] == 'team point') & (set3_block['block_zone'].notna())])
        if n3 !=0:
            block_p3 = block_p3/n3
        else:
            block_p3 = 0
        set4_block = set4[set4['player'].notna()]
        block_p4 = len(set4_block[(set4_block['point_type'] == 'team point') & (set4_block['block_zone'].notna())])
        if n4 !=0:
            block_p4 = block_p4/n4
        else:
            block_p4 = 0
        set5_block = set5[set5['player'].notna()]
        block_p5 = len(set5_block[(set5_block['point_type'] == 'team point') & (set5_block['block_zone'].notna())])
        if n5 !=0:
            block_p5 = block_p5/n5
        else:
            block_p5 = 0

    
        block_e1 = len(set1_block[(set1_block['point_type'] == 'opp point') & (set1_block['block_zone'].notna())])
        if n1 !=0:
            block_e1 = block_e1/n1
        else:
            block_e1 = 0
        block_e2 = len(set2_block[(set2_block['point_type'] == 'opp point') & (set2_block['block_zone'].notna())])
        if n2 !=0:
            block_e2 = block_e2/n2
        else:
            block_e2 = 0
        block_e3 = len(set3_block[(set3_block['point_type'] == 'opp point') & (set3_block['block_zone'].notna())])
        if n3 !=0:
            block_e3 = block_e3/n3
        else:
            block_e3 = 0
        block_e4 = len(set4_block[(set4_block['point_type'] == 'opp point') & (set4_block['block_zone'].notna())])
        if n4 !=0:
            block_e4 = block_e4/n4
        else:
            block_e4 = 0
        block_e5 = len(set5_block[(set5_block['point_type'] == 'opp point') & (set5_block['block_zone'].notna())])
        if n5 !=0:
            block_e5 = block_e5/n5
        else:
            block_e5 = 0
        
        bar_block = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [block_p1, block_p2, block_p3, block_p4, block_p5],
            'Mean errors x set' : [block_e1, block_e2, block_e3, block_e4, block_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Block-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_points(bar_block)
    



    elif st.session_state.info_type == "errors":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_block_error(inst_df)


        focus_block = focus_block[(focus_block['score'] == 'L') & (focus_block['point_type'] == 'opp point')]
        
        block = pd.DataFrame({
            'start_block' : focus_block['block_zone'].str.extract(r'block_(\d+)')[0].dropna().astype(int),
        })
        
        block = block.reset_index(drop=True)
        
        frequenza_blocchi = block['start_block'].value_counts(normalize=True).sort_index().reindex(range(1, 5), fill_value=0)

        # Esegui la funzione per visualizzare il grafico

        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s block distribution on the field.">
                Block distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        plot_volleyball_block_frequency(frequenza_blocchi)


        #BAR CHART
        set1_block = set1[set1['player'].notna()]
        block_p1 = len(set1_block[(set1_block['point_type'] == 'team point') & (set1_block['block_zone'].notna())])
        if n1 !=0:
            block_p1 = block_p1/n1
        else:
            block_p1 = 0
        set2_block = set2[set2['player'].notna()]
        block_p2 = len(set2_block[(set2_block['point_type'] == 'team point') & (set2_block['block_zone'].notna())])
        if n2 !=0:
            block_p2 = block_p2/n2
        else:
            block_p2 = 0
        set3_block = set3[set3['player'].notna()]
        block_p3 = len(set3_block[(set3_block['point_type'] == 'team point') & (set3_block['block_zone'].notna())])
        if n3 !=0:
            block_p3 = block_p3/n3
        else:
            block_p3 = 0
        set4_block = set4[set4['player'].notna()]
        block_p4 = len(set4_block[(set4_block['point_type'] == 'team point') & (set4_block['block_zone'].notna())])
        if n4 !=0:
            block_p4 = block_p4/n4
        else:
            block_p4 = 0
        set5_block = set5[set5['player'].notna()]
        block_p5 = len(set5_block[(set5_block['point_type'] == 'team point') & (set5_block['block_zone'].notna())])
        if n5 !=0:
            block_p5 = block_p5/n5
        else:
            block_p5 = 0

    
        block_e1 = len(set1_block[(set1_block['point_type'] == 'opp point') & (set1_block['block_zone'].notna())])
        if n1 !=0:
            block_e1 = block_e1/n1
        else:
            block_e1 = 0
        block_e2 = len(set2_block[(set2_block['point_type'] == 'opp point') & (set2_block['block_zone'].notna())])
        if n2 !=0:
            block_e2 = block_e2/n2
        else:
            block_e2 = 0
        block_e3 = len(set3_block[(set3_block['point_type'] == 'opp point') & (set3_block['block_zone'].notna())])
        if n3 !=0:
            block_e3 = block_e3/n3
        else:
            block_e3 = 0
        block_e4 = len(set4_block[(set4_block['point_type'] == 'opp point') & (set4_block['block_zone'].notna())])
        if n4 !=0:
            block_e4 = block_e4/n4
        else:
            block_e4 = 0
        block_e5 = len(set5_block[(set5_block['point_type'] == 'opp point') & (set5_block['block_zone'].notna())])
        if n5 !=0:
            block_e5 = block_e5/n5
        else:
            block_e5 = 0
        
        bar_block = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean points x set' : [block_p1, block_p2, block_p3, block_p4, block_p5],
            'Mean errors x set' : [block_e1, block_e2, block_e3, block_e4, block_e5],
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Block-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_errors(bar_block)

###########################################################################################

if st.session_state.fundamental_type == "defense":

    st.session_state.game_choice = st.selectbox("Select a game:",game_labels, placeholder='Select a game...')
    
    #caso di selezione di tutti i game
    if st.session_state.game_choice == 'all games':
        
        match_conc = pd.DataFrame()
        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        
        for file_names in excels:
        
            match1 = excels[file_names]['Set 1']
            match2 = excels[file_names]['Set 2']
            match3 = excels[file_names]['Set 3']
            match4 = excels[file_names]['Set 4']
            match5 = excels[file_names]['Set 5']

            match_conc = pd.concat([match_conc,match1,match2,match3,match4,match5])
            set1 = pd.concat([set1,match1])
            set2 = pd.concat([set2,match2])
            set3 = pd.concat([set3,match3])
            set4 = pd.concat([set4,match4])
            set5 = pd.concat([set5,match5])

            if not match1.empty:
                n1 +=1
            if not match2.empty:
                n2 +=1
            if not match3.empty:
                n3 +=1
            if not match4.empty:
                n4 +=1
            if not match5.empty:
                n5 +=1
    
        
    #caso di selezione di game singolo
    else:

        #info visualization
        match_index = game_labels.index(st.session_state.game_choice)
        
        df_games = pd.DataFrame.from_dict(all_games, orient="index")
        
        result_visualization(df_games,match_index)

        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()
        
        n1 = 1
        n2 = 1
        n3 = 1
        n4 = 1
        n5 = 1

        match_index = game_labels.index(st.session_state.game_choice)
        match = excels.iloc[:,match_index]

        match1 = match['Set 1']
        match2 = match['Set 2']
        match3 = match['Set 3']
        match4 = match['Set 4']
        match5 = match['Set 5']

        match_conc = pd.concat([match1,match2,match3,match4,match5])
        set1 = match1
        set2 = match2
        set3 = match3
        set4 = match4
        set5 = match5

        #INSTANCE CHART
        set11 = match1
        set22 = match2
        set33 = match3
        set44 = match4
        set55 = match5
        
        set11['n_set']=1
        set22['n_set']=2
        set33['n_set']=3
        set44['n_set']=4
        set55['n_set']=5

        inst_df = pd.concat([set11,set22,set33,set44,set55]).reset_index(drop=True)

    #COURT CHART  
    focus = match_conc[match_conc['player'].notna()]

    focus_defense = focus[focus['defense_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", 'errors')
    
    if st.session_state.info_type == "errors":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_defense_error(inst_df)

        focus_defense = focus_defense[(focus_defense['score'] == 'L') & (focus_defense['point_type'] == 'opp point') & (focus_defense['attack_zone'].notna())]

        defense = pd.DataFrame({
            'start_def' : focus_defense['attack_zone'].str.extract(r'att_(\d+)')[0].dropna().astype(int),
            'end_def' : focus_defense['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        defense = defense.reset_index(drop=True)
       
        #crea vettore con frequenza zone di attacco
        frequenza_attacchi = defense['start_def'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_difese = defense['end_def'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(defense['start_def'], defense['end_def'], normalize=True)

        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s defense errors distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
                Defense errors distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_defense_frequency(frequenza_attacchi,frequenza_difese,frequenza_transizioni, soglia_freq=min_frequenza_threshold)
        

        #BAR CHART
        set1_def = set1[set1['player'].notna()]
        def_e1 = len(set1_def[(set1_def['point_type'] == 'opp point') & (set1_def['attack_zone'].notna()) & (set1_def['defense_zone'].notna())])
        if n1 !=0:
            def_e1 = def_e1/n1
        else:
            def_e1 = 0

        set2_def = set2[set2['player'].notna()]
        def_e2 = len(set2_def[(set2_def['point_type'] == 'opp point') & (set2_def['attack_zone'].notna()) & (set2_def['defense_zone'].notna())])
        if n2 !=0:
            def_e2 = def_e2/n2
        else:
            def_e2 = 0

        set3_def = set3[set3['player'].notna()] 
        def_e3 = len(set3_def[(set3_def['point_type'] == 'opp point') & (set3_def['attack_zone'].notna()) & (set3_def['defense_zone'].notna())])
        if n3 !=0:
            def_e3 = def_e3/n3
        else:
            def_e3 = 0

        set4_def = set4[set4['player'].notna()]
        def_e4 = len(set4_def[(set4_def['point_type'] == 'opp point') & (set4_def['attack_zone'].notna()) & (set4_def['defense_zone'].notna())])
        if n4 !=0:
            def_e4 = def_e4/n4
        else:
            def_e4 = 0
        
        set5_def = set5[set5['player'].notna()]
        def_e5 = len(set5_def[(set5_def['point_type'] == 'opp point') & (set5_def['attack_zone'].notna()) & (set5_def['defense_zone'].notna())])
        if n5 !=0:
            def_e5 = def_e5/n5
        else:
            def_e5 = 0
        
        bar_def = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean errors x set' : [def_e1, def_e2, def_e3, def_e4, def_e5]
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Defense-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_def_errors(bar_def)

###################################################################################################ààà
    
if st.session_state.fundamental_type == "receive":

    st.session_state.game_choice = st.selectbox("Select a game:",game_labels, placeholder='Select a game...')
    
    #caso di selezione di tutti i game
    if st.session_state.game_choice == 'all games':
        
        match_conc = pd.DataFrame()
        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        
        for file_names in excels:
        
            match1 = excels[file_names]['Set 1']
            match2 = excels[file_names]['Set 2']
            match3 = excels[file_names]['Set 3']
            match4 = excels[file_names]['Set 4']
            match5 = excels[file_names]['Set 5']

            match_conc = pd.concat([match_conc,match1,match2,match3,match4,match5])
            set1 = pd.concat([set1,match1])
            set2 = pd.concat([set2,match2])
            set3 = pd.concat([set3,match3])
            set4 = pd.concat([set4,match4])
            set5 = pd.concat([set5,match5])

            if not match1.empty:
                n1 +=1
            if not match2.empty:
                n2 +=1
            if not match3.empty:
                n3 +=1
            if not match4.empty:
                n4 +=1
            if not match5.empty:
                n5 +=1
    
        
    #caso di selezione di game singolo
    else:

        #info visualization
        match_index = game_labels.index(st.session_state.game_choice)
        
        df_games = pd.DataFrame.from_dict(all_games, orient="index")
        
        result_visualization(df_games,match_index)

        set1 = pd.DataFrame()
        set2 = pd.DataFrame()
        set3 = pd.DataFrame()
        set4 = pd.DataFrame()
        set5 = pd.DataFrame()
        
        n1 = 1
        n2 = 1
        n3 = 1
        n4 = 1
        n5 = 1

        match = excels.iloc[:,match_index]

        match1 = match['Set 1']
        match2 = match['Set 2']
        match3 = match['Set 3']
        match4 = match['Set 4']
        match5 = match['Set 5']

        match_conc = pd.concat([match1,match2,match3,match4,match5])
        set1 = match1
        set2 = match2
        set3 = match3
        set4 = match4
        set5 = match5

        #INSTANCE CHART
        set11 = match1
        set22 = match2
        set33 = match3
        set44 = match4
        set55 = match5
        
        set11['n_set']=1
        set22['n_set']=2
        set33['n_set']=3
        set44['n_set']=4
        set55['n_set']=5

        inst_df = pd.concat([set11,set22,set33,set44,set55]).reset_index(drop=True)

    #COURT CHART  
    focus = match_conc[match_conc['player'].notna()]

    focus_receive = focus[focus['defense_zone'].notna()]

    st.session_state.info_type = st.segmented_control("Choose the type of parameter:", 'errors')
    
    if st.session_state.info_type == "errors":

        if st.session_state.game_choice != 'all games':
            st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="This chart is a summary of the game. It represents in chronological order all the points gained or lost by each player that took part in the match. The points gained in the selected fundamental are highlighted with green bars, the lost ones with red bars, while the grey bars represent the other events of the game related to other fundamentals.">
                    Match history
                </span>
                """,
                unsafe_allow_html=True
            )
            match_history_receive_error(inst_df)

        focus_receive = focus_receive[(focus_receive['score'] == 'L') & (focus_receive['point_type'] == 'opp point') & (focus_receive['serve_zone'].notna())]
        

        receive = pd.DataFrame({
            'start_rec' : focus_receive['serve_zone'].str.extract(r'serve_(\d+)')[0].dropna().astype(int),
            'end_rec' : focus_receive['defense_zone'].str.extract(r'def_(\d+)')[0].dropna().astype(int)

        })
        receive = receive.reset_index(drop=True)
        
        #crea vettore con frequenza zone di servizio
        frequenza_servizi = receive['start_rec'].value_counts(normalize=True).sort_index().reindex(range(1, 7), fill_value=0)
        frequenza_ace = receive['end_rec'].value_counts(normalize=True).sort_index().reindex(range(1, 11), fill_value=0)
        frequenza_transizioni = pd.crosstab(receive['start_rec'], receive['end_rec'], normalize=True)

        st.markdown(
            """
            <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
            title="This chart is a discrete heatmap, showing the team’s receive errors distribution on the field. The arrows represent the ball’s trajectory, and their size shows the frequency of the trajectory. Their number can be adjusted using the slider. ">
                Receive errors distribution chart
            </span>
            """,
            unsafe_allow_html=True
        )

        min_frequenza_threshold = st.slider(
            "Minimum ball trajectory frequency:",
            min_value=0.0,
            max_value=frequenza_transizioni.max().max() if not frequenza_transizioni.empty else 0.1,
            value=0.01,  # Valore predefinito
            step=0.001,
            format="%.3f"
        )

        # Esegui la funzione per visualizzare il grafico
        plot_volleyball_receive_frequency(frequenza_servizi,frequenza_ace,frequenza_transizioni, soglia_freq=min_frequenza_threshold)

        
        #BAR CHART
        set1_rec = set1[set1['player'].notna()]
        rec_e1 = len(set1_rec[(set1_rec['point_type'] == 'opp point') & (set1_rec['serve_zone'].notna()) & (set1_rec['defense_zone'].notna())])
        if n1 !=0:
            rec_e1 = rec_e1/n1
        else:
            rec_e1 = 0

        set2_rec = set2[set2['player'].notna()]
        rec_e2 = len(set2_rec[(set2_rec['point_type'] == 'opp point') & (set2_rec['serve_zone'].notna()) & (set2_rec['defense_zone'].notna())])
        if n2 !=0:
            rec_e2 = rec_e2/n2
        else:
            rec_e2 = 0

        set3_rec = set3[set3['player'].notna()] 
        rec_e3 = len(set3_rec[(set3_rec['point_type'] == 'opp point') & (set3_rec['serve_zone'].notna()) & (set3_rec['defense_zone'].notna())])
        if n3 !=0:
            rec_e3 = rec_e3/n3
        else:
            rec_e3 = 0

        set4_rec = set4[set4['player'].notna()]
        rec_e4 = len(set4_rec[(set4_rec['point_type'] == 'opp point') & (set4_rec['serve_zone'].notna()) & (set4_rec['defense_zone'].notna())])
        if n4 !=0:
            rec_e4 = rec_e4/n4
        else:
            rec_e4 = 0
        
        set5_rec = set5[set5['player'].notna()]
        rec_e5 = len(set5_rec[(set5_rec['point_type'] == 'opp point') & (set5_rec['serve_zone'].notna()) & (set5_rec['defense_zone'].notna())])
        if n5 !=0:
            rec_e5 = rec_e5/n5
        else:
            rec_e5 = 0
        
        bar_rec = pd.DataFrame({
            'Set': ['set 1', 'set 2', 'set 3', 'set 4', 'set 5'],
            'Mean errors x set' : [rec_e1, rec_e2, rec_e3, rec_e4, rec_e5]
        })
        st.markdown(
                """
                <span style="border-bottom:1px dotted #888; cursor:help; font-size:1.5em; font-weight:bold;"
                title="Based on the initial choice between points or errors, this bar chart shows the mean number of points gained or the mean number of errors per set, specific to the fundamental previously selected, by the team.">
                    Receive-per-set bar chart
                </span>
                """,
                unsafe_allow_html=True
        )
        bar_plot_def_errors(bar_rec)

###########################################################################################



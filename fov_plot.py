import matplotlib.pyplot as plt
import numpy as np
from tools import *
import math

def plot_camera_profile(photo, settings):
    
    # Calcolo altezza FOV in funzione della distanza
    def fov_height(d):
        return d * np.tan(np.radians(photo.fov_ang_v / 2))
    
    def fov_width(d):
        # Larghezza reale a distanza d
        return d * np.tan(np.radians(photo.fov_ang_h / 2))
    
    # Gestione caso far infinito
    far_is_infinite = math.isinf(photo.far)
    max_distance = 1.25*((photo.far if photo.far < photo.hyperfocal else photo.hyperfocal) if not far_is_infinite else photo.hyperfocal)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # --- Disegniamo triangolo FOV SOLO tra near e far ---
    d_fill = np.linspace(photo.near, photo.far if not far_is_infinite else max_distance, 500)
    h_fill = fov_height(d_fill)
    ax.fill_between(d_fill, -h_fill, h_fill, color='skyblue', alpha=0.3, label='FOV')
    
    # --- Bordi sempre visibili ---
    d_borders = np.linspace(0, max_distance, 500)
    h_borders = fov_height(d_borders)
    ax.plot(d_borders, h_borders, color='skyblue', linewidth=2)
    ax.plot(d_borders, -h_borders, color='skyblue', linewidth=2)
    
    # Se far infinito, disegniamo un rettangolo oltre iperfocale
    if far_is_infinite or settings.focus_distance_m >= photo.hyperfocal:
        rect_start = settings.focus_distance_m
        rect_end = max_distance
        h_rect = fov_height(photo.hyperfocal)
        ax.fill_between([rect_start, rect_end], -h_rect, h_rect, color='lightgrey', alpha=0.5, label='∞')
    
    # Barre verticali per distanze chiave
    bars = {
        'Near': (photo.near, 'orange'),
        'Focus': (settings.focus_distance_m, 'green'),
        'Far': (photo.far, 'red'),
        'Hyperfocal': (photo.hyperfocal, 'purple')
    }
        
    for label, (x, color) in bars.items():
        # parcheggio al bordo destro se esce dal grafico
        x_plot = min(x, max_distance) if not math.isinf(x) else max_distance
        ax.axvline(x=x_plot, color=color, linestyle='--', linewidth=2)
        # Label verticale con offset, stessa riga
        ax.annotate(
            label, 
            xy=(x_plot, 0),  # riferimento alla linea
            xytext=(-1, 0),                  # offset orizzontale
            textcoords='offset points',
            ha='right',
            va='center',                     # centrata in y
            rotation=90,
            color=color,
            fontsize=10,
            fontweight='bold'
        )
        # numero sull'asse X, usando coordinate dell’asse per la Y
        ax.annotate(
            format_value(x),
            xy=(x_plot, 0),  # x in dati, y in basso
            xycoords=('data', 'axes fraction'),  # y in coordinate normalizzate 0=bottom
            xytext=(-15, 15),  # offset in punti se vuoi
            textcoords='offset points',
            ha='center',
            va='top',
            rotation=0,
            color=color,
            fontsize=12,
            fontweight='bold'
        )
            
    # Stile grafico
    ax.set_xlabel('Distanza (m)', fontsize=12)
    ax.set_ylabel('Altezza FOV (m)', fontsize=12)
    ax.set_title('Vista di profilo del FOV della fotocamera', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    ax.set_xlim(0, max_distance)
    ax.set_ylim(-fov_height(max_distance*1.1), fov_height(max_distance*1.1))
    ax.legend()
    
    return fig

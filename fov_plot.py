import matplotlib.pyplot as plt
import numpy as np
from tools import *
import math

def plot_camera_profile(photo, settings):
    
    # Calcolo altezza FOV in funzione della distanza
    def fov_height(d):
        return d * np.tan(np.radians(photo.fov_ang_v / 2))
    
    # Gestione caso far infinito
    far_is_infinite = math.isinf(photo.far)
    max_distance = photo.far if not far_is_infinite else photo.hyperfocal * 1.1
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Disegniamo triangolo FOV fino a far (o poco dopo iperfocale se far=infinito)
    d_vals = np.linspace(0, max_distance, 500)
    h_vals = fov_height(d_vals)
    ax.fill_between(d_vals, -h_vals, h_vals, color='skyblue', alpha=0.3, label='FOV')
    
    # Se far infinito, disegniamo un rettangolo oltre iperfocale
    if far_is_infinite:
        rect_start = photo.hyperfocal
        rect_end = photo.hyperfocal * 1.2
        h_rect = fov_height(photo.hyperfocal)
        ax.fill_between([rect_start, rect_end], -h_rect, h_rect, color='lightgrey', alpha=0.5, label='Focus infinito')
    
    # Barre verticali per distanze chiave
    bars = {
        'Near': (photo.near, 'green'),
        'Focus': (settings.focus_distance_m, 'orange'),
        'Far': (photo.far, 'red'),
        'Iperfocale': (photo.hyperfocal, 'purple')
    }
    
    for label, (x, color) in bars.items():
        if math.isinf(x):
            continue  # non disegniamo linea infinita
        ax.axvline(x=x, color=color, linestyle='--', linewidth=2)
        # Label spostata sopra triangolo
        y_pos = fov_height(x) + 0.1 * fov_height(max_distance)
        ax.annotate(f"{label}\n{format_value(x)}", xy=(x, y_pos),
                    xytext=(0, 0), textcoords='offset points',
                    ha='center', va='bottom', color=color, fontsize=10, fontweight='bold')
    
    # Stile grafico
    ax.set_xlabel('Distanza (m)', fontsize=12)
    ax.set_ylabel('Altezza FOV (m)', fontsize=12)
    ax.set_title('Vista di profilo del FOV della fotocamera', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    ax.set_xlim(0, max(photo.far if not far_is_infinite else photo.hyperfocal*1.2, photo.hyperfocal*1.2))
    ax.set_ylim(-fov_height(max_distance*1.1), fov_height(max_distance*1.1))
    ax.legend()
    
    return fig

import matplotlib.pyplot as plt
import numpy as np
from tools import *
import math

def plot_camera_profile(photo, settings):
    
    # Calcolo FOV in funzione della distanza
    def fov_height(d):
        return d * np.tan(np.radians(photo.fov_ang_v / 2))
    
    def fov_width(d):
        return d * np.tan(np.radians(photo.fov_ang_h / 2))
    
    # Gestione caso far infinito
    far_is_infinite = math.isinf(photo.far) or settings.focus_distance_m >= photo.hyperfocal
    max_distance = 1.25*((photo.far if photo.far < photo.hyperfocal else photo.hyperfocal) if not far_is_infinite else photo.hyperfocal)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    fov_color = ('skyblue' if photo.far < max_distance else 'blue' ) if not far_is_infinite else 'purple'
    d_fill = np.linspace(photo.near, photo.far, 500)
    h_fill = fov_height(d_fill)
    ax.fill_between(d_fill, -h_fill, h_fill, color=fov_color, alpha=0.3)

    # --- Bordi sempre visibili ---
    d_borders = np.linspace(0, max_distance, 500)
    h_borders = fov_height(d_borders)
    ax.plot(d_borders, h_borders, color='black', linewidth=1)
    ax.plot(d_borders, -h_borders, color='black', linewidth=1)
    
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
            xytext=(-20, 15),  # offset in punti se vuoi
            textcoords='offset points',
            ha='center',
            va='top',
            rotation=0,
            color=color,
            fontsize=12,
            fontweight='bold'
        )

    # Testo multilinea ma con angolare + lineare sulla stessa riga
    textstr = '\n'.join([
        f'FoV az: {photo.fov_ang_h:.0f}° ({photo.fov_lin_h:.1f} m)',
        f'FoV el: {photo.fov_ang_v:.0f}° ({photo.fov_lin_v:.1f} m)',
        f'Hyperfocal: {format_value(photo.hyperfocal)} m',
        f'Near: {format_value(photo.near)} m',
        f'Far: {format_value(photo.far)} m',
        f'DoF: {format_value(photo.dof)} m'])

    # Aggiungiamo il textbox in alto a sinistra
    ax.text(
        0.02, 0.98, textstr, transform=ax.transAxes,  # coordinate relative alla finestra [0,1]
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
    )
            
    # Stile grafico
    ax.set_xlabel('Distance [m]', fontsize=12)
    ax.set_ylabel('Height [m]', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    ax.set_xlim(0, max_distance)
    ax.set_ylim(-max_distance/4, +max_distance/4)
    ax.set_aspect('equal')  # fondamentale per FOV reale!
    ax.legend()
    
    return fig
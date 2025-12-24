import streamlit as st
from photoCalcs import *
from tools import *
import math

st.markdown(
    """
    <style>
    /* Riduce margine verticale tra tutti i widget principali */
    div.stSlider, 
    div.stNumberInput, 
    div.stSelectSlider, 
    div.stExpander {
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
    }

    /* Riduce il padding interno dei box dei widget */
    div.stSlider > div, 
    div.stNumberInput > div, 
    div.stSelectSlider > div {
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }

    /* Opzionale: riduce l'altezza del testo nei bottoni/freccette */
    button, input {
        line-height: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.title("📷 Lens Mate App")

# valori di default
default_sensor_w_mm = 22.3
default_sensor_h_mm = 14.8
default_coc_mm = 0.019

with st.expander("Camera", expanded=False):
    col1, col2, col3 = st.columns(3)
    sensor_width = col1.number_input("Sensor Width [mm]", value=22.3, format="%.1f", step=0.1)
    sensor_height = col2.number_input("Sensor Height [mm]", value=14.8, format="%.1f", step=0.1)
    coc = col3.number_input("Circle of Confusion [mm]", value=0.019, format="%.3f", step=0.001)


camera = Camera(sensor_width, sensor_height, coc)

with st.expander("Settings", expanded=True):
    col1, col2, col3 = st.columns([1,1,1])
    focal_length = col1.slider("Focal Length [mm]", 16, 400, 50)
    aperture = col2.select_slider(
        "Aperture [f/]", options=[1.4, 2.0, 2.8, 4.0, 5.6, 8.0, 11.0, 16.0, 22.0], value=4.0
    )
    focus_distance = col3.slider("Focus Distance [m]", 0.1, 50.0, 1.0)

settings = Settings(focal_length, aperture, focus_distance)

# calcolo
photo = Photo()
photo.calc_optics(camera, settings)

# visualizzazione risultati
st.subheader("📊 Risultati calcolati")

st.write(f"Hyperfocal Distance: **{format_value(photo.hyperfocal)} m**")
st.write(f"Near Focus: **{format_value(photo.near)} m**")
st.write(f"Far Focus: **{format_value(photo.far)} m**")
st.write(f"Depth of Field: **{format_value(photo.dof)} m**")
st.write(f"Horizontal FOV: **{round(photo.fov_ang_h)}°** ({format_value(photo.fov_lin_h)} m)")
st.write(f"Vertical FOV: **{round(photo.fov_ang_v)}°** ({format_value(photo.fov_lin_v)} m)")
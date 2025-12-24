import streamlit as st
from photoCalcs import Camera, Settings, Photo
import math

st.title("📷 Lens Mate App")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

st.sidebar.header("Camera")

# valori di default
default_sensor_w_mm = 22.3
default_sensor_h_mm = 14.8
default_coc_mm = 0.019

sensor_width = st.sidebar.number_input(
    "Sensor Width [mm]", value=default_sensor_w_mm
)
sensor_height = st.sidebar.number_input(
    "Sensor Height [mm]", value=default_sensor_h_mm
)
coc = st.sidebar.number_input(
    "Circle of Confusion [mm]", value=default_coc_mm
)

camera = Camera(sensor_width, sensor_height, coc)

st.sidebar.header("Settings")

focal_length = st.sidebar.slider("Focal Lenght [mm]", 14, 300, 50)
aperture = st.sidebar.select_slider(
    "Aperture [f/]", options=[1.4, 2.0, 2.8, 4.0, 5.6, 8.0, 11.0, 16.0, 22.0], value=2.8
)
focus_distance = st.sidebar.slider("Focus Distance [m]", 0.3, 50.0, 5.0)

settings = Settings(focal_length, aperture, focus_distance)

# calcolo
photo = Photo()
photo.calc_optics(camera, settings)

# visualizzazione risultati
st.subheader("📊 Risultati calcolati")
st.write(f"Iperfocale: **{photo.hyperfocal:.2f} m**")
st.write(f"Distanza minima di messa a fuoco: **{photo.near:.2f} m**")
st.write(f"Distanza massima di messa a fuoco: **{'∞' if math.isinf(photo.far) else f'{photo.far:.2f} m'}**")
st.write(f"Profondità di campo: **{'∞' if math.isinf(photo.dof) else f'{photo.dof:.2f} m'}**")
from fastapi import FastAPI
from pydantic import BaseModel
from lens_mate import *

app = FastAPI()

class InputData(BaseModel):
    focal_length: float
    aperture: float
    focus_distance: float
    sensor_width: float
    sensor_height: float
    coc: float

@app.post("/calculate")
def calculate(data: InputData):
    camera = Camera(data.sensor_width, data.sensor_height, data.coc)
    settings = Settings(data.focal_length, data.aperture, data.focus_distance)
    photo = Photo()
    photo.calc_optics(camera, settings)

    return {
        "hyperfocal": photo.hyperfocal,
        "near": photo.near_limit,
        "far": photo.far_limit,
        "fov": photo.fov
    }

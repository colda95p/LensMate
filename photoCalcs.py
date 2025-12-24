import math 

# ---------------------------
# Classe Camera
# ---------------------------
class Camera:
    def __init__(self, sensor_width_mm, sensor_height_mm, circle_of_confusion_mm):
        self.sensor_width_mm = sensor_width_mm
        self.sensor_height_mm = sensor_height_mm
        self.circle_of_confusion_mm = circle_of_confusion_mm

# ---------------------------
# Classe PhotoSettings
# ---------------------------
class Settings:
    def __init__(self, focal_length_mm, aperture, focus_distance_m):
        self.focal_length_mm = focal_length_mm
        self.aperture = aperture
        self.focus_distance_m = focus_distance_m

# ---------------------------
# Classe Photo
# ---------------------------
class Photo:
    def __init__(self):
        self.dof = 0
        self.hyperfocal = 0
        self.near = 0
        self.far = 0

    def calc_optics(self, camera: Camera, settings: Settings):
        f = settings.focal_length_mm / 1000
        coc = camera.circle_of_confusion_mm / 1000
        N = settings.aperture
        u = settings.focus_distance_m
        den = (f**4-(N*coc*(u-f))**2)
        self.dof = (2*N*coc*u*(u-f)*f**2) / den; 
        if (self.dof <= 0):
            self.dof = 0
        if (math.isnan(self.dof) or math.isinf(self.dof)):
            self.dof = math.inf

        self.hyperfocal = (f**2) / (N * coc) + f
        self.near = (self.hyperfocal * u) / (self.hyperfocal + (u - f))
        if self.hyperfocal - (u - f) <= 0:
            self.far = math.inf
        else:
            self.far = (self.hyperfocal * u) / (self.hyperfocal - (u - f))

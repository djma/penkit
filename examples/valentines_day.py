import numpy as np
from penkit import shapes
from penkit.textures.util import concat, translate, distance, fit_texture, center, polar_to_cartesian
from penkit.write import write_plot

# unused
def limacon(a, b, resolution=100):
    theta = np.linspace(0., 2*np.pi, resolution)
    r = b + a * np.cos(theta)
    return polar_to_cartesian((r, theta))

# unused
def cardioid(resolution=100):
    return limacon(1, 1)

def limacon_envelope():
    #circle_center = (0,0)
    circle_radius = 1
    P = (1,0)

    num_circles = 50
    circles_centers = [(circle_radius * np.cos(theta), circle_radius * np.sin(theta)) for theta in np.linspace(0, 2*np.pi, num_circles)]
    circles = [concat([shapes.circle(center, distance(center, P)), ([np.nan],[np.nan])]) for center in circles_centers]
    return concat(circles)

def connect_mod_n(n):
    """
    returns a function that takes two integers and draws a line connecting them in a mod circle
    """
    def connect(a, b):
        angles = np.linspace(0, 2*np.pi, n+1)
        a_angle = angles[a % n]
        a_point = (np.cos(a_angle), np.sin(a_angle))
        b_angle = angles[b % n]
        b_point = (np.cos(b_angle), np.sin(b_angle))
        return shapes.line(origin=a_point, end=b_point)
    return connect

connect = connect_mod_n(100)
mult_cardioid = concat([concat([connect(i, 2*i), ([np.nan], [np.nan])]) for i in range(100)])
mult_cardioid = concat([mult_cardioid, shapes.circle((0,0), 1)])

final = concat([
    translate(center(fit_texture(limacon_envelope())), (1.2*0.5, 1.2*0.3)), 
    ([np.nan],[np.nan]), 
    translate(center(fit_texture(mult_cardioid)), (1.2*-0.5, 1.2*-0.3)),
    ])

write_plot([final], 'examples/valentines_day.svg', height=3, width=5, stroke_thickness_pct=0.001)
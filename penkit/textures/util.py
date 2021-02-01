"""The ``textures.util`` module contains utility functions for working with textures.
"""

import numpy as np

LIFT = ([np.nan], [np.nan])

def rotate_texture(texture, rotation, x_offset=0.5, y_offset=0.5):
    """Rotates the given texture by a given angle.

    Args:
        texture (texture): the texture to rotate
        rotation (float): the angle of rotation in degrees
        x_offset (float): the x component of the center of rotation (optional)
        y_offset (float): the y component of the center of rotation (optional)

    Returns:
        texture: A texture.
    """
    x, y = texture
    x = x.copy() - x_offset
    y = y.copy() - y_offset
    angle = np.radians(rotation)
    x_rot = x * np.cos(angle) + y * np.sin(angle)
    y_rot = x * -np.sin(angle) + y * np.cos(angle)
    return x_rot + x_offset, y_rot + y_offset


def fit_texture(layer, preserve_ratio=True):
    """Fits a layer into a texture by scaling each axis to (0, 1).

    Does not preserve aspect ratio (TODO: make this an option).

    Args:
        layer (layer): the layer to scale

    Returns:
        texture: A texture.
    """
    x, y = layer
    x_size = np.nanmax(x) - np.nanmin(x)
    y_size = np.nanmax(y) - np.nanmin(y)
    if preserve_ratio:
        x = (x - np.nanmin(x)) / max(x_size, y_size)
        y = (y - np.nanmin(y)) / max(x_size, y_size)
    else:
        x = (x - np.nanmin(x)) / x_size
        y = (y - np.nanmin(y)) / y_size
    return x, y

def concat(layers):
    """
    Args:
        layers (list(layer)): a list of layers
    """
    return (
        np.concatenate([l[0] for l in layers]),
        np.concatenate([l[1] for l in layers])
    )

def translate(layer, offset):
    x, y = layer
    x = x.copy() - offset[0]
    y = y.copy() - offset[1]
    return x, y

def center(layer):
    x, y = layer
    x = (x - np.nanmean(x))
    y = (y - np.nanmean(y))
    return x, y

def crop(layer, x1, y1, x2, y2):
    x_min = min(x1, x2)
    y_min = min(y1, y2)
    x_max = max(x1, x2)
    y_max = max(y1, y2)

    x, y = layer
    x = x.copy()
    y = y.copy()

    mask = np.logical_or.reduce([x > x_max, x < x_min, y > y_max, y < y_min])
    x[mask] = np.nan
    y[mask] = np.nan
    return x,y

def reverse(layer):
    """
    Reverses the drawing order of a layer
    """
    x, y = layer
    x = x.copy()
    y = y.copy()

    x = np.flip(x)
    y = np.flip(y)
    return x,y

def vflip(layer):
    """
    Flips a layer along the mean y-axis
    """
    x, y = layer
    x = x.copy()
    y = y.copy()

    x = -x + 2*np.nanmean(x)
    return x,y

def polar_to_cartesian(polar_layer):
    """
    Converts ([r], [theta]) to ([x], [y]), assuming a center of 0,0
    """
    r, theta = polar_layer
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
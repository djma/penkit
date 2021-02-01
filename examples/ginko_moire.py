import numpy as np
from penkit import shapes
from penkit.textures.util import concat, rotate_texture, translate, center, crop, reverse, vflip
from penkit.shapes import line, circle
from penkit.write import write_plot

l = (np.array([]), np.array([]))

num_spokes = 200

for i in range(num_spokes):
    l = concat([l, line((0,0), length=1, angle=2*np.pi*(i/4/num_spokes))])
    #l = concat([l, ([np.nan], [np.nan])])
    l = concat([l, line((0.1,0.07), length=1, angle=2*np.pi*(i/4/num_spokes))])
    l = concat([l, ([np.nan], [np.nan])])

write_plot([l], 'examples/ginko_moire.svg', height=8.5, width=8.5, stroke_thickness_pct=0.0015)
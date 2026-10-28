
# open http://localhost:3939/viewer
# Python3 -m ocp_vscode
# Python3 regadera.py

from build123d import *
from ocp_vscode import *
import math

# ==================== PARAMETERS ====================
# Strut core dimensions
strut_width = 7.9      # Fits into the 10mm pocket (leaves 0.5mm wiggle room per side)
strut_length = 211.0   # Total length of the joint beam

# End hole dimensions
hole_diameter = 2.0
hole_depth = 10.0      # 1cm deep

# ==================== MODEL GENERATION ====================
with BuildPart() as lantern_strut:
    # 1. Create the main square solid strut centered on the origin
    Box(
        length=strut_width, 
        width=strut_width, 
        height=strut_length, 
        align=(Align.CENTER, Align.CENTER, Align.CENTER)
    )
    
    # 2. Get the top face and drill the first hole
    top_face = lantern_strut.faces().sort_by(Axis.Z)[-1]
    with Locations(top_face):
        Hole(radius=hole_diameter / 2, depth=hole_depth)
        
    # 3. Get the bottom face and drill the second hole
    bottom_face = lantern_strut.faces().sort_by(Axis.Z)[0]
    with Locations(bottom_face):
        # Hole orientation automatically aligns to the face's normal direction
        Hole(radius=hole_diameter / 2, depth=hole_depth)
        
show(lantern_strut)
export_stl(lantern_strut.part , "lantern_strut.stl")


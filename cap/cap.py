from build123d import *
from ocp_vscode import *

# 1. Define dimensions
outer_diameter = 74.0 * MM
wall_thickness = 2.0 * MM
cap_height = 10.0 * MM
dome_radius = 0.5 * MM  # The radius of the rounded top edge

with BuildPart() as round_cap:
    # 2. Create the main solid cylinder body
    Cylinder(radius=outer_diameter / 2, height=cap_height)
    
    # 3. Fillet the top circular edge to make it round
    # We target the edge furthest along the Z-axis (the top face edge)
    top_edge = round_cap.edges().sort_by(Axis.Z)[-1]
    fillet(top_edge, radius=dome_radius)
    
    # 4. Hollow out the bottom to turn the solid shape into a cap
    # We use offset to remove material from the bottom face
    bottom_face = round_cap.faces().sort_by(Axis.Z)[0]
    offset(amount=-wall_thickness, openings=bottom_face)

# The resulting 3D geometry is stored in round_cap.part
show(round_cap)
export_stl(round_cap.part , "round_cap.stl")


# open http://localhost:3939/viewer
# Python3 -m ocp_vscode
# Python3 regadera.py

from build123d import *
from ocp_vscode import *
import math

# ==================== PARAMETERS ====================
# Base plate dimensions
base_diameter = ((297 * 1.5) - 30 )/ math.pi
base_radius = base_diameter / 2
base_height = 1.5

# Column geometry
cup_height = 10.0
cup_wall_thickness = 1.0

# Lantern paper gap parameters
paper_gap = 0.7
lantern_wall_thickness = 1.0

# Square Pocket Columns parameters
square_side = 10.5            # 1cm side length
hole_diameter = 3.0           # 3mm holes

# --- AUTOMATIC PARAMETRIC CALCULATIONS ---
outer_wall_R2 = base_radius
outer_wall_R1 = outer_wall_R2 - lantern_wall_thickness
inner_wall_R2 = outer_wall_R1 - paper_gap
inner_wall_R1 = inner_wall_R2 - lantern_wall_thickness

# Position for the square pockets so their outer edge meets the inside of the lantern wall exactly.
square_placement_radius = inner_wall_R1 - (square_side / 2)

# Calculate the big centered hole radius to perfectly touch the inner edge of the squares
center_hole_radius = square_placement_radius - (square_side / 2)

# ==================== MODEL GENERATION ====================
with BuildPart() as lantern_top:
    # 1. Create the flat base plate disc
    Cylinder(radius=base_radius, height=base_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2. Get the top face of the base plate (The absolute reference plane)
    top_face = lantern_top.faces().sort_by(Axis.Z)[-1]

    # 3. Step A: Build the 3 Solid Square Columns
    with BuildSketch(top_face) as square_sketch:
        with PolarLocations(radius=square_placement_radius, count=3, start_angle=60):
            Rectangle(width=square_side, height=square_side)
    extrude(square_sketch.sketch, amount=cup_height, mode=Mode.ADD)

    # 4. Step B: Build the Outer Lantern Wall (A solid ring)
    with BuildSketch(top_face) as outer_wall_sk:
        Circle(radius=outer_wall_R2)
        Circle(radius=outer_wall_R1, mode=Mode.SUBTRACT)
    extrude(outer_wall_sk.sketch, amount=cup_height, mode=Mode.ADD)

    # 5. Step C: Build the Inner Lantern Wall (A solid ring)
    with BuildSketch(top_face) as inner_wall_sk:
        Circle(radius=inner_wall_R2)
        Circle(radius=inner_wall_R1, mode=Mode.SUBTRACT)
    extrude(inner_wall_sk.sketch, amount=cup_height, mode=Mode.ADD)

    # 6. Step D: Hollow out the interior pockets for the squares (Upward drill)
    with BuildSketch(top_face) as square_drill:
        with PolarLocations(radius=square_placement_radius, count=3, start_angle=60):
            inner_square = square_side - (2 * cup_wall_thickness)
            Rectangle(width=inner_square, height=inner_square)
    extrude(square_drill.sketch, amount=cup_height, mode=Mode.SUBTRACT)

    # 7. Step E: Drill ALL SIX 3mm thru-holes spaced 60° apart
    # count=6 automatically calculates 360 / 6 = 60 degrees of separation.
    # start_angle=60 keeps the pattern aligned with the center of the square pockets.
    with Locations(top_face):
        with PolarLocations(radius=square_placement_radius, count=6, start_angle=60):
            Hole(radius=hole_diameter / 2, depth=None)

    # 8. Step F: Create the big centered hole passing completely through the base
    with Locations(top_face):
        Hole(radius=center_hole_radius, depth=None)

show(lantern_top)
export_stl(lantern_top.part , "lantern_top.stl")

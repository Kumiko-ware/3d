
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

# Candle dimension (Internal size of the cup)
candle_diameter = 39.0
candle_radius = candle_diameter / 2

# Cup geometry
cup_wall_thickness = 1.0
cup_height = 10.0
cup_separation = 0.5  # Safe gap between cups

# Lantern paper gap parameters
paper_gap = 0.7
lantern_wall_thickness = 1.0

# Square Pocket Columns parameters
square_side = 10.5            # 1cm side length
square_hole_diameter = 3.0    # 3mm thru-hole

# --- AUTOMATIC PARAMETRIC CALCULATIONS ---
outer_cup_radius = candle_radius + cup_wall_thickness
placement_radius = (outer_cup_radius + (cup_separation / 2)) / math.sin(math.radians(60))

outer_wall_R2 = base_radius
outer_wall_R1 = outer_wall_R2 - lantern_wall_thickness
inner_wall_R2 = outer_wall_R1 - paper_gap
inner_wall_R1 = inner_wall_R2 - lantern_wall_thickness

# Calculate maximum possible radius for the square pockets
# so their outer edge meets the inside of the lantern wall exactly.
square_placement_radius = inner_wall_R1 - (square_side / 2)

# ==================== MODEL GENERATION ====================
with BuildPart() as lantern_base:
    # 1. Create the flat base plate disc
    Cylinder(radius=base_radius, height=base_height, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # 2. Get the top face of the base plate (The absolute reference plane)
    top_face = lantern_base.faces().sort_by(Axis.Z)[-1]

    # 3. Step A: Build the 3 Solid Outer Candle Cups
    with BuildSketch(top_face) as cup_sketch:
        with PolarLocations(radius=placement_radius, count=3):
            Circle(radius=outer_cup_radius)
    extrude(cup_sketch.sketch, amount=cup_height, mode=Mode.ADD)

    # 4. Step B: Build the 3 Solid Square Columns
    with BuildSketch(top_face) as square_sketch:
        with PolarLocations(radius=square_placement_radius, count=3, start_angle=60):
            Rectangle(width=square_side, height=square_side)
    extrude(square_sketch.sketch, amount=cup_height, mode=Mode.ADD)

    # 5. Step C: Build the Outer Lantern Wall (A solid ring)
    with BuildSketch(top_face) as outer_wall_sk:
        Circle(radius=outer_wall_R2)
        Circle(radius=outer_wall_R1, mode=Mode.SUBTRACT)
    extrude(outer_wall_sk.sketch, amount=cup_height, mode=Mode.ADD)

    # 6. Step D: Build the Inner Lantern Wall (A solid ring)
    with BuildSketch(top_face) as inner_wall_sk:
        Circle(radius=inner_wall_R2)
        Circle(radius=inner_wall_R1, mode=Mode.SUBTRACT)
    extrude(inner_wall_sk.sketch, amount=cup_height, mode=Mode.ADD)

    # 7. Step E: Drill out the interior pockets for the candles (Upward drill)
    with BuildSketch(top_face) as candle_drill:
        with PolarLocations(radius=placement_radius, count=3):
            Circle(radius=candle_radius)
    extrude(candle_drill.sketch, amount=cup_height, mode=Mode.SUBTRACT)

    # 8. Step F: Drill out the interior pockets for the squares (Upward drill)
    with BuildSketch(top_face) as square_drill:
        with PolarLocations(radius=square_placement_radius, count=3, start_angle=60):
            inner_square = square_side - (2 * cup_wall_thickness)
            Rectangle(width=inner_square, height=inner_square)
    extrude(square_drill.sketch, amount=cup_height, mode=Mode.SUBTRACT)

    with Locations(top_face):
        with PolarLocations(radius=square_placement_radius, count=3, start_angle=60):
            # Hole() automatically punches a cylindrical clearance down along the normal direction.
            # depth=None makes it cut through the entire part cleanly.
            Hole(radius=square_hole_diameter / 2, depth=None)

show(lantern_base)
export_stl(lantern_base.part , "lantern_base.stl")

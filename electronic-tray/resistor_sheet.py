from build123d import *
from ocp_vscode import show, show_all

# ==============================================================================
# 1. PARAMETRIC CONFIGURATION
# ==============================================================================

# Sheet Dimensions (Standard A4 Page)
a4_width = 210.0             # Width along the short edge (X-axis)
a4_length = 297.0            # Length along the long edge (Y-axis)
margin_width = 30.0          # Left flat margin reserved for the binder rings

# Tray & Pocket Heights
base_thickness = 1.0         # Thickness of the bottom sheet
pocket_depth = 8.0          # Depth of each electronic component slot

# --- SEPARATED WALL THICKNESS PARAMETERS ---
# External Borders
outer_wall_thickness_x = 1.0  # Outer boundary wall thickness on Left/Right edges of the grid
outer_wall_thickness_y = 1.0  # Outer boundary wall thickness on Top/Bottom edges of the grid

# Internal Dividers
inner_wall_thickness_x = 1.0  # Vertical divider walls separating columns (X-direction)
inner_wall_thickness_y = 1.0  # Horizontal divider walls separating rows (Y-direction)

# Grid Layout
num_cols = 6
num_rows = 4

# Standard Lever Arch Binder Holes Configuration
enable_holes = True
hole_diameter = 6.0          # Standard 6mm hole punch diameter
hole_margin = 12.0           # Center distance of binder holes from the left edge

# 4-hole system centered along the 297mm length (80mm - 80mm - 80mm standard spacing)
y_center = a4_length / 2.0
hole_y_positions = [
    y_center - 120.0,
    y_center - 40.0,
    y_center + 40.0,
    y_center + 120.0
]

# ==============================================================================
# 2. AUTOMATIC GEOMETRY CALCULATION
# ==============================================================================

# Calculate active grid area width (excluding left binder margin)
pocket_area_width = a4_width - margin_width

# Calculate individual pocket width (X-axis)
total_walls_x = (2 * outer_wall_thickness_x) + ((num_cols - 1) * inner_wall_thickness_x)
pocket_width = (pocket_area_width - total_walls_x) / num_cols

# Calculate individual pocket length (Y-axis)
total_walls_y = (2 * outer_wall_thickness_y) + ((num_rows - 1) * inner_wall_thickness_y)
pocket_length = (a4_length - total_walls_y) / num_rows

print("--- Calculated Dimensions ---")
print(f"Pocket Width (X): {pocket_width:.2f} mm")
print(f"Pocket Length (Y): {pocket_length:.2f} mm")

# ==============================================================================
# 3. 3D MODEL GENERATION
# ==============================================================================

with BuildPart() as tray:
    # Step A: Extrude the flat A4 base plate
    Box(a4_width, a4_length, base_thickness, align=(Align.MIN, Align.MIN, Align.MIN))
    
    # Step B: Add the solid pocket-block on top of the base (offset by margin_width)
    with Locations((margin_width, 0, base_thickness)):
        Box(
            pocket_area_width, 
            a4_length, 
            pocket_depth, 
            align=(Align.MIN, Align.MIN, Align.MIN)
        )
        
    # Step C: Subtract the individual pocket spaces
    x_start = margin_width + outer_wall_thickness_x
    y_start = outer_wall_thickness_y
    
    for row in range(num_rows):
        for col in range(num_cols):
            # Compute bottom-left coordinate of each pocket space
            p_x = x_start + col * (pocket_width + inner_wall_thickness_x)
            p_y = y_start + row * (pocket_length + inner_wall_thickness_y)
            
            with Locations((p_x, p_y, base_thickness)):
                # Added +1.0 to height to guarantee a clean, flush cut through the top face
                Box(
                    pocket_width, 
                    pocket_length, 
                    pocket_depth + 1.0, 
                    align=(Align.MIN, Align.MIN, Align.MIN), 
                    mode=Mode.SUBTRACT
                )
                
    # Step D: Punch standard binder holes into the flat margin
    if enable_holes:
        for h_y in hole_y_positions:
            # We offset Z slightly (-0.5) and increase height to avoid CAD coincident-face artifacts
            with Locations((hole_margin, h_y, -0.5)):
                Cylinder(
                    radius=hole_diameter / 2.0, 
                    height=base_thickness + 1.0, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), 
                    mode=Mode.SUBTRACT
                )

# ==============================================================================
# 4. VIEW MODEL
# ==============================================================================

show(tray)

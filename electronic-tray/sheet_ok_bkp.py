from build123d import *
from ocp_vscode import show, show_all

# ==============================================================================
# 1. PARAMETRIC CONFIGURATION (YOUR EXACT SPECIFICATIONS)
# ==============================================================================

# Sheet Dimensions (Standard A4 Page)
a4_width = 210.0             # Width along short edge (X-axis)
a4_length = 297.0            # Length along long edge (Y-axis)
margin_width = 23.0          # Left flat margin reserved for binder rings

# Tray & Pocket Heights
base_thickness = 1.0         # Thickness of the bottom sheet
pocket_depth = 8.0           # Depth of each electronic component slot
total_height = base_thickness + pocket_depth

# --- SEPARATED WALL PARAMETERS ---
# Y-Axis (Row Separators & Outer Borders)
outer_wall_thickness_top = 4.0     # Top border thickness of the tray
outer_wall_thickness_bottom = 1.0  # Bottom border thickness of the tray
inner_wall_thickness_y = 4.0       # Separators between rows (Horizontal dividers)

# X-Axis (Column Separators & Outer Borders within active grid area)
outer_wall_thickness_left = 1.0    # Left border of grid (after the 23mm margin)
outer_wall_thickness_right = 1.0   # Right border of grid (edge of A4 sheet)
inner_wall_thickness_x = 1.0       # Separators between columns (Vertical dividers)

# Grid Layout
num_cols = 6
num_rows = 4

# --- TOP-LOADING SNAP LID PARAMETERS ---
lid_proud_height = 1.0       # How far the top surface of the lid stands proud above the tray
lid_top_thickness = 1.2      # Main top cap thickness of the lid
print_clearance = 0.25       # Clearance tolerance around the lid for 3D printing

# Single-Sided Overhang (Top edge only)
y_overhang_extension = 2.0   # Overhang length extending over the top divider wall
overhang_clearance = 0.6     # Vertical gap between the overhang and the divider wall top face

# Flap Depths (Vertical extension downward into pocket)
side_flap_depth = 4.0 + lid_proud_height    # Left/Right flaps (now latching)
top_bottom_flap_depth = 2.0 + lid_proud_height # Front/Back flaps (now alignment-only)
flap_thickness = 1.0         # Thickness of all flaps

# --- CUSTOM FLAP WIDTH PARAMETERS ---
side_flap_span_y = 15.0      # Span/width of the Left/Right flaps along the Y-axis
top_bottom_flap_span_x = 15.0 # Span/width of the Front/Back flaps along the X-axis

# --- TUNABLE LATCHING & RECENTERING GEOMETRY ---
# Tunable parameters for the Wall Recess (Locking Pockets in the Left/Right walls)
recess_depth_x = 0.5         # How deep the lock pocket cuts into the side wall
recess_span_y = 8.0          # Width of the locking pocket along the Y-axis
recess_height_z = 1.2        # Vertical height of the locking pocket
recess_offset_z = 1.8        # Distance from top of tray down to the pocket top

# Tunable parameters for the Flap Snap Bumps (on the Left/Right flaps)
bump_projection_x = 0.45     # How far the bump protrudes outwards
bump_span_y = 6.0            # Width of the snap bump along the Y-axis
bump_height_z = 1.0          # Vertical height of the snap bump

# --- ENGRAVED TEXT PARAMETERS ---
text_font_size = 20.0        # Your requested size 20 font
text_engrave_depth = 0.5     # Depth of the engraving (0.5mm)

# Binder Holes
enable_holes = True
hole_diameter = 6.0
hole_margin = 12.0
y_center = a4_length / 2.0
hole_y_positions = [y_center - 120.0, y_center - 40.0, y_center + 40.0, y_center + 120.0]

# ==============================================================================
# 2. AUTOMATIC GEOMETRY CALCULATION & SAFEGUARDS
# ==============================================================================

# Calculate active grid area width (excluding left binder margin)
pocket_area_width = a4_width - margin_width

# Calculate individual pocket width (X-axis)
total_separators_x = (num_cols - 1) * inner_wall_thickness_x
pocket_width = (pocket_area_width - outer_wall_thickness_left - outer_wall_thickness_right - total_separators_x) / num_cols

# Calculate individual pocket length (Y-axis)
total_separators_y = (num_rows - 1) * inner_wall_thickness_y
pocket_length = (a4_length - outer_wall_thickness_top - outer_wall_thickness_bottom - total_separators_y) / num_rows

# SAFEGUARD: Prevent latch cuts from breaking through dividers/outer walls
max_safe_depth_x = min(
    inner_wall_thickness_x * 0.5, 
    outer_wall_thickness_left * 0.5,
    outer_wall_thickness_right * 0.5
)
if recess_depth_x > max_safe_depth_x:
    recess_depth_x = max_safe_depth_x

if bump_projection_x > recess_depth_x:
    bump_projection_x = recess_depth_x

# ==============================================================================
# 3. 3D MODEL GENERATION: TRAY
# ==============================================================================

with BuildPart() as tray:
    # Step A: Extrude the flat A4 base plate
    Box(a4_width, a4_length, base_thickness, align=(Align.MIN, Align.MIN, Align.MIN))
    
    # Step B: Add the solid pocket-block on top of the base
    with Locations((margin_width, 0, base_thickness)):
        Box(pocket_area_width, a4_length, pocket_depth, align=(Align.MIN, Align.MIN, Align.MIN))
        
    # Step C: Subtract pockets and create side snap recesses
    x_start = margin_width + outer_wall_thickness_left
    y_start = outer_wall_thickness_bottom
    recess_z = total_height - recess_offset_z - recess_height_z
    
    for row in range(num_rows):
        for col in range(num_cols):
            p_x = x_start + col * (pocket_width + inner_wall_thickness_x)
            p_y = y_start + row * (pocket_length + inner_wall_thickness_y)
            
            # 1. Main pocket cavity subtraction
            with Locations((p_x, p_y, base_thickness)):
                Box(
                    pocket_width, 
                    pocket_length, 
                    pocket_depth + 1.0, 
                    align=(Align.MIN, Align.MIN, Align.MIN), 
                    mode=Mode.SUBTRACT
                )
            
            # 2. Subtract latching recesses in LEFT & RIGHT inner pocket walls only (centered in Y)
            with Locations((p_x, p_y + pocket_length/2.0, recess_z)):
                Box(recess_depth_x * 2.0, recess_span_y, recess_height_z, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
                    
            with Locations((p_x + pocket_width, p_y + pocket_length/2.0, recess_z)):
                Box(recess_depth_x * 2.0, recess_span_y, recess_height_z, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

    # Step D: Punch binder holes
    if enable_holes:
        for h_y in hole_y_positions:
            with Locations((hole_margin, h_y, -0.5)):
                Cylinder(
                    radius=hole_diameter / 2.0, 
                    height=base_thickness + 1.0, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), 
                    mode=Mode.SUBTRACT
                )

# ==============================================================================
# 4. 3D MODEL GENERATION: 24 INDIVIDUAL SNAP LIDS (E24 SERIES DECADE)
# ==============================================================================

# Standard E24 decade base values
e24_values = [
    "10", "11", "12", "13", "15", "16",
    "18", "20", "22", "24", "27", "30",
    "33", "36", "39", "43", "47", "51",
    "56", "62", "68", "75", "82", "91"
]

# Inner cap dimensions based on pocket size (with print clearance)
lid_inner_w = pocket_width - (2.0 * print_clearance)
lid_inner_l = pocket_length - (2.0 * print_clearance)

# Total cap bounds
lid_cap_w = lid_inner_w
lid_cap_l = pocket_length + y_overhang_extension - (2.0 * print_clearance)

# Shift to center the extended cap over the pocket flaps
y_alignment_shift = y_overhang_extension / 2.0

# Flap widths
flap_w_x = lid_inner_w * 0.5 - (2.0 * print_clearance) 
flap_w_y = lid_inner_l * 0.5 - (2.0 * print_clearance) 

# Spacing to arrange the 24 lids in a 4 x 6 grid next to the tray
grid_start_x = a4_width + 5.0 + lid_cap_w/2 # Spaced 5mm to the right of the tray
grid_start_y = 0.0 + lid_cap_l/2
grid_pitch_x = lid_cap_w + 5.0  # 5mm gap between columns
grid_pitch_y = lid_cap_l + 3.0 #inner_wall_thickness_y - y_overhang_extension

# Store generated lid parts for VS Code visualization
all_lids = []

for index, label in enumerate(e24_values):
    # Determine grid coordinates for placing each lid in the viewer
    g_col = index % num_cols
    g_row = index // num_cols
    
    # Calculate offset in 3D space
    disp_x = grid_start_x + g_col * grid_pitch_x
    disp_y = grid_start_y + g_row * grid_pitch_y
    
    with BuildPart() as single_lid:
        # 1. Create top flat lid cap
        with Locations((0, y_alignment_shift, 0)):
            Box(lid_cap_w, lid_cap_l, lid_top_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
            
            # Subtract the fingernail clearance slot from the underside of the top overhang
            overhang_cut_y = (lid_cap_l / 2.0) - (y_overhang_extension / 2.0)
            with Locations((0, overhang_cut_y, 0)):
                Box(
                    lid_cap_w + 1.0, 
                    y_overhang_extension + 0.1, 
                    overhang_clearance, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), 
                    mode=Mode.SUBTRACT
                )

            # 2. Engrave Custom E24 Text centered on the top lid cap face
            # Use 'extrude' (lowercase) with '.sketch' attribute to prevent any runtime crashes
            with BuildSketch(Plane.XY.moved(Location((0, 0, lid_top_thickness)))) as text_sketch:
                Text(label, font_size=text_font_size, align=(Align.CENTER, Align.CENTER))
            extrude(text_sketch.sketch, amount=-text_engrave_depth, mode=Mode.SUBTRACT)
        
        # 3. Add Left & Right snapping flaps with latch bumps (X-direction)
        flap_offset_x = (lid_cap_w / 2.0) - (flap_thickness / 2.0)
        bump_z_pos = side_flap_depth - (recess_offset_z + lid_proud_height) - bump_height_z
        
        # Left Snapping Flap
        with Locations((-flap_offset_x, 0, -side_flap_depth)):
            Box(flap_thickness, side_flap_span_y, side_flap_depth, 
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Snap bump
            with Locations((-flap_thickness/2.0, 0, bump_z_pos)):
                Box(bump_projection_x, bump_span_y, bump_height_z, 
                    align=(Align.MAX, Align.CENTER, Align.MIN))
                
        # Right Snapping Flap
        with Locations((flap_offset_x, 0, -side_flap_depth)):
            Box(flap_thickness, side_flap_span_y, side_flap_depth, 
                align=(Align.CENTER, Align.CENTER, Align.MIN))
            # Snap bump
            with Locations((flap_thickness/2.0, 0, bump_z_pos)):
                Box(bump_projection_x, bump_span_y, bump_height_z, 
                    align=(Align.MIN, Align.CENTER, Align.MIN))
                
        # 4. Add Front & Back short side flaps strictly for alignment (no bumps, Y-direction)
        flap_offset_y = (lid_inner_l / 2.0) - (flap_thickness / 2.0)
        
        # Front Alignment Flap
        with Locations((0, -flap_offset_y, -top_bottom_flap_depth)):
            Box(top_bottom_flap_span_x, flap_thickness, top_bottom_flap_depth, 
                align=(Align.CENTER, Align.CENTER, Align.MIN))
                
        # Back Alignment Flap
        with Locations((0, flap_offset_y, -top_bottom_flap_depth)):
            Box(top_bottom_flap_span_x, flap_thickness, top_bottom_flap_depth, 
                align=(Align.CENTER, Align.CENTER, Align.MIN))
                
    # Position the completed lid on the display grid and save
    positioned_lid = single_lid.part.moved(Location((disp_x, disp_y, 0)))
    all_lids.append(positioned_lid)

# ==============================================================================
# 5. VIEWING
# ==============================================================================

# Unpack the list of 24 lids and the tray to display them all together
show(tray, *all_lids)

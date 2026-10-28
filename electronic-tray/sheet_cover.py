from build123d import *
from ocp_vscode import show, show_all

# ==============================================================================
# 1. PARAMETRIC CONFIGURATION
# ==============================================================================

# Sheet Dimensions (Standard A4 Page)
a4_width = 210.0             # Width along short edge (X-axis)
a4_length = 297.0            # Length along long edge (Y-axis)
margin_width = 23.0          # Left flat margin reserved for binder rings

# Tray & Pocket Heights
base_thickness = 1.0         # Thickness of the bottom sheet
pocket_depth = 8.0           # Depth of each electronic component slot
total_height = base_thickness + pocket_depth

# --- FULLY SEPARATED WALL PARAMETERS ---
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
overhang_clearance = 0.5     # Vertical gap between the overhang and the divider wall top face

# Vertical Latching Flaps (Y-Direction: Front & Back)
latch_flap_depth = 2.0 + lid_proud_height  
latch_flap_thickness = 1.0   

# Side Alignment Flaps (X-Direction: Left & Right)
alignment_flap_depth = 1.0 + lid_proud_height 
alignment_flap_thickness = 1.0 

# Latching Joint Details (Front/Back walls only)
latch_pocket_depth = 0.5     # Depth of latching recess inside tray wall / bump on flap
latch_pocket_height = 1.0    # Vertical height of the snapping bump/recess
latch_pocket_offset = 1.0    # Distance from top of tray down to the recess

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

# SAFEGUARD: Prevent latch cuts from breaking through divider walls
max_safe_depth_y = inner_wall_thickness_y * 0.25
if latch_pocket_depth > max_safe_depth_y:
    latch_pocket_depth = max_safe_depth_y

print("--- Calculated Dimensions ---")
print(f"Pocket Storage Size: {pocket_width:.2f} mm (Width) x {pocket_length:.2f} mm (Length)")

# ==============================================================================
# 3. 3D MODEL GENERATION: TRAY
# ==============================================================================

with BuildPart() as tray:
    # Step A: Extrude the flat A4 base plate
    Box(a4_width, a4_length, base_thickness, align=(Align.MIN, Align.MIN, Align.MIN))
    
    # Step B: Add the solid pocket-block on top of the base
    with Locations((margin_width, 0, base_thickness)):
        Box(pocket_area_width, a4_length, pocket_depth, align=(Align.MIN, Align.MIN, Align.MIN))
        
    # Step C: Subtract pockets and create snap recesses
    x_start = margin_width + outer_wall_thickness_left
    y_start = outer_wall_thickness_bottom
    
    # Recess depth from top of the tray
    recess_z = total_height - latch_pocket_offset - latch_pocket_height
    
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
            
            # 2. Subtract latching recesses in Front & Back inner pocket walls only
            recess_length_x = pocket_width * 0.25  
            
            # Front Wall Recess
            with Locations((p_x + pocket_width/2.0, p_y, recess_z)):
                Box(recess_length_x, latch_pocket_depth * 2.0, latch_pocket_height, 
                    align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
                    
            # Back Wall Recess
            with Locations((p_x + pocket_width/2.0, p_y + pocket_length, recess_z)):
                Box(recess_length_x, latch_pocket_depth * 2.0, latch_pocket_height, 
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
# 4. 3D MODEL GENERATION: INDIVIDUAL SNAP LID
# ==============================================================================

# Inner cap dimensions based on pocket size (with print clearance)
lid_inner_w = pocket_width - (2.0 * print_clearance)
lid_inner_l = pocket_length - (2.0 * print_clearance)

# X-axis total width (Standard cap width with clearance)
lid_cap_w = lid_inner_w

# Y-axis total length with single-sided top extension
# Length = pocket_length + overhang_extension - clearance
lid_cap_l = pocket_length + y_overhang_extension - (2.0 * print_clearance)

# Centered offset to align the main body of the lid with the pocket underneath
# Because the extension is only on one side, we shift the 3D block to keep flaps in line
y_alignment_shift = y_overhang_extension / 2.0

# Flap widths (leaving clearance at corners so flaps do not bind)
flap_w_x = lid_inner_w * 0.2 - (2.0 * print_clearance)
flap_w_y = lid_inner_l * 0.2 - (2.0 * print_clearance)

with BuildPart() as lid:
    # 1. Create top flat lid cap (Shifted to allow the single-sided extension)
    with Locations((0, y_alignment_shift, 0)):
        Box(lid_cap_w, lid_cap_l, lid_top_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
        
        # Subtract the fingernail clearance slot from the underside of the top overhang
        # This keeps the main lid proud at 1.0mm, but creates a gap below the 2mm overhang
        overhang_cut_y = (lid_cap_l / 2.0) - (y_overhang_extension / 2.0)
        with Locations((0, overhang_cut_y, 0)):
            Box(
                lid_cap_w + 1.0, 
                y_overhang_extension + 0.1, 
                overhang_clearance, 
                align=(Align.CENTER, Align.CENTER, Align.MIN), 
                mode=Mode.SUBTRACT
            )
    
    # 2. Add Left & Right short side flaps strictly for alignment (no bumps, X-direction)
    # Note: These are centered relative to the pocket (not the shifted cap)
    flap_offset_x = (lid_cap_w / 2.0) - (alignment_flap_thickness / 2.0)
    
    # Left Alignment Flap
    with Locations((-flap_offset_x, 0, -alignment_flap_depth)):
        Box(alignment_flap_thickness, flap_w_y, alignment_flap_depth, 
            align=(Align.CENTER, Align.CENTER, Align.MIN))
            
    # Right Alignment Flap
    with Locations((flap_offset_x, 0, -alignment_flap_depth)):
        Box(alignment_flap_thickness, flap_w_y, alignment_flap_depth, 
            align=(Align.CENTER, Align.CENTER, Align.MIN))
            
    # 3. Add Front & Back snapping flaps with latch bumps (Y-direction)
    flap_offset_y = (lid_inner_l / 2.0) - (latch_flap_thickness / 2.0)
    bump_z_pos = latch_flap_depth - (latch_pocket_offset + lid_proud_height) - latch_pocket_height
    
    # Front Snapping Flap
    with Locations((0, -flap_offset_y, -latch_flap_depth)):
        Box(flap_w_x, latch_flap_thickness, latch_flap_depth, 
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Snap bump
        with Locations((0, -latch_flap_thickness/2.0, bump_z_pos)):
            Box(flap_w_x, latch_pocket_depth, latch_pocket_height, 
                align=(Align.CENTER, Align.MAX, Align.MIN))
            
    # Back Snapping Flap
    with Locations((0, flap_offset_y, -latch_flap_depth)):
        Box(flap_w_x, latch_flap_thickness, latch_flap_depth, 
            align=(Align.CENTER, Align.CENTER, Align.MIN))
        # Snap bump
        with Locations((0, latch_flap_thickness/2.0, bump_z_pos)):
            Box(flap_w_x, latch_pocket_depth, latch_pocket_height, 
                align=(Align.CENTER, Align.MIN, Align.MIN))

# Position the lid next to the tray in space for clear rendering in VS Code Viewer
lid_display = lid.part.moved(Location((margin_width + 10, -50, 0)))

# ==============================================================================
# 5. VIEWING
# ==============================================================================

show(tray, lid_display)

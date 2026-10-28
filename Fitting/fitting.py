from build123d import *

1. Maximize Wall Thickness
Do not rely on infill to hold water. You must create a solid, thick outer shell.
Perimeters: Set to at least 4 to 6.

Go to Print Settings > Layers and perimeters > Perimeters.Top/Bottom Solid Layers: Set to 5 to 7.
Go to Print Settings > Layers and perimeters > Horizontal shells.

2. Force Over-Extrusion (The Secret Weapon)Over-extruding plastic crushes the filament into the previous layer, closing microscopic pinholes.Extrusion Multiplier: Increase this value to 1.03 or 1.05 (a 3% to 5% increase).

Go to Filament Settings > Filament > Extrusion multiplier.

3. Increase Extrusion WidthWider lines melt together better and have fewer total seams. You can safely print wider lines than your nozzle size. For a 0.4mm nozzle: Change all widths (Default, First layer, Perimeters, Infill) to 0.5mm or 0.6mm.

Go to Print Settings > Advanced > Extrusion width.

4. Optimize Temperature and SpeedHotter plastic flows together better, while slower speeds ensure consistent flow.Nozzle Temperature: Print at the higher end of your filament’s recommended range (e.g., 245°C–250°C for PETG) to maximize layer bonding.

Go to Filament Settings > Filament > Temperature.Speed: Reduce your outer perimeter speed to 30–40 mm/s. Go to Print Settings > Speed.

5. Adjust Seams and InfillWater will always find a path through the start/stop points of your layers.Seam Position: Set to Aligned or Rear. Avoid "Random," which scatters potential leak holes all over the part.

Go to Print Settings > Layers and perimeters > Seam position.Infill Type: Use Gyroid at 20% or higher. If water does breach the outer wall, Gyroid infill isolates water into tiny individual pockets, preventing a total blowout. Go to Print Settings > Infill.

thread_pitch = 1.814
thread_id = 24.118
thread_od = 26.441
thread_height_sharp = 1.743
thread_height_round = 1.162
thread_length = 8
fitting_diameter = 35
fitting_height = 15

tube_od = 4.6
tube_id = 3.6
tube_length = 10
ridge_diameter = 6.4
ridge_length = 4.6

fitting_body = Cylinder(radius = fitting_diameter/2,
                        height = fitting_height)

bottom = fitting_body.faces().sort_by(Axis.Z)[-1]

fitting_body = offset(fitting_body,
                      amount = - (35 - thread_od+0.01)/2,
                      openings = bottom)

thread_path = Helix(pitch = thread_pitch,
                    height = thread_length,
                    radius = thread_od/2)

guide_path = Helix(pitch=thread_pitch,
                   height=thread_length,
                   radius=(thread_od / 2) + 1.0)

sketch_plane = thread_path ^ 0

thread_profile = Trapezoid(width = thread_pitch - 0.2,
                           height = thread_height_round - 0.2,
                           left_side_angle = 90 - 27.5,
                           align = (Align.CENTER, Align.MIN),
                           rotation = -90)

fitting_thread = sweep(sections =  sketch_plane * thread_profile,
                       path = thread_path,
                       binormal = guide_path)
fitting_thread.position -= (0, 0 , 1)

tube = Cylinder(radius = tube_od /2,
                height = tube_length)

ridge = Cone(bottom_radius = tube_od/2,
             top_radius = ridge_diameter/2,
             height = ridge_length)

ridge.position -= (0, 0, ridge_length)

tube = tube + ridge

hole = Cylinder(radius = tube_id/2, height = 100)

tube.position -= (0, 0, tube_length)

tubes = Pos(fitting_diameter/6, 0, 0) * tube + Pos(-fitting_diameter/6, 0, 0) * tube

holes = Pos(fitting_diameter/6, 0, 0) * hole + Pos(-fitting_diameter/6, 0, 0) * hole

holes += PolarLocations(radius = fitting_diameter/2,
                         count = 12) * Cylinder(radius = 2, height = 100)

export_stl(fitting_body + fitting_thread + tubes - holes, "fitting.stl")


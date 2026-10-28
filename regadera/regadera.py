
# open http://localhost:3939/viewer
# python3 -m ocp_vscode
# python3 regadera.py

from build123d import *
from ocp_vscode import *


tube_length = 30
tube_diameter = 12
tube_angle = 30
flower_diameter = 40
cone_length = 18
hole_diameter = .8
hole_radius = 3
wall_thickness = 1

lower_cone = Circle(radius = tube_diameter/2)
upper_cone = Pos([0,0,cone_length]) * Circle(radius = flower_diameter/2)
cone_faces = Sketch() + [upper_cone, lower_cone,]
cone = loft(cone_faces)
cone.orientation = (tube_angle,0,0)


tube = Cylinder(radius = tube_diameter/2, height = tube_length)
tube.position += (0, -0.5, -tube_length/3)

part = tube + cone

part = offset(objects = part, amount = wall_thickness,
              openings = part.faces().sort_by(Axis.Z)[0])

flower_plane = Plane(part.faces().sort_by(Axis.Z)[-1])

holes_locations = [loc for loc in HexLocations(radius = hole_radius,
                                               x_count = 20,
                                               y_count = 20)
                   if loc.position.length < flower_diameter/2 - hole_radius]

holes = flower_plane * holes_locations * Hole(radius = hole_diameter, depth = wall_thickness)

part -= holes

show(part)
export_stl(part , "regadera.stl")


from cadquery import *
from cadquery.func import *
from cadquery.vis import *

depth = 34
height = 100
width = 60
hole_dist = 83.34
hole_mount = 4
hole_cable = 12
stud_diam = 5


result = (Workplane("XY")
          .box(height, width, depth)
          .faces("+Z")
          .shell(1)
          .faces("<Z[1]")
          .workplane()
          .tag("base")
          .center(hole_dist/2, 0)
          .circle(stud_diam/2)
          .extrude(depth)
          .faces(">>Z")
          .hole(2, 20)
          .center(0, 20)
          .hole(hole_mount)
          .workplaneFromTagged("base")
          .center(-hole_dist/2, 0)
          .circle(stud_diam/2)
          .extrude(depth)
          .faces(">>Z")
          .hole(2, 20)
          .center(0, -20)
          .hole(hole_mount)
          .faces("<Y").workplane()
          .center(5,depth/2)
          .hole(hole_cable,3)
          )

result.export("box.stl")
show(result)

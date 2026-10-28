use <MCAD/boxes.scad>

$//fa=.5; $fs=.2;

// Rubber feet: 109 x 69.5
// Total base: 145 x 90, width 34
// Feet = 6.5 dia (r= 3.7)

// Height until led: 85
// Lateral space, for hook: 62

thickness = 3;

// Base
difference(){
    translate([0, 0, thickness/2])
    roundedBox(size=[145, 90 + 2*thickness, thickness],radius=1,sidesonly=false);
    translate([54.5, 34.75, thickness + 2.7 ]) sphere(3.7);
    translate([54.5, -34.75, thickness + 2.7 ]) sphere(3.7);
    translate([-54.5, 34.75, thickness + 2.7 ]) sphere(3.7);
    translate([-54.5, -34.75, thickness + 2.7]) sphere(3.7);
    translate([0, 0, thickness/2])
    roundedBox(size=[100, 60.5, 20],radius=5,sidesonly=false);
}

// Wall side
height = 85;

difference(){
translate([0, 90/2 + thickness/2, height/2 + thickness/2])
    rotate([90, 0, 0])
    roundedBox(size=[145, height + thickness, thickness],radius=1,sidesonly=false);
    // Tape space
    translate([(145-40)/2, 90/2 + thickness/2 + (thickness-0.5), height/2 + thickness/2])
    rotate([90, 0, 0])
    roundedBox(size=[20, height-20 + thickness, thickness],radius=.1,sidesonly=false);
    
    translate([-(145-40)/2, 90/2 + thickness/2 + (thickness-0.5), height/2 + thickness/2])
    rotate([90, 0, 0])
    roundedBox(size=[20, height-20 + thickness, thickness],radius=.1,sidesonly=false);
}

// angled thickness
angth = thickness * sin(39);
angdp = thickness * cos(39);

// Router side
// Vertical
translate([0, -(90/2 + thickness/2), (10+angth)/2 + thickness/2])
    rotate([90, 0, 0])
    roundedBox(size=[145, 10 + angth + thickness, thickness],radius=1,sidesonly=false);
// Diagonal
translate([0, -(90/2 + thickness/2) + cos(39) * 30/2 - 0.6, sin(39) * 30/2 + 10 + thickness/2 + angth])
    rotate([39, 0, 0])
    roundedBox(size=[145, 30, thickness],radius=1,sidesonly=false);

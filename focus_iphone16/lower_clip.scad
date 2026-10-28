use <MCAD/boxes.scad>

$fa=.5;
$fs=.2;

$fa=5;
$fs=2;

module hinge(width, height, thickness, bore){
    difference(){
        union(){
            translate([0, 0, height/2])
                cube([thickness, width, height], true);
            translate([0, 0, height])
                rotate([0, 90, 0])
                    cylinder(h = thickness, r = width/2, center = true);
        }
        translate([0, 0, height])
                rotate([0, 90, 0])
                    cylinder(h = thickness + 2, r = bore/2, center = true);
}
}

module spring_holder(dia, height){
    cylinder(h = height, r = dia/2 + 1, center = false);
    translate([0, 0, height])
    difference(){
        cylinder(h = height, r = dia/2 + 1, center = false);
        translate([0, 0, 1]);
        cylinder(h = height + 2, r = dia/2, center = false);
    }
}

// Jaw
translate([0,0,5]){
    intersection() {
        roundedBox(size=[154, 40, 10],radius=1,sidesonly=false);
        translate([0,0,-936])
            sphere(r=939);
    }
}
translate([0,20,2.5]){
    roundedBox(size=[154, 80,5],radius=1,sidesonly=false);
}

// Hinges
translate([72, 24.9, 0])
    hinge(10, 17, 5, 3);

translate([61.5, 24.9, 0])
    hinge(10, 17, 5, 3);

translate([-72, 24.9, 0])
    hinge(10, 17, 5, 3);

translate([-61.5, 24.9, 0])
    hinge(10, 17, 5, 3);

// Phone holder
translate([0, 64, 26])
rotate([-90, 180, 0])
difference(){
    // Outside
    roundedBox(size=[154,52,13],radius=1,sidesonly=false);
    // Inside (phone space)
    translate([0, 5, 0])
        roundedBox(size=[152,52,11],radius=1,sidesonly=false);
    // Front opening (Screen)
    translate([0, 6, 5])
        roundedBox(size=[142,45,11],radius=1,sidesonly=false);
    // Side opening (USB port)
    translate([5, 37, 0])
        roundedBox(size=[152,55,9],radius=1,sidesonly=false);
}

// Springs
translate([45, 38.8, 4])
        spring_holder(28.4, 4);

translate([-45, 38.8, 4])
        spring_holder(28.4, 4);
use <MCAD/boxes.scad>

$fa=.5;
$fs=.2;

$fa=1; $fs=.5;

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
    difference() {
        roundedBox(size=[154,40,10],radius=1,sidesonly=false);
        translate([0,0,939])
            sphere(r=939);
    }
}
translate([0, 17, 2.5]){
    roundedBox(size=[154,74,5],radius=1,sidesonly=false);
}

// New curvature
difference(){
    translate([0.25, -0.9, 0]) //0.3, -0.8
        rotate([-7.2, -2.3, 0])
            translate([0, 0, 5]){
                difference() {
                    roundedBox(size=[154,39.5,10],radius=1,sidesonly=false);
                    translate([0,0,939])
                        sphere(r=939);
            }
        }
    translate([0, 0, -5])
        cube([160, 100, 10], center = true);
    translate([0, -30, 10])
        cube([160, 20, 20], center = true);
    translate([10 + 154/2, 0, 10])
        cube([20, 40, 20], center = true);
    translate([-10 - 154/2, 0, 10])
        cube([20, 40, 20], center = true);        
}

// Hinges
translate([66.75, 24.9, 1])
        hinge(10, 17, 5, 3);

translate([-66.75, 24.9, 1])
        hinge(10, 17, 5, 3);

// Springs
translate([45, 38.8, 4])
        spring_holder(28.4, 4);

translate([-45, 38.8, 4])
        spring_holder(28.4, 4);
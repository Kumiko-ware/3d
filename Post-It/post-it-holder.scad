use <MCAD/boxes.scad>

// $fa=.5; $fs=.2;

// PAPER
//base
roundedBox(size=[96,96,3],radius=1,sidesonly=false);
//back
translate([0,46.5,46.5])
rotate([90, 0, 0])
roundedBox(size=[96,96,3],radius=1,sidesonly=false);
//right
translate([46.5, 0, 46.5])
rotate([0, 90, 0])
roundedBox(size=[96,96,3],radius=1,sidesonly=false);
//left
translate([-46.5, 0, 46.5])
rotate([0, 90, 0])
roundedBox(size=[96,96,3],radius=1,sidesonly=false);
//front-left
translate([-32, -46.5,46.5])
rotate([90, 0, 0])
roundedBox(size=[32,96,3],radius=1,sidesonly=false);
//front-right
translate([32, -46.5,46.5])
rotate([90, 0, 0])
roundedBox(size=[32,96,3],radius=1,sidesonly=false);

// PENCILS
//base
translate([55, 0, 0])
roundedBox(size=[20,96,3],radius=1,sidesonly=false);

//right
translate([63.5, 0, 46.5])
rotate([0, 90, 0])
roundedBox(size=[96,96,3],radius=1,sidesonly=false);
//front
translate([55, -46.5, 46.5])
rotate([90, 0, 0])
roundedBox(size=[20,96,3],radius=1,sidesonly=false);
//back
translate([55, 46.5, 46.5])
rotate([90, 0, 0])
roundedBox(size=[20,96,3],radius=1,sidesonly=false);

module pencil_bore(){
    difference(){
        cylinder(94, 5.5, 5.5);
    }
}

module pencil_tube(){
    difference(){
        cylinder(93, 6.5, 6.5);
    }
}

//top
difference(){
    union(){
        //top
        translate([55, 0, 93])
        roundedBox(size=[20,96,3],radius=1,sidesonly=false);
        
        translate([55,37,1.5])
        pencil_tube();
        translate([55,18.5,1.5])
        pencil_tube();
        translate([55,0,1.5])
        pencil_tube();
        translate([55,-18.5,1.5])
        pencil_tube();
        translate([55,-37,1.5])
        pencil_tube();
    }
    translate([55,37,1.5])
    pencil_bore();
    translate([55,18.5,1.5])
    pencil_bore();
    translate([55,0,1.5])
    pencil_bore();
    translate([55,-18.5,1.5])
    pencil_bore();
    translate([55,-37,1.5])
    pencil_bore();
}
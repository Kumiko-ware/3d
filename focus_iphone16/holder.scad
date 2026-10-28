use <MCAD/boxes.scad>


$fa=.5;
$fs=.2;

rotate([-90, 180, 0])
difference(){
    roundedBox(size=[154,55,13],radius=1,sidesonly=false);
    translate([0, 6, 0])
        roundedBox(size=[152,55,11],radius=1,sidesonly=false);
    translate([0, 6, 5])
        roundedBox(size=[142,45,11],radius=1,sidesonly=false);
    translate([5, 6, 0])
        roundedBox(size=[152,55,9],radius=1,sidesonly=false);
}

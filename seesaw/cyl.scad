use <MCAD/boxes.scad>

$fa=.5;
$fs=.2;

//$fa=1; $fs=5;

difference(){
   cylinder(37, 9.7, 9.7);
    translate([0,0,-1])
   cylinder(39, 7.7, 7.7);
    }
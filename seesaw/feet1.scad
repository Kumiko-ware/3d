use <MCAD/boxes.scad>

$fa=.5;
$fs=.2;

//$fa=1; $fs=5;

difference(){
    roundedBox(size=[99,41,4],radius=1,sidesonly=false);
    translate([0, 0, 2])
        roundedBox(size=[97,39,4],radius=.1,sidesonly=false);
    }
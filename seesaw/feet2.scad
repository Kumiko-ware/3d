use <MCAD/boxes.scad>

$fa=.5;
$fs=.2;

//$fa=1; $fs=5;

difference(){
    roundedBox(size=[71,71,10],radius=1,sidesonly=false);
    translate([0, 0, 8])
        roundedBox(size=[69,69,10],radius=.1,sidesonly=false);
    }
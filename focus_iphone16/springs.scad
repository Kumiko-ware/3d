module spring_holder(dia, height){
    cylinder(h = height, r = dia/2 + 1, center = false);
    translate([0, 0, height])
    difference(){
        cylinder(h = height, r = dia/2 + 1, center = false);
        translate([0, 0, 1]);
        cylinder(h = height + 2, r = dia/2, center = false);
    }
}

 spring_holder(28.4, 5);
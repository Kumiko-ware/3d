$fa = 1;
$fs = 0.4;

length = 49;
width = 38;
height = 25;
vert_ft_len = 5;
alpha = 55;
bar_r = 2.5;
pin_r = 4.5/2;
pin_len = 7;
pin_space = 25;

base = height/10;
diag_h = height - bar_r - (vert_ft_len + base);
diag_len = diag_h / cos(alpha);
diag_d = diag_h * tan(alpha);

module BAR() {
// vertical front
translate([bar_r , 0])
    cylinder(vert_ft_len + base, bar_r, bar_r);

// diagonal    
translate([bar_r, 0, base + vert_ft_len]){
    rotate([0, alpha/2, 0])
        sphere(bar_r);
    rotate([0, alpha, 0]) 
        cylinder(diag_len, bar_r, bar_r);
}

// horizontal
translate([bar_r + diag_d, 0, base + vert_ft_len + diag_h]){
    rotate([0, (alpha - 90)/2, 0]) 
        sphere(bar_r);
    rotate([0, 90, 0])
        cylinder(length - bar_r - (bar_r + diag_d), bar_r, bar_r);
}

// vertical rear
translate([length - bar_r, 0, height - bar_r])
    sphere(bar_r);

translate([length - bar_r, 0, 0])
    cylinder(height - bar_r, bar_r, bar_r);
}

module light() {
    scale([0.5, 1, 1])
    sphere(bar_r);
    rotate([90, 0, -90])
        cylinder(bar_r/4, bar_r, bar_r);
}

color("#008080"){
// base
translate([bar_r/2, bar_r/2, 0])
    cube([length - bar_r, width - bar_r, base]);
// left
translate([bar_r, 0, 0])
    cube([length - 2*bar_r, bar_r, base]);
// front    
translate([0, bar_r, 0])
    cube([bar_r, width - 2*bar_r, base]);
// rear    
translate([length - bar_r, bar_r, 0])
    cube([bar_r, width - 2*bar_r, base]);
//right
translate([bar_r, width - bar_r, 0])
    cube([length - 2*bar_r, bar_r, base]);

// BARS lateral
translate([0, bar_r, 0])    
    BAR();
translate([0, width - bar_r, 0])
    BAR();
// trans bars
translate([bar_r, bar_r, vert_ft_len + base])
    rotate([-90, 0, 0])
        cylinder(width - 2*bar_r, bar_r, bar_r);
        
translate([bar_r + diag_d, bar_r, height - bar_r])
    rotate([-90, 0, 0])
        cylinder(width - 2*bar_r, bar_r, bar_r);
        
translate([length - 2*bar_r, bar_r, height - bar_r])
    rotate([-90, 0, 0])
        cylinder(width - 2*bar_r, bar_r, bar_r);

// lights
translate([length - 2*bar_r, width/3, height + bar_r/2])
    light();
translate([length - 2*bar_r, width/3*2, height + bar_r/2])
    light();
    
// pins
translate([(length - pin_space - 2*pin_r)/2+pin_r, width/2, base])
    rotate([180,0,0])
        cylinder(pin_len - pin_r + base, pin_r, pin_r);
translate([(length - pin_space - 2*pin_r)/2+pin_r, width/2, - pin_len + pin_r])
            sphere(pin_r);
translate([(length - pin_space - 2*pin_r)/2 + pin_r + pin_space, width/2, base])
    rotate([180,0,0])
        cylinder(pin_len - pin_r + base, pin_r, pin_r);
translate([(length - pin_space - 2*pin_r)/2 + pin_r + pin_space, width/2, - pin_len + pin_r])
    sphere(pin_r);   
}


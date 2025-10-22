// Gmsh project created on Tue Oct 21 14:04:07 2025
Point(1) = {0, 0, 0, .1};
Point(2) = {1, 0, 0, .1};
Point(3) = {1, 1.01, 0, .1};
Point(4) = {0, 1, 0, .1};

Point(5) = {.4, 1, 0, .1};
Point(6) = {.2, 1.01, 0, .1};


Line(1) = {1, 2};
Line(2) = {2, 3};
Line(5) = {4, 1};
Line(3) = {3, 6};
Line(4) = {5, 4};

Physical Curve("bot", 5) = {1};
Physical Curve("right", 6) = {2};
Physical Curve("left", 8) = {5};
Physical Curve("top", 7) = {3, 4};


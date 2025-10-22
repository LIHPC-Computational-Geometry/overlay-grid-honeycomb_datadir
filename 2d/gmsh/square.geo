// Gmsh project created on Tue Oct 21 14:04:07 2025
Point(1) = {0, 0, 0, .1};
Point(2) = {1, 0, 0, .1};
Point(3) = {1, 1, 0, .1};
Point(4) = {0, 1, 0, .1};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Physical Curve("bot", 5) = {1};
Physical Curve("right", 6) = {2};
Physical Curve("top", 7) = {3};
Physical Curve("left", 8) = {4};

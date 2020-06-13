from CreateMatrix import createMatrix
from vector3d import Vector3D

p0 = Vector3D(0, 0, 0)
p1 = Vector3D(50, 0, 0)
p2 = Vector3D(0, 0, 100)

(origin, ax, ay, az) = createMatrix(p0, p1, p2)

print(origin, ax, ay, az);

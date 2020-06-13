# coding:sjis
from vector3d import Vector3D

a = Vector3D()
b = Vector3D(0, 1, 2)
c = Vector3D(1, 2, 3)

print("ああ", a, b, b.abs(), b.abs())

print(a, b, c)

print(-a, -b, -c)

print(a + b, b + c)

print(a - b, b - c)

print(a * 2, b * 3, c * 4)

print(2 * a, 3 * b, 4 * c)

print(a / 2, b / 3, c / 4)

print(a.length(), b.length(), c.length())

print(a.length2(), b.length2(), c.length2())

print(a.dot(b), b.dot(c))

print(a.cross(b), b.cross(c))
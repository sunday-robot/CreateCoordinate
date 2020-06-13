# 3次元ベクトルクラス
# coding:sjis

import math
from operator import __mul__

class Vector3D:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

	# 単項演算子"-"
	def __neg__(self):
		return Vector3D(-self.x, -self.y, -self.z)
	
	# 加算
	def __add__(self, v):
		return Vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

	# 減算
	def __sub__(self, v):
		return Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

	# ベクトル同士の乗算、除算は定義しない
	# (乗算は外積と内積の両方が考えられて混乱する、除算は乗算を定義しないことが理由)

	# 乗算(ベクトル * スカラー)
	def __mul__(self, s):
		return Vector3D(self.x * s, self.y * s, self.z * s)

	# 乗算(スカラー * ベクトル)
	def __ｒmul__(self, s):
		return __mul__(self, s)

	# 除算(ベクトル / スカラー)
	def __truediv__(self, s):
		return Vector3D(self.x / s, self.y / s, self.z / s)
	
	# 長さ
	def length(self):
		a = math.sqrt(self.length2())
		return a

	# 長さの二乗(複数のベクトルの長さ比較だけがしたい場合は、こちらのほうが速いというだけ)
	def length2(self):
		return self.x * self.x + self.y * self.y + self.z * self.z

	# 内積
	def dot(self, v):
		return self.x * v.x +  self.y * v.y + self.z * v.z

	# 外積
	def cross(self, v):
		x = self.y * v.z - self.z * v.y
		y = self.z * v.x - self.x * v.z
		z = self.x * v.y - self.y * v.x
		return Vector3D(x, y, z)

	# 単位ベクトル(長さを1にしたもの)	
	def unit(self):
		return self / self.length()

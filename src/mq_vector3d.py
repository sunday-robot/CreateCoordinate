# coding:sjis
# Vector3Dに、以下の拡張をするもの
# ・MQPointを引数とするコンストラクタを追加
# ・MQPointを生成するメソッドを追加

from vector3d import Vector3D

def fromMQPoint(mqpoint):
	return Vector3D(mqpoint.x, mqpoint.y, mqpoint.z)

def toMQPoint(v):
	return MQSystem.newPoint(v.x, v.y, v.z)

Vector3D.fromMQPoint = fromMQPoint
Vector3D.toMQPoint = toMQPoint

# 選択されている3角形から、ローカル座標系を設定した新たなオブジェクトを生成する。
# 一番長い辺に属さない頂点を原点とする。
# 原点
# をZ軸とする。この辺の終点を原点とし、始点をZ軸の向きとする。
# 三角形の面をXZ平面とする。面の表側がY軸の向きである。

# 入力チェック：
# 1つの三角形だけが選択されていること。

from vector3d import Vector3D
from CreateMatrix import createMatrix

def _fromMQPoint(mqpoint):
	return Vector3D(mqpoint.x, mqpoint.y, mqpoint.z)

def _toMQPoint(v):
	return MQSystem.newPoint(v.x, v.y, v.z)

# 入力値(三角形の頂点座標のリスト)を取得する
def _getInput():
	# MQOドキュメントから、選択されている3角形の面(Face)を取得する。
	# 三角形の面をinputFaceに、その三角形が属するオブジェクトをinputObjectにセットする。
	doc = MQSystem.getDocument()
	inputObject = None
	inputFace = None
	# MQOドキュメントの全オブジェクトを走査する(選択されているオブジェクトのリストを返すメソッドはMQOドキュメントにはない)
	# 複数選択されている可能性があるので、選択されている三角形の面が見つかっても走査は中断しない
	for oi in range(doc.numObject):
		obj = doc.object[oi]
		# ↓この判定は必要だったと思うがなぜなのかは忘れた…
		if not obj:
			continue
		# オブジェクトの全ての面(Face)を走査する。
		for fi in range(obj.numFace):
			if not doc.isSelectFace(oi, fi):
				continue
			face = obj.face[fi]
			if face.numVertex != 3:
				raise ValueError("三角形以外のものが選択されています。")
			if inputFace:
				raise ValueError("2つ以上の面が選択されています。")
			inputObject = obj
			inputFace = face
	if not inputFace:
		raise ValueError("1つも面が選択されていません。")

	# 三角形の頂点
	v0 = inputObject.vertex[face.index[0]]
	v1 = inputObject.vertex[face.index[1]]
	v2 = inputObject.vertex[face.index[2]]

	# 三角形の頂点の座標
	p0 = _fromMQPoint(v0.getPos())  # getPos()は、ワールド座標系の座標値を返すらしい。（ローカル座標を取得するにはローカル座標系情報を参照して自前で計算するしかない？)
	p1 = _fromMQPoint(v1.getPos())
	p2 = _fromMQPoint(v2.getPos())

	# 面が片面であれば、その情報も欲しいが、APIを見てもそのような情報は得られなさそう。

	return (p0, p1, p2)

# ローカル座標系の各軸のベクトルから、回転角(ヘッド、ピッチ、バンク)を算出する
def _calcRotation(ax, ay, az):
	matrix = MQSystem.newMatrix()
	matrix.set(1, 1, ax.x)
	matrix.set(1, 2, ax.y)
	matrix.set(1, 3, ax.z)
	matrix.set(2, 1, ay.x)
	matrix.set(2, 2, ay.y)
	matrix.set(2, 3, ay.z)
	matrix.set(3, 1, az.x)
	matrix.set(3, 2, az.y)
	matrix.set(3, 3, az.z)
	rotation = matrix.getRotation()
	return rotation

# ローカル座標系を設定したオブジェクトを生成する
def _createCoordinateObject(origin, rotation):
	obj = MQSystem.newObject()
	obj.rotation = rotation
	obj.translation = _toMQPoint(origin)
	return obj

def main():
	# 本コマンドの入力パラメータ--三角形の頂点座標のリスト--を取得する。
	try:
		(p0, p1, p2) = _getInput()
	except ValueError as ve:
		MQSystem.messageBox(str(ve))
		return

	# 三角形の頂点座標のリストから、ローカル座標系の原点と、各軸のベクトルを求める。
	(origin, ax, ay, az) = createMatrix(p0, p1, p2)
	
	# ローカル座標系の各軸のベクトルから、回転(ヘッド、ピッチ、バンク)を算出する
	rotation = _calcRotation(ax, ay, az)
	
	# ローカル座標系を設定したオブジェクトを生成する
	coordinateObject = _createCoordinateObject(origin, rotation)
	
	# オブジェクトをMQSystem.documentに登録する
	MQSystem.getDocument().addObject(coordinateObject)
	
main()

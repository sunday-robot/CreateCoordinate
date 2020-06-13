# coding:shift_jis
# 選択されている3角形から、ローカル座標系を設定した新たなオブジェクトを生成する。
# 一番長い辺に属さない頂点を原点とする。
# 原点
# をZ軸とする。この辺の終点を原点とし、始点をZ軸の向きとする。
# 三角形の面をXZ平面とする。面の表側がY軸の向きである。


# 三角形の頂点のリストから、ローカル座標系の原点と、主軸と副軸のベクトルを取得する
def _getOriginAndVectors(p0, p1, p2):
    # 三角形の各辺のベクトル
    v20 = p2 - p0
    v12 = p1 - p2
    v01 = p0 - p1

    # 三角形の各辺の長さ(どの辺が最長かを調べるために使用するだけなので、長さの二乗でもよい)
    l20 = v20.length2()
    l12 = v12.length2()
    l01 = v01.length2()

    # 一番長い辺を調べ、原点 origin, 主軸(Z軸)a1、副軸(X軸)a2を特定する
    if l01 > l12:
        if l01 > l20:
            # l01, (l20 | l12)
            origin = p2
            a1 = v12
            a2 = -v20
        else:
            # l20, (l12 | l20)
            origin = p1
            a1 = v01
            a2 = -v12
    else:
        if l12 > l20:
            # l12, (l01 | l20)
            origin = p0
            a1 = v20
            a2 = -v01
        else:
            # l20, l12, l01
            origin = p1
            a1 = v01
            a2 = -v12
    return (origin, a1, a2)

# 特定された主軸a1、副軸a2から、正規化されたZ軸、X軸、Y軸を生成する
def _calcAxes(a1, a2):
    az = a1.unit()
    ax = (a2 - a1 * a1.dot(a2) / a1.dot(a1)).unit()
    ay = az.cross(ax)
    return (ax, ay, az)

def createMatrix(p0, p1, p2):
    """
    @return: (原点座標, X軸, Y軸, Z軸)
    @param p0: 頂点座標1
    @param p1: 頂点座標2
    @param p2: 頂点座標3
    """
    (origin, a1, a2) = _getOriginAndVectors(p0, p1, p2)
    (ax, ay, az) = _calcAxes(a1, a2)
    return (origin, ax, ay, az)

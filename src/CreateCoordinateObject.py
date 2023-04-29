# �I������Ă���3�p�`����A���[�J�����W�n��ݒ肵���V���ȃI�u�W�F�N�g�𐶐�����B
# ��Ԓ����ӂɑ����Ȃ����_�����_�Ƃ���B
# ���_
# ��Z���Ƃ���B���̕ӂ̏I�_�����_�Ƃ��A�n�_��Z���̌����Ƃ���B
# �O�p�`�̖ʂ�XZ���ʂƂ���B�ʂ̕\����Y���̌����ł���B

# ���̓`�F�b�N�F
# 1�̎O�p�`�������I������Ă��邱�ƁB

from vector3d import Vector3D
from CreateMatrix import createMatrix

def _fromMQPoint(mqpoint):
	return Vector3D(mqpoint.x, mqpoint.y, mqpoint.z)

def _toMQPoint(v):
	return MQSystem.newPoint(v.x, v.y, v.z)

# ���͒l(�O�p�`�̒��_���W�̃��X�g)���擾����
def _getInput():
	# MQO�h�L�������g����A�I������Ă���3�p�`�̖�(Face)���擾����B
	# �O�p�`�̖ʂ�inputFace�ɁA���̎O�p�`��������I�u�W�F�N�g��inputObject�ɃZ�b�g����B
	doc = MQSystem.getDocument()
	inputObject = None
	inputFace = None
	# MQO�h�L�������g�̑S�I�u�W�F�N�g�𑖍�����(�I������Ă���I�u�W�F�N�g�̃��X�g��Ԃ����\�b�h��MQO�h�L�������g�ɂ͂Ȃ�)
	# �����I������Ă���\��������̂ŁA�I������Ă���O�p�`�̖ʂ��������Ă������͒��f���Ȃ�
	for oi in range(doc.numObject):
		obj = doc.object[oi]
		# �����̔���͕K�v�������Ǝv�����Ȃ��Ȃ̂��͖Y�ꂽ�c
		if not obj:
			continue
		# �I�u�W�F�N�g�̑S�Ă̖�(Face)�𑖍�����B
		for fi in range(obj.numFace):
			if not doc.isSelectFace(oi, fi):
				continue
			face = obj.face[fi]
			if face.numVertex != 3:
				raise ValueError("�O�p�`�ȊO�̂��̂��I������Ă��܂��B")
			if inputFace:
				raise ValueError("2�ȏ�̖ʂ��I������Ă��܂��B")
			inputObject = obj
			inputFace = face
	if not inputFace:
		raise ValueError("1���ʂ��I������Ă��܂���B")

	# �O�p�`�̒��_
	v0 = inputObject.vertex[face.index[0]]
	v1 = inputObject.vertex[face.index[1]]
	v2 = inputObject.vertex[face.index[2]]

	# �O�p�`�̒��_�̍��W
	p0 = _fromMQPoint(v0.getPos())  # getPos()�́A���[���h���W�n�̍��W�l��Ԃ��炵���B�i���[�J�����W���擾����ɂ̓��[�J�����W�n�����Q�Ƃ��Ď��O�Ōv�Z���邵���Ȃ��H)
	p1 = _fromMQPoint(v1.getPos())
	p2 = _fromMQPoint(v2.getPos())

	# �ʂ��Жʂł���΁A���̏����~�������AAPI�����Ă����̂悤�ȏ��͓����Ȃ������B

	return (p0, p1, p2)

# ���[�J�����W�n�̊e���̃x�N�g������A��]�p(�w�b�h�A�s�b�`�A�o���N)���Z�o����
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

# ���[�J�����W�n��ݒ肵���I�u�W�F�N�g�𐶐�����
def _createCoordinateObject(origin, rotation):
	obj = MQSystem.newObject()
	obj.rotation = rotation
	obj.translation = _toMQPoint(origin)
	return obj

def main():
	# �{�R�}���h�̓��̓p�����[�^--�O�p�`�̒��_���W�̃��X�g--���擾����B
	try:
		(p0, p1, p2) = _getInput()
	except ValueError as ve:
		MQSystem.messageBox(str(ve))
		return

	# �O�p�`�̒��_���W�̃��X�g����A���[�J�����W�n�̌��_�ƁA�e���̃x�N�g�������߂�B
	(origin, ax, ay, az) = createMatrix(p0, p1, p2)
	
	# ���[�J�����W�n�̊e���̃x�N�g������A��](�w�b�h�A�s�b�`�A�o���N)���Z�o����
	rotation = _calcRotation(ax, ay, az)
	
	# ���[�J�����W�n��ݒ肵���I�u�W�F�N�g�𐶐�����
	coordinateObject = _createCoordinateObject(origin, rotation)
	
	# �I�u�W�F�N�g��MQSystem.document�ɓo�^����
	MQSystem.getDocument().addObject(coordinateObject)
	
main()

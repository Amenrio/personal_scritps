

import maya.cmds as cmds

elastico = "grp_x_elastico"

lct_arms = ["clavicle", "upperArm", "lowerArm", "hand"]

lct_spine = ["pelvis", "spine00", "spine01", "spine02", "spine03", "spine04",
             "chest", "chestExtra", "neck00", "neck01", "neck02", "head", "headEnd"]

lct_legs = ["upperLeg", "lowerLeg", "foot", "toe", "toeEnd"]

bending_ctls = ["Bend00", "Bend01", "Bend02"]

grps = ["grp_x_skin", "grp_x_ctl", "grp_x_toolkit"]

lct_pinkie = ["pinkieFinger00", "pinkieFinger01",
              "pinkieFinger02", "pinkieFinger03", "pinkieFingerEnd"]

lct_ring = ["ringFinger00", "ringFinger01",
            "ringFinger02", "ringFinger03", "ringFingerEnd"]

lct_middle = ["middleFinger00", "middleFinger01",
              "middleFinger02", "middleFinger03", "middleFingerEnd"]

lct_index = ["indexFinger00", "indexFinger01",
             "indexFinger02", "indexFinger03", "indexFingerEnd"]

lct_thumb = ["thumbFinger00", "thumbFinger01",
             "thumbFinger02", "thumbFingerEnd"]


# listas globales para la posicion de los dedos
list_positions_pinkie = []
list_positions_ring = []
list_positions_middle = []
list_positions_index = []
list_positions_thumb = []

# nombre global para los dedos
fingers = ["pinkie", "ring", "middle", "index", "thumb"]
pelvis = "lct_c_pelvis"
chest_extra = "lct_c_chestExtra"
limb = ["Arm", "Leg"]
lct_armPosition = []
lct_legsPosition = []
bending_positions = []
joint_list = []

side = ["l", "r"]
groups = ["rig", "skin", "ctl", "toolkit"]


def create_chain(chain_list, position_list, chain_name, side):
    idx = 0
    joint_list = []

    for pos in position_list:
        newPosition = pos
        joint_list.append(cmds.joint(name="skin_{}_{}".format(
            side, chain_list[idx]), position=newPosition))
        idx += 1
    for j in joint_list:
        cmds.joint(j, e=True, oj="xzy", sao="zup", ch=True, zso=True)
        cmds.joint(joint_list[-1], e=True, oj="none", zso=True)
    cmds.select(clear=True)


def create_chain_fingers(chain_list, position_list, rotation_list, chain_name, side):
    idx = 0

    for pos, rot in zip(position_list, rotation_list):

        name = "skin_{}_{}".format(
            side, chain_list[idx])
        cmds.joint(name=name, position=pos)
        cmds.select(clear=True)
        cmds.xform("{}".format(name), ro=rot)
        idx += 1


def parent_fingers(s):
    for f in fingers:
        if f == "thumb":
            cmds.parent("skin_{}_{}FingerEnd".format(s, f),
                        "skin_{}_{}Finger02".format(s, f))
        else:
            cmds.parent("skin_{}_{}FingerEnd".format(s, f),
                        "skin_{}_{}Finger03".format(s, f))
            cmds.parent("skin_{}_{}Finger03".format(s, f),
                        "skin_{}_{}Finger02".format(s, f))

        cmds.parent("skin_{}_{}Finger02".format(s, f),
                    "skin_{}_{}Finger01".format(s, f))
        cmds.parent("skin_{}_{}Finger01".format(s, f),
                    "skin_{}_{}Finger00".format(s, f))


def create_symmetry_groups(chain_list, location, symmetry, scaleOffset, chain_name):

    symmetry_name = "grp_{}_skinSymmetry{}".format(location, chain_name)
    sym_position = cmds.xform(symmetry, q=True, ws=True, m=True)

    cmds.group(empty=True, a=True, name=symmetry_name)
    cmds.xform(symmetry_name, ws=True, m=sym_position)

    cmds.parent("skin_{}_{}".format(location, chain_list[0]), symmetry_name)
    zeroOrient("skin_{}_{}".format(location, chain_list[0]))
    if location is "r":
        cmds.setAttr("{}.scale{}".format(symmetry_name, scaleOffset), -1)

        if chain_name == limb[0]:
            cmds.rename("{}".format(symmetry_name), "grp_r_skinSymmetryArm")

        elif chain_name == limb[1]:
            cmds.rename("{}".format(symmetry_name), "grp_r_skinSymmetryLeg")

    cmds.select(clear=True)


def get_lct_positions(s, list_names):
    list_positions = []
    for l in list_names:
        name = "lct_{}_{}".format(s, l)
        pos = cmds.xform(name, q=True, t=True, ws=True)
        list_positions.append(pos)

    return list_positions


def get_lct_rotations(s, list_names):
    list_rotations = []
    for l in list_names:
        name = "lct_{}_{}".format(s, l)
        rot = cmds.xform(name, q=True, ro=True, ws=True)
        list_rotations.append(rot)

    return list_rotations


def parent_everything():
    for g in grps:
        cmds.parent(g, "grp_x_rig")

    cmds.select(clear=True)
    cmds.parent("skin_c_root", "grp_x_skin")
    cmds.parent("skin_c_pelvis", "skin_c_root")

    for s in side:
        cmds.parent("grp_{}_skinSymmetryArm".format(s), "skin_c_chestExtra")
        cmds.parent("grp_{}_skinSymmetryLeg".format(s), "skin_c_pelvis")

    cmds.select(clear=True)


def create_bending(jointPrincipal, chain_name, location):
    list_names = []
    for b in bending_ctls:
        list_names.append("{}{}".format(jointPrincipal, b))

    bending_positions = get_lct_positions("l", list_names)
    create_chain(list_names, bending_positions, chain_name, location)

# Cacho de codigo reutilizado gracias Angel o/


def zeroOrient(o):
    if cmds.nodeType(o) == 'joint':
        valueRotate = cmds.xform(o, q=True, ws=True, ro=True)
        parentObj = cmds.pickWalk(o, direction='up')

        if parentObj[0] != o:
            cmds.parent(o, world=True)

        cmds.setAttr(o + '.jointOrientX', valueRotate[0])
        cmds.setAttr(o + '.jointOrientY', valueRotate[1])
        cmds.setAttr(o + '.jointOrientZ', valueRotate[2])

        cmds.setAttr(o + '.rotateX', 0)
        cmds.setAttr(o + '.rotateY', 0)
        cmds.setAttr(o + '.rotateZ', 0)

        if parentObj[0] != o:
            cmds.parent(o, parentObj)

        valueX = cmds.getAttr(o + '.jointOrientX')
        valueY = cmds.getAttr(o + '.jointOrientY')
        valueZ = cmds.getAttr(o + '.jointOrientZ')

        cmds.setAttr(o + '.rotateX', valueX)
        cmds.setAttr(o + '.rotateY', valueY)
        cmds.setAttr(o + '.rotateZ', valueZ)

        cmds.setAttr(o + '.jointOrientX', 0)
        cmds.setAttr(o + '.jointOrientY', 0)
        cmds.setAttr(o + '.jointOrientZ', 0)

def run():
    cmds.select(all=True)
    importedScene = cmds.ls(selection=True)
    if elastico in importedScene:
        autoSkin()
    else:
        cmds.file("E:/03_scripts/99_mayaScenes/MRA_scn_elastico.mb",i=True)
def autoSkin():

    for g in groups:
        cmds.group(empty=True, a=True, name="grp_x_{}".format(g))

    cmds.joint(name="skin_c_root")
    zeroOrient("skin_c_root")
    cmds.select(clear=True)
    lct_pinkiePosition = get_lct_positions("l", lct_pinkie)
    lct_ringPosition = get_lct_positions("l", lct_ring)
    lct_middlePosition = get_lct_positions("l", lct_middle)
    lct_indexPosition = get_lct_positions("l", lct_index)
    lct_thumbPosition = get_lct_positions("l", lct_thumb)
    lct_pinkieRotation = get_lct_rotations("l", lct_pinkie)
    lct_ringRotation = get_lct_rotations("l", lct_ring)
    lct_middleRotation = get_lct_rotations("l", lct_middle)
    lct_indexRotation = get_lct_rotations("l", lct_index)
    lct_thumbRotation = get_lct_rotations("l", lct_thumb)
    lct_spinePosition = get_lct_positions("c", lct_spine)
    create_chain(lct_spine, lct_spinePosition, "Spine", "c")
    lct_armPosition = get_lct_positions("l", lct_arms)
    lct_legsPosition = get_lct_positions("l", lct_legs)
    for s in side:

        create_chain(lct_arms, lct_armPosition, limb[0], s)
        create_chain(lct_legs, lct_legsPosition, limb[1], s)
        create_chain_fingers(
            lct_pinkie, lct_pinkiePosition, lct_pinkieRotation, "finger", s)
        create_chain_fingers(lct_ring, lct_ringPosition,
                             lct_ringRotation, "finger", s)
        create_chain_fingers(
            lct_middle, lct_middlePosition, lct_middleRotation, "finger", s)
        create_chain_fingers(lct_index, lct_indexPosition,
                             lct_indexRotation, "finger", s)
        create_chain_fingers(lct_thumb, lct_thumbPosition,
                             lct_thumbRotation, "finger", s)
        parent_fingers(s)
        cmds.parent("skin_{}_pinkieFinger00".format(s),
                    "skin_{}_hand".format(s))
        cmds.parent("skin_{}_ringFinger00".format(s), "skin_{}_hand".format(s))
        cmds.parent("skin_{}_middleFinger00".format(s),
                    "skin_{}_hand".format(s))
        cmds.parent("skin_{}_indexFinger00".format(s),
                    "skin_{}_hand".format(s))
        cmds.parent("skin_{}_thumbFinger00".format(s),
                    "skin_{}_hand".format(s))
        cmds.select(clear=True)
        create_bending("upperArm", "Arm", s)
        create_bending("lowerArm", "Arm", s)
        create_bending("upperLeg", "Leg", s)
        create_bending("lowerLeg", "Leg", s)

        cmds.parent("skin_{}_upperArmBend00".format(s),
                    "skin_{}_upperArm".format(s))
        cmds.parent("skin_{}_lowerArmBend00".format(s),
                    "skin_{}_lowerArm".format(s))
        cmds.parent("skin_{}_upperLegBend00".format(s),
                    "skin_{}_upperLeg".format(s))
        cmds.parent("skin_{}_lowerLegBend00".format(s),
                    "skin_{}_lowerLeg".format(s))

    cmds.select(all=True, hi=True)
    joints = cmds.ls(selection=True)
    for o in joints:
        zeroOrient(o)

    for s in side:
        create_symmetry_groups(lct_arms, s, chest_extra, "X", limb[0])
        create_symmetry_groups(lct_legs, s, pelvis, "X", limb[1])

    parent_everything()
    cmds.setAttr("skin_r_toe.rotateX", 0)
    cmds.setAttr("skin_l_toe.rotateX", 0)
    cmds.select(all=True, hi=True)
    joints = cmds.ls(selection=True)
    for o in joints:
        if cmds.nodeType(o) == 'joint':
            cmds.setAttr(o + ".displayLocalAxis", 1 )

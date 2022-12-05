import maya.cmds as cmds
import MRA_scr_rig_checkPipeline_v02 as CP
import MRA_namingPipeline_v02 as NMP
import MRA_library_variableNames_v02 as VARS


def checkOrient(*args):
    listMistakes = []

    selection = cmds.ls(selection=True, dag=True, transforms=True)
    if not selection:
        cmds.select("grp_x_rig")

    selection = cmds.ls(selection=True, dag=True, transforms=True)

    for o in selection:
        if cmds.nodeType(o) == "joint":
            jntOri = cmds.getAttr(o + ".jointOrient")
            orient = jntOri[0]
            error = 0
            for j in orient:

                if j > (-0.0001) and j < (0.0001):
                    continue
                else:
                    error += 1
            if error > 0:
                listMistakes.append(o)

    MRA_OPUI(listMistakes)
    # print(listMistakes)


def MRA_OPUI(object):

    if cmds.window('MRA_OPUI', exists=True):
        cmds.deleteUI('MRA_OPUI')

    ventanaUI = cmds.window(
        'MRA_OPUI', t="MRA Check Orient Joints", rtf=True, s=True, mnb=False, mxb=False)

    cmds.columnLayout(adjustableColumn=True)
    cmds.rowLayout(adjustableColumn=4)

    cmds.setParent("..")
    scrollLayout = cmds.scrollLayout(cr=True)

    cmds.separator(style='none', height=5)
    cmds.text("Lista de Joints")
    cmds.separator(style='none', height=5)
    if len(object) > 0:
        for o in object:
            command = "cmds.select('{}')".format(o)

            cmds.button(label="{0}".format(o), c=command, bgc=[0.65, 0.3, 0.3])
    else:
        cmds.text(label="    No se encontraron orientaciones en los joints    ",
                  align="center", h=30, bgc=[0.1, 1, 0.1], fn="boldLabelFont")

    cmds.showWindow(ventanaUI)

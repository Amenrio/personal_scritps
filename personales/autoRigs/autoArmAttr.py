"""
SCRIPT para crear PLANTILLA para un attr_l_brazo
MRA_plantillaSquashStretchLimbs.py

"""

import maya.cmds as cmds

node_name = ["attr_r_arm", "attr_l_arm", "attr_l_leg", "attr_r_leg"]
attr = ["IKFKSwitch","IKAutoStretch","BendingCtls","BreakJointCtl"]

jnt_l_chain = ["jnt_l_upperArm","jnt_l_lowerArm","jnt_l_hand"]
cik_l_chain = ["cik_l_upperArm","None","cik_l_hand"]

jnt_r_chain = ["jnt_r_upperArm","jnt_r_lowerArm","jnt_r_hand"]
cik_r_chain = ["cik_r_upperArm","None","cik_r_hand"]

def create_nurbs_shapes():
##Creates All Atributes
    for n in node_name:
        limb = n.split("_")

        cmds.createNode('transform',name=str(n.upper()))
        cmds.createNode('nurbsCurve',name = n,p=n.upper())

        cmds.select(n)
        attr_shape = cmds.ls(selection=True)
        for a in attr:
            if a is "IKAutoStretch":
                cmds.addAttr(longName = a, at="enum",en="OFF:STR:SQSH")
            elif a is "BreakJointCtl":
                if limb[2] == "arm":
                    cmds.addAttr(longName = a, at="enum",en="OFF:ON",nn="Break Elbow Ctl")
                else:
                    cmds.addAttr(longName = a, at="enum",en="OFF:ON",nn="Break Knee Ctl")
            else:
                cmds.addAttr(longName = a, at="enum",en="OFF:ON")
            cmds.setAttr("{}.{}".format(n,a), cb=True)

def create_node_network():
    for n in node_name:
        side_flag = n.split("_")

        l_elbow_translate = cmds.getAttr("{}.translateX".format(jnt_l_chain[1]))
        l_hand_translate = cmds.getAttr("{}.translateX".format(jnt_l_chain[2]))
        r_elbow_translate = cmds.getAttr("{}.translateX".format(jnt_r_chain[1]))
        r_hand_translate = cmds.getAttr("{}.translateX".format(jnt_r_chain[2]))

        nameOp= "{}_{}_operation".format(side_flag[1],side_flag[2])
        nameConvert= "{}_{}_convertTranslate".format(side_flag[1],side_flag[2])
        nameDist = "{}_{}_distance".format(side_flag[1],side_flag[2])
        nameNorm = "{}_{}_norm".format(side_flag[1],side_flag[2])
        nameCondt = "{}_{}_cond".format(side_flag[1],side_flag[2])


        cmds.shadingNode('distanceBetween',asUtility=True,name = nameDist)

        cmds.shadingNode('multiplyDivide',asUtility=True,name=nameOp)
        cmds.setAttr("{}.input2X".format(nameOp),2)

        cmds.shadingNode('multiplyDivide',asUtility=True,name=nameNorm)
        cmds.setAttr("{}.operation".format(nameNorm),2)
        cmds.shadingNode('condition',asUtility=True,name=nameCondt)
        cmds.shadingNode('multiplyDivide',asUtility=True,name = nameConvert)




        cmds.connectAttr("{}.{}".format(n,attr[1]), "{}.input1X".format(nameOp))
        cmds.connectAttr("{}.distance".format(nameDist), "{}.input1X".format(nameNorm))

        cmds.connectAttr("{}.outputX".format(nameNorm), "{}.colorIfTrueR".format(nameCondt))
        cmds.connectAttr("{}.distance".format(nameDist), "{}.firstTerm".format(nameCondt))
        cmds.connectAttr("{}.outputX".format(nameOp), "{}.operation".format(nameCondt))

        cmds.connectAttr("{}.outColorR".format(nameCondt),"{}.input1X".format(nameConvert))
        cmds.connectAttr("{}.outColorR".format(nameCondt),"{}.input1Y".format(nameConvert))


        if side_flag[1] == "l":
            if side_flag[2] == "arm":
                cmds.connectAttr("{}.worldMatrix[0]".format(cik_l_chain[0]),"{}.inMatrix1".format(nameDist))
                cmds.connectAttr("{}.worldMatrix[0]".format(cik_l_chain[2]),"{}.inMatrix2".format(nameDist))
                left_total_distance = cmds.getAttr("{}.distance".format(nameDist))
                cmds.setAttr("{}.secondTerm".format(nameCondt), left_total_distance)
                cmds.setAttr("{}.input2X".format(nameNorm), left_total_distance)
                cmds.connectAttr("{}.outputX".format(nameConvert),"{}.translateX".format(jnt_l_chain[1]))
                cmds.connectAttr("{}.outputY".format(nameConvert),"{}.translateX".format(jnt_l_chain[2]))
                cmds.setAttr("{}.input2X".format(nameConvert),l_elbow_translate)
                cmds.setAttr("{}.input2Y".format(nameConvert),l_hand_translate)

        else:
            if side_flag[2] == "arm":
                cmds.connectAttr("{}.worldMatrix[0]".format(cik_r_chain[0]),"{}.inMatrix1".format(nameDist))
                cmds.connectAttr("{}.worldMatrix[0]".format(cik_r_chain[2]),"{}.inMatrix2".format(nameDist))
                right_total_distance = cmds.getAttr("{}.distance".format(nameDist))
                cmds.setAttr("{}.secondTerm".format(nameCondt), right_total_distance)
                cmds.setAttr("{}.input2X".format(nameNorm), right_total_distance)
                cmds.connectAttr("{}.outputX".format(nameConvert),"{}.translateX".format(jnt_r_chain[1]))
                cmds.connectAttr("{}.outputY".format(nameConvert),"{}.translateX".format(jnt_r_chain[2]))
                cmds.setAttr("{}.input2X".format(nameConvert),r_elbow_translate)
                cmds.setAttr("{}.input2Y".format(nameConvert),r_hand_translate)

def run_autoRig():
    create_nurbs_shapes()
    create_node_network()

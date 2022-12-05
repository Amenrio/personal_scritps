import maya.cmds as cmds
import MRA_library_variableNames_v02 as VARS


def IHI():
    selection = cmds.ls(selection=True)

    for sel in selection:
        sName = sel

        relatives = cmds.listRelatives(sel, s=True)
        
        for r in relatives:

            newName = VARS.get_nice_name_shapes(r)
            if len(newName) > 1:
                if newName[0] != "attr":
                    cmds.setAttr(sName+"|"+r + ".ihi", 0)

            else:
                cmds.setAttr(sName+"|"+r + ".ihi", 0)

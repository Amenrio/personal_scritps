"""Custom Module to hide nonimportant nodes from ChannelBox history
"""

import maya.cmds as cmds
from cpl.scripts import libraryNaming as lib


def IHI():
    """From selection, searches its relatives and hides everything except
    Nodes with "attr" in its name
    """
    selection = cmds.ls(selection=True)

    for sel in selection:
        sName = sel

        relatives = cmds.listRelatives(sel, s=True)

        for r in relatives:

            newName = lib.get_nice_name_shapes(r)
            if len(newName) > 1:
                if newName[0] != "attr":
                    cmds.setAttr(sName+"|"+r + ".ihi", 0)

            else:
                cmds.setAttr(sName+"|"+r + ".ihi", 0)

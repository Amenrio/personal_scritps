#CheckPipeline ANIM2 CDAV
#MRA script para comprobar Pipeline de ANIMACION 2 CDAV
import MRA_library_variableNames_v02 as VARS  # Libreria de variables
import MRA_orientPipeline_v02 as ORP
import MRA_namingPipeline_v02 as NMP
import maya.cmds as cmds


def MRA_checkPipeline():
    #print messageErrorRigPipe
    window_name = "MRA_checkPipeline"
    window_title = "MRA Check Pipeline"
    window_w = 275
    window_h = 195
    #Check if window already exists
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)

    #Window properties
    window = cmds.window(window_name, sizeable=False, t=window_title,
                         w=window_w, h=window_h, mnb=0, mxb=0, nde=True)
    #Create the Main Layout

    main_layout = cmds.scrollLayout(cr=True)
    cmds.separator(style='none', height=10)
    cmds.text("Check Orient in Joints", align="center",
              h=30, backgroundColor=[0.36, 0.36, 0.36],
              font="boldLabelFont")
    cmds.separator(style='none', height=10)
    cmds.button(label="Check Orient Pipeline", h=40,
                c=ORP.checkOrient, bgc=[0.682, 0.616, 0.851])

    cmds.separator(style='none', height=10)
    cmds.text("Pipeline Animacion", align="center",
              h=30, backgroundColor=[0.36, 0.36, 0.36],
              font="boldLabelFont")
    cmds.separator(style='none', height=10)
    cmds.button(label="Check Naming Pipeline", h=40,
                c=NMP.check_naming_pipeline, bgc=[0.682, 0.616, 0.851])
    cmds.separator(style='none', height=10)

    cmds.showWindow(window)

# MRA script para comprobar Naming de ANIMACION 2

import maya.cmds as cmds
import MRA_library_variableNames_v02 as VARS  # Libreria de variables


# Listas globales


# Filtra el namespace (en caso de existir) y divide el nombre del objeto (en los " _ ") en un array de 3 partes, node_type_flag_name
def get_nice_name(name_obj):
    if (name_obj.find(':')) > 0:
        obj = name_obj.split(':')
        parts_obj = obj[1].split("_")
        return parts_obj

    else:
        parts_obj = name_obj.split("_")
        return parts_obj

# Detecta errores en el naming pipeline, devuelve 0 si detecta algun error


def check_naming(name_obj):
    if (name_obj.find(":")) > 0:             #
        obj = name_obj.split(":")            # Detecta Namespace en el objeto
        LE_NAMESPACES.append(name_obj)       #

        if(obj[1].find("_")) < 0:           #
            # Analiza si es correcto el nombre fuera del namespace
            LE_NAMING.append(obj[1])

    elif (name_obj.find("|")) > 0:
        obj = name_obj.split("|")
        if(obj[1].find("_")) < 0:
            LE_NAMING.append(name_obj)
    else:
        if(name_obj.find("_")) < 0:
            LE_NAMING.append(name_obj)  # Comprueba si es correcto el nombre


# Comprueba si existen nombres duplicados, devuelve 0 si detecta algun error
def check_duplicates(name_obj):
    if(name_obj.find("|")) > 0:
        LE_DUPLICATED.append(name_obj)


# Compara con dos diccionarios si las dos primeras partes del objeto cumplen el naming (naming_maya y location_flags), si no lo cumplen, se anaden a las listas de errores

def check_syntax(name_obj):
    obj = get_nice_name(name_obj)
    if len(obj) > 3 or len(obj) < 2:
        LE_WARNINGS.append(name_obj)
    else:
        # si obj[0] existe dentro de los valores del diccionario namingMaya
        if obj[0] not in VARS.naming_maya.values():
            LE_WARNINGS.append(name_obj)

        # si obj[1] existe dentro de los valores del diccionario locationFlags
        elif obj[1] not in VARS.location_flags.values():

            LE_WARNINGS.append(name_obj)



# Codigo principal
def check_naming_pipeline(*args):
    global LE_NAMESPACES  # Lista de Namespaces
    global LE_NAMING  # Lista de errores por Naming
    global LE_DUPLICATED  # Lista de elementos con nombres duplicados
    global LE_WARNINGS  # Lista de elementos de warnings de, ejemplo, sintaxis o flags
    LE_NAMESPACES = []
    LE_NAMING = []
    LE_DUPLICATED = []
    LE_WARNINGS = []

    selection = cmds.select(all=True)
    all_objects = cmds.ls(selection=True, dag=True, transforms=True)

    for o in all_objects:
        check_naming(o)

    for o in all_objects:
        check_duplicates(o)

    for o in all_objects:
        check_syntax(o)

    naming_pipeline_ui(LE_NAMING, LE_NAMESPACES,
                       LE_DUPLICATED, LE_WARNINGS)


def naming_pipeline_ui(error_list, namespace_list, duplicated_list, warning_list):
    window_name = "naming_pipeline_ui"
    window_title = "MRA Naming Pipeline"
    window_w = 275
    window_h = 400
    # Check if winow already exists
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)

    # Window porperties
    window = cmds.window(window_name, t=window_title,
                         s=True, mnb=0, mxb=0, rtf=True)
    layout = cmds.scrollLayout(cr=True)
    cmds.separator(style='none', height=5)
    cmds.text("Lista de Objetos")
    cmds.separator(style='none', height=5)
    if len(error_list) > 0:
        cmds.frameLayout("No cumplen el naming convention: {0}".format(
            len(error_list)), p=layout, bgc=[0.4, 0.1, 0.1], bgs=True, fn="boldLabelFont")
        for o in error_list:
            command = "cmds.select('{0}')".format(o)
            cmds.button(o, bgc=[1, 0.338, 0.338], c=command)
        cmds.separator(style='none', height=10, p=layout)

    if len(duplicated_list) > 0:
        cmds.frameLayout("Objetos con nombres duplicados: {0}".format(len(
            duplicated_list)), p=layout, bgc=[1, 0.206, 0], bgs=True, fn="boldLabelFont")
        for j in duplicated_list:
            command = "cmds.select('{0}')".format(j)
            cmds.button(label="  {}  ".format(j), bgc=[
                        1, 0.875, 0.231], c=command)
        cmds.separator(style='none', height=10, p=layout)

    if len(warning_list) > 0:
        cmds.frameLayout("Posibles fallos u objetos mal escritos: {0} ".format(
            len(warning_list)), p=layout, bgc=[0.068,0.068,0.068])
        for k in warning_list:
            command = "cmds.select('{0}')".format(k)
            cmds.button(label="  {}  ".format(k), bgc=[0.125,0.125,0.125], c=command)

        cmds.separator(style='none', height=10, p=layout)

    if len(namespace_list) > 0:
        cmds.frameLayout("Presencia de Namespace: {0}".format(
            len(namespace_list)), p=layout, bgc=[0, 0.45, 1], bgs=True, fn="boldLabelFont")
        for l in namespace_list:
            command = "cmds.select('{0}')".format(l)
            cmds.button(label="  {}  ".format(l), bgc=[0, 0.781, 1], c=command)
    if len(error_list) == 0 and len(duplicated_list) == 0 and len(warning_list) == 0 and len(namespace_list) == 0:
        cmds.text(label="    No se encontraron errores en el Naming    ",
                  h=30, p=layout, bgc=[0.1, 1, 0.1], fn="boldLabelFont")

    cmds.showWindow(window)

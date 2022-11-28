@echo off
ECHO Instalando CheckPipeline en Maya2022
set MAYA_SCR_DIR="%HOMEDRIVE%%HOMEPATH%/Documents/maya/2022/prefs/scripts"

set MAYA_SHE_DIR="%HOMEDRIVE%%HOMEPATH%/Documents/maya/2022/prefs/shelves"

if exist %MAYA_SCR_DIR% (
    cd CheckPipeline
    xcopy *.py %MAYA_SCR_DIR%
    echo Scripts intsalados
)else (
    echo Error, no se encontro el directorio prefs/scripts para maya 2022!
)

if exist %MAYA_SHE_DIR% (
    cd ../Shelves
    xcopy *.mel %MAYA_SHE_DIR%
    echo Shelf instalada
)else (
    echo Error, no se encontro el directorio prefs/shelves para maya 2022!
)

PAUSE
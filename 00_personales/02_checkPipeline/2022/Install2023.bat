@echo off
set MAYA_SCR_DIR="%HOMEDRIVE%%HOMEPATH%/Documents/maya/2022/prefs/scripts"

set MAYA_SHE_DIR="%HOMEDRIVE%%HOMEPATH%/Documents/maya/2022/prefs/shelves"


if exist %MAYA_SCR_DIR% (
    cd CheckPipeline
    xcopy *.py %MAYA_SCR_DIR%
)else (
    echo Error!
)

if exist %MAYA_SHE_DIR% (
    cd ../Shelves
    xcopy *.mel %MAYA_SHE_DIR%
)else (
    echo Error!
)


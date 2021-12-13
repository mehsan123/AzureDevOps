@echo off
setlocal
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 10/08/2020                                      |
rem |                                                             |
rem | Program to parse a .tbmspec file and an .xml file which     |
rem | contains the description of the source code.                |
rem | For each low level requirement, there should be a field     |
rem | calld "Reference". This "Reference" function is looked up   |
rem | in the .xml file and if found then the function is "mapped" |
rem | to the requirement. Finally a .tbmspec file is created      |
rem | containing just the updated low level requirements.         |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set PYTHON_PATH=%TBED%\Utils\Python
set PRJ=Cashregister

set ROOT=%~dp0
set PROJECT_TBMSPEC=%ROOT%%PRJ%.tbmspec
set MAPPING_TBMSPEC=%ROOT%Mapping.tbmspec
if exist knownsource.xml set SOURCE_XML=%ROOT%knownsource.xml
if exist Source_Description.xml set SOURCE_XML=%ROOT%Source_Description.xml
set LOG=%ROOT%\Generate_Mapping.log
set PATH=%PYTHON_PATH%;%TBED%;%NTP%;%PATH%

rem First check that all the files, paths etc exist
rem ===============================================
if not exist "%PYTHON_PATH%\python.exe" (
  @echo Requires Python 2.7 or above
  pause
  exit
)

if not exist "%PROJECT_TBMSPEC%" (
  @echo missing %PROJECT_TBMSPEC%
  pause
  exit
)

if not exist "%SOURCE_XML%" (
  @echo missing %SOURCE_XML%
  pause
  exit
)


rem Delete any existing files
rem =========================
if exist %MAPPING_TBMSPEC% del /F %MAPPING_TBMSPEC%
if exist %LOG% del /F %LOG%


rem Execute the python script
rem =========================
@echo on
python.exe "Generate_Mapping.py" %PROJECT_TBMSPEC% %SOURCE_XML% %MAPPING_TBMSPEC%
@echo off


rem Finally display the result
rem ==========================
if exist %MAPPING_TBMSPEC% %MAPPING_TBMSPEC%

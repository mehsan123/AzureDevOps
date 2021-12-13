@echo off
setlocal
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 11/08/2020                                      |
rem |                                                             |
rem | Program to parse a .tbmspec file and for each Test Case of  |
rem | type External Task. Set the "Program" to the value of the   |
rem | Custom Attribute "Program".                                 |
rem | Adds placeholders for the input/output/reference documents. |
rem | Create a new .tbmspec file which contains just the Test     |
rem | Cases of type Unit Test. Remove any unnecessary tags etc    |
rem | and then update the documentation and description fields    |
rem | from the information found in the .tcf file.                |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set PYTHON_PATH=%TBED%\Utils\Python
set PRJ=Cashregister

set ROOT=%~dp0
set PROJECT_TBMSPEC=%ROOT%%PRJ%.tbmspec
set TASKS_TBMSPEC=%ROOT%ExternalTasks.tbmspec
set LOG=%ROOT%\Set_External_Tasks.log
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

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


rem Delete any existing files
rem =========================
if exist %TASKS_TBMSPEC% del /F %TASKS_TBMSPEC%
if exist %LOG% del /F %LOG%

@echo on
python.exe "Set_External_Tasks.py" %PROJECT_TBMSPEC% %TASKS_TBMSPEC%
@echo off

rem Finally display the result
rem ==========================
if exist %TASKS_TBMSPEC% %TASKS_TBMSPEC%

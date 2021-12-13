@echo off
setlocal
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 10/08/2020                                      |
rem |                                                             |
rem | Program to parse a .tbmspec file and for each Test Case of  |
rem | type Unit Test, locate the associated .tcf file and parse   |
rem | it to find the sequence documentation.                      |
rem | Create a description containing for each test case, the     |
rem | name of the procedure and the description of the test case. |
rem | Create a new .tbmspec file which contains just the Test     |
rem | Cases of type Unit Test, remove any unnecessary tags etc    |
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
set TESTCASES_TBMSPEC=%ROOT%TestCases.tbmspec
set TCF_ROOT=%ROOT%LowLevelTests
set LOG=%ROOT%\Update_Test_Cases_from_TCFs.log
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

rem First check that all the files, paths etc exist
rem ===============================================
if not exist "%PYTHON_PATH%\python.exe" (
  @echo Requires Python 2.7 or above
  pause
  exit
)

if not exist "%TCF_ROOT%" (
  @echo missing %TCF_ROOT%
  pause
  exit
) else (
  if not exist "%TCF_ROOT%\*.tcf" (
    @echo no tcf files in %TCF_ROOT%
    pause
    exit
  )
)

if not exist "%PROJECT_TBMSPEC%" (
  @echo missing %PROJECT_TBMSPEC%
  pause
  exit
)


rem Delete any existing files
rem =========================
if exist %TESTCASES_TBMSPEC% del /F %TESTCASES_TBMSPEC%
if exist %LOG% del /F %LOG%


rem Execute the python script
rem =========================
@echo on
python.exe "Update_Test_Cases_from_TCFs.py" %PROJECT_TBMSPEC% %TESTCASES_TBMSPEC% %TCF_ROOT%
@echo off


rem Finally display the result
rem ==========================
if exist %TESTCASES_TBMSPEC% %TESTCASES_TBMSPEC%

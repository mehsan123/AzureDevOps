@echo off
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 09/01/2020                                      |
rem |                                                             |
rem | Program to read a set that has been analysed and            |
rem | automatically create a light grey box sequence for each     |
rem | function that isolates the function.                        |
rem | Testers can then use new from sequence to start creating    |
rem | tests. Finally they would export the sequence.              |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set PYTHON_PATH=%TBED%\Utils\Python
set PRJ=Cashregister

set ROOT=%~dp0
set TCF_ROOT=%ROOT%Initial_UnitTests
set LOG=%ROOT%\Create_ut_tcfs.log
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

if exist "%TBED%\TBbrowse.exe" (
  set GLH=%WORK%\%PRJ%_tbwrkfls\%PRJ%.glh
) else (
  set GLH=%WORK%\%PRJ%_tbwrkfls\%PRJ%.ldra
)

set XML=%WORK%\%PRJ%_tbwrkfls\%PRJ%.xml

rem First check that all the files, paths etc exist
rem ===============================================
if not exist "%PYTHON_PATH%\python.exe" (
  @echo Requires Python 2.7 or above
  pause
  exit
)

if not exist "%GLH%" (
  @echo missing %GLH%
  pause
  exit
)

copy %WORK%\Examples\Workshops\Generate_xml\Release\Generate_xml.exe %TBED%\Generate_xml.exe

if not exist "%TCF_ROOT%" (
  md %TCF_ROOT%
)


if exist %LOG% del /F %LOG%


rem Generating XML from analysis results
rem ====================================
@echo Generating xml
start /wait "ldra" /min Generate_xml.exe %GLH%


rem Execute the python script
rem =========================
@echo on
python.exe "Create_ut_tcfs.py" %PRJ% %XML% %TCF_ROOT%
@echo off

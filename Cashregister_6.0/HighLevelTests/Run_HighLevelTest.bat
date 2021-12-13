@echo off
setlocal enableextensions enabledelayedexpansion
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 01/05/2020                                      |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set HLR_TEST=%1

if ["%HLR_TEST%"]==[""] (
  @echo Must pass the name of a High Level Test
  pause
  exit /B 1
)

cd ..\..
set ROOT=%cd%

set PRJ=Cashregister
set PYTHON_PATH=%TBED%\Utils\Python
set PATH=%PYTHON_PATH%;%TBED%;%PATH%
set SRC_FILES=%ROOT%\%PRJ%.tcf

set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Section="C/C++ %COMPILER% LDRA Testbed"
if exist "%TBED%\contestbed.exe" set TOOL=start "ldra" /wait /min contestbed
if exist "%TBED%\conunit.exe" set TOOL=start "ldra" /wait /min conunit

rem Run the Instrumentation and Build
rem =================================
@echo Running Instrumentation and Build
%TOOL% %SRC_FILES% /212q

cd /d %WORK%
if exist *.exh del /F *.exh
%ROOT%\Source\%PRJ%.exe < %ROOT%\HighLevelTests\In\HLR_Input_%HLR_TEST%.txt > %ROOT%\HighLevelTests\Out\HLR_Output_%HLR_TEST%.txt
cd /d %ROOT%

python.exe Configuration\file_compare.py HighLevelTests\Out\HLR_Output_%HLR_TEST%.txt HighLevelTests\Ref\HLR_Reference_%HLR_TEST%.txt

set STATUS=%errorlevel%

rem Perform the dynamic analysis
rem ============================
%TOOL% %SRC_FILES% /32panq /dataset=%HLR_TEST%

exit /B %STATUS%

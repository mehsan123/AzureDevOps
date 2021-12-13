@echo off
setlocal
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 01/05/2020                                      |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set PRJ=Cashregister
set COMPILER=MinGW200 GCC C/C++ v3.2
set PATH=%TBED%;%PATH%
set ROOT=%~dp0
set CONFIG_DIR=%ROOT%Configuration

rem Configure relative paths 
rem ========================
set SRC_FILES=%ROOT%%PRJ%.tcf
set WORK_DIR=%WORK%\%PRJ%_tbwrkfls

if exist "%TBED%\contestbed.exe" set TOOL=start "ldra" /wait /min contestbed
if exist "%TBED%\conunit.exe" set TOOL=start "ldra" /wait /min conunit

set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Section="C/C++ %COMPILER% LDRA Testbed"
set TBP=%ROOT%TBmanager\%PRJ%.tbp
set TBM=start "ldra" /wait /min TBmanager.exe %TBP% /first=%FIRST% /last=%LAST%
set FIRST="Jane"
set LAST="Wilson"


rem Delete the existing set and work directory
rem ==========================================
@echo Deleting Existing Results
%TOOL% /delete_set=%PRJ%
if exist %WORK_DIR% rmdir /s /q %WORK_DIR%

rem Set up necessary testbed.ini options
rem ====================================
@echo Configuring Testbed.ini
%TBI% COMPILER_SELECTED="%COMPILER%"
%TBS% CM_TOOL_SELECTED=Subversion
%TBS% CM_ADD_VERSION_TO_REPORTS=TRUE
%TBS% DYNAMIC_REPORT_CONFIGURATION=DO-178C Level A
%TBS% FILE_LIMIT=32
%TBS% TBRUN_LOCAL_STUB_HIT_COUNTS=TRUE
%TBS% TBRUN_TC_SETJMP=TRUE
%TBS% METFILE=%CONFIG_DIR%\metpen.dat


rem restore project to initial state
rem ================================
@echo Restoring project to initial state
if exist *.xml del /F *.xml
if exist *.htm del /F *.htm
if exist *.html del /F *.html
if exist *.exh del /F *.exh
if exist *.txt del /F *.txt
if exist *.cfg del /F *.cfg
if exist Cashregister.tbp del /F Cashregister.tbp
if exist *.tbmspec del /F *.tbmspec
if exist *.log del /F *.log
if exist report_storage rmdir /s /q report_storage 
if exist baselines rmdir /s /q baselines 
if exist tbreq rmdir /s /q tbreq 
cd Source
call clean > nul
cd ..
cd HighLevelTests
if exist *.log del /F *.log 
cd ..
cd LowLevelTests
if exist *.csp del /F *.csp 
cd ..
cd Configuration
if exist *.log del /F *.log
cd..

xcopy /S /Q /i TBmanager_Template . > nul

if errorlevel 1 pause

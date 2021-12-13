@echo off
setlocal enableextensions enabledelayedexpansion
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 10/08/2020                                      |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+


rem Configure variables that are likely to change
rem =============================================
set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set PRJ=Cashregister
set COMPILER=MinGW200 GCC C/C++ v3.2
set PATH=%TBED%;%PATH%
set ROOT=%~dp0
set CONFIG_DIR=%ROOT%Configuration
set START_TIME=%TIME%

rem Configure relative paths 
rem ========================
set SRC_FILES=%ROOT%%PRJ%.tcf
set WORK_DIR=%WORK%\%PRJ%_tbwrkfls


if exist "%TBED%\contestbed.exe" set TOOL=start "ldra" /wait /min contestbed
if exist "%TBED%\conunit.exe" set TOOL=start "ldra" /wait /min conunit
set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Section="C/C++ %COMPILER% LDRA Testbed"


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


rem Run the Main Static, Complexity Analysis, Data Flow, Information Flow & Instrumentation
rem =======================================================================================
@echo Running Analysis and Instrumentation
%TOOL% %SRC_FILES% /112a34021q


rem Run each sequence in the TCF directory
rem ======================================
set TCF_ROOT=%ROOT%LowLevelTests
set TESTS=0
for %%i in (%TCF_ROOT%\*.tcf) do set /A TESTS=TESTS+1
set TEST=0
for %%i in (%TCF_ROOT%\*.tcf) do (
  set /A TEST=TEST+1
  @echo !TEST!/!TESTS! : %%i 
  %TOOL% %SRC_FILES% /1q /tbruntcf=%%i /tbruntcfargs="-regress -quit"
)


rem Generate a Test Manager Report
rem ==============================
@echo Generating a Test Manager Report
%TOOL% %SRC_FILES% /generate_overview_rep


rem Display Execution Time
rem ======================
set END_TIME=%TIME%
set options="tokens=1-4 delims=:.,"
for /f %options% %%a in ("%START_TIME%") do set start_h=%%a&set /a start_m=100%%b %% 100&set /a start_s=100%%c %% 100&set /a start_ms=100%%d %% 100
for /f %options% %%a in ("%END_TIME%") do set end_h=%%a&set /a end_m=100%%b %% 100&set /a end_s=100%%c %% 100&set /a end_ms=100%%d %% 100

set /a hours=%end_h%-%start_h%
set /a mins=%end_m%-%start_m%
set /a secs=%end_s%-%start_s%
set /a ms=%end_ms%-%start_ms%

if %ms% lss 0 set /a secs = %secs% - 1 & set /a ms = 100%ms%
if %secs% lss 0 set /a mins = %mins% - 1 & set /a secs = 60%secs%
if %mins% lss 0 set /a hours = %hours% - 1 & set /a mins = 60%mins%
if %hours% lss 0 set /a hours = 24%hours%
if 1%ms% lss 100 set ms=0%ms%
@echo Time taken %mins% mins %secs% secs


rem Open the Test Manager Report
rem ============================
if exist "%WORK_DIR%\%PRJ%_reports\%PRJ%.ovs.htm" "%WORK_DIR%\%PRJ%_reports\%PRJ%.ovs.htm"
if exist "%WORK_DIR%\%PRJ%.ovs.htm" "%WORK_DIR%\%PRJ%.ovs.htm"

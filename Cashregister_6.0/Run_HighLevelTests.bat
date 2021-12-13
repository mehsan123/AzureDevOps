@echo off
setlocal enableextensions enabledelayedexpansion
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 07/05/2021                                      |
rem |                                                             |
rem |    Copyright (C) 2021 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set WORK=C:\_LDRA_Workarea\1002_RC3
set PRJ=Cashregister
set COMPILER=MinGW200 GCC C/C++ v3.2
set PATH=%TBED%;%PATH%
set ROOT=%~dp0
set CONFIG_DIR=%ROOT%Configuration
set TOTAL_TESTS=0
set PASSED_TESTS=0
set START_TIME=%TIME%

set WORK_DIR=%WORK%\%PRJ%_tbwrkfls
set REPORT=%PRJ%_HighLevelTests.html

if exist "%TBED%\TBbrowse.exe" (
  set TOOL_SUITE_VERSION=9.8.5
  set TEST_MANAGER_REPORT="%WORK_DIR%\%PRJ%.ovs.htm"
  set DYNAMIC_DATA_FLOW_REPORT="%WORK_DIR%\%PRJ%.cvs.htm"
) else (
  set TOOL_SUITE_VERSION=10.0.0
  set TEST_MANAGER_REPORT="%WORK_DIR%\%PRJ%_reports\%PRJ%.ovs.htm"
  set DYNAMIC_DATA_FLOW_REPORT="%WORK_DIR%\%PRJ%_reports\%PRJ%.dpo.htm"
  set TBREPORTS=start "ldra" /wait /min tbreports
)

rem Get date
rem ========
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set TEST_DATE=%Day%/%Month%/%Year%
set COPYRIGHT_YEAR=%Year%

rem Set Paths
rem =========
set PYTHON_PATH=%TBED%\Utils\Python
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

rem First check that all the files, paths etc exist
rem ===============================================
if not exist "%PYTHON_PATH%\python.exe" (
  @echo Requires Python 2.7 or above
  pause
  exit
)


rem Create Report
rem =============
if exist "%REPORT%" del /F "%REPORT%"
copy %CONFIG_DIR%\ReportTemplates\Head.html "%REPORT%">nul
@echo Creating %REPORT%


rem Configure relative paths 
rem ========================
set SRC_FILES=%ROOT%%PRJ%.tcf

set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Section="C/C++ %COMPILER% LDRA Testbed"
if exist "%TBED%\contestbed.exe" set TOOL=start "ldra" /wait /min contestbed
if exist "%TBED%\conunit.exe" set TOOL=start "ldra" /wait /min conunit


rem Set up necessary testbed.ini options
rem ====================================
%TBI% COMPILER_SELECTED="%COMPILER%"
%TBS% CM_TOOL_SELECTED=Subversion
%TBS% CM_ADD_VERSION_TO_REPORTS=TRUE
%TBS% DYNAMIC_REPORT_CONFIGURATION=DO-178C Level A
%TBS% FILE_LIMIT=32
%TBS% TBRUN_LOCAL_STUB_HIT_COUNTS=TRUE
%TBS% TBRUN_TC_SETJMP=TRUE
%TBS% METFILE=%CONFIG_DIR%\metpen.dat


rem Delete the existing set and work directory
rem ==========================================
@echo Deleting Existing Results
%TOOL% /delete_set=%PRJ%
if exist %WORK_DIR% rmdir /s /q %WORK_DIR%


rem Run the Analysis
rem ================
@echo Running Analysis
%TOOL% %SRC_FILES% /112a345q


rem Run the Instrumentation and Build
rem =================================
@echo Running Instrumentation and Build
%TOOL% %SRC_FILES% /212q


rem Run all High Level Tests
rem ========================
call :RUN_TEST Add_Products "Start a session and add a number of products using the barcode and the special keys, then quit."
call :RUN_TEST Cancel_Session "Start a session, then cancel and quit."
call :RUN_TEST Cancelling_Products "Start a session, add two products, then cancel both and finally cancel the session and quit."
call :RUN_TEST Count_Shopping_Basket_Products "Start a session, add 50 products, add another product, end the session and quit." 
call :RUN_TEST Display_Help_When_Incorrect_Input "Enter an incorrect command, then quit."
call :RUN_TEST Display_Help_When_Requested "Enter h to display help, then quit."
call :RUN_TEST Display_Removed_Product "Start a session, add a product, cancel the product, then quit."
call :RUN_TEST Display_Ticket "Start a session, enter multiple products via both barcodes and special keys, then end the session and quit."
call :RUN_TEST Display_When_Scanned "Start a session, enter valid barcode, an invalid barcode, then quit."
call :RUN_TEST Empty_When_End "Start a session, enter a barcode, end session and quit."
call :RUN_TEST Filling_The_Basket "Start a session enter 50 products, end session, then quit."
call :RUN_TEST Generate_Ticket "Start a session, enter one of each product, end session and quit."
call :RUN_TEST Ignoring_Erroneous_Commands "Without starting a session, enter all the commands that should be ignored until a session is started, then quit."
call :RUN_TEST Inform_End_Session "Start a session, end the session, then quit."
call :RUN_TEST Key_In_Process_Barcodes "Start a session, enter a barcode one digit at a time, then quit."
call :RUN_TEST Manage_User_Interface_Session "Start a session, restart the session, end the session, end again the session, then quit."
call :RUN_TEST Start_With_Empty "End a session, Start a session, enter product, end session, then quit."
call :RUN_TEST User_Input "Start a session, add product, cancel product, add two products, cancel both products, run random command, then quit."
@echo total tests = %TOTAL_TESTS%


rem Generate a Test Manager Report
rem ==============================
%TOOL% %SRC_FILES% /generate_overview_rep


rem Perform the Dynamic Data Flow Coverage
rem ======================================
%TOOL% %SRC_FILES% /35q
if exist "%TBED%\TBbrowse.exe" (
  %TOOL% %SRC_FILES% /generate_dyndflow_report=html
) else (
  %TBREPORTS% %WORK_DIR%\%PRJ%.ldra -datacoupling_report
)

rem Measure Execution Time
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
@echo Time taken %hours%:%mins%:%secs%


rem Create the HTML report
rem ======================
python.exe %CONFIG_DIR%\add_tail.py %ROOT%%REPORT% %CONFIG_DIR%\ReportTemplates\Tail.html %COPYRIGHT_YEAR% 
python.exe %CONFIG_DIR%\finalise_report.py "%ROOT%%REPORT%" "%PRJ%" "%TEST_DATE%" "%mins% mins %secs% secs" "%TOOL_SUITE_VERSION%" "%TEST_MANAGER_REPORT%" "%DYNAMIC_DATA_FLOW_REPORT%" "%TOTAL_TESTS%" "%PASSED_TESTS%"


rem Open the HTML report
rem ====================
if exist "%ROOT%%REPORT%" "%ROOT%%REPORT%"

exit

rem ================================= SUBROUTINES =================================================


rem ========================
rem Subroutine to run a test
rem ========================
:RUN_TEST
set HLR_TEST=%1
set TEST_DESCRIPTION=%2
set /A TOTAL_TESTS=TOTAL_TESTS+1
set TEST_NUMBER=%TOTAL_TESTS%

cd /d %WORK%
if exist *.exh del /F *.exh
%ROOT%Source\%PRJ%.exe < %ROOT%HighLevelTests\In\HLR_Input_%HLR_TEST%.txt > %ROOT%HighLevelTests\Out\HLR_Output_%HLR_TEST%.txt
cd /d %ROOT%

python.exe Configuration\file_compare.py HighLevelTests\Out\HLR_Output_%HLR_TEST%.txt HighLevelTests\Ref\HLR_Reference_%HLR_TEST%.txt

if %errorlevel% == 0 (
  @echo Test %TEST_NUMBER%/18 : %HLR_TEST% : Passed
  set /A PASSED_TESTS=PASSED_TESTS+1
  python.exe %CONFIG_DIR%\add_test_case.py %ROOT%%REPORT% %CONFIG_DIR%\ReportTemplates\PassedTest.html %TEST_NUMBER% %HLR_TEST% %TEST_DESCRIPTION%
) else (
  @echo ERROR: Test %TEST_NUMBER%/18 : %HLR_TEST% : Failed
  python.exe %CONFIG_DIR%\add_test_case.py %ROOT%%REPORT% %CONFIG_DIR%\ReportTemplates\FailedTest.html %TEST_NUMBER% %HLR_TEST% %TEST_DESCRIPTION%
)

rem Perform the dynamic analysis
rem ============================
%TOOL% %SRC_FILES% /32panq /dataset=%HLR_TEST%

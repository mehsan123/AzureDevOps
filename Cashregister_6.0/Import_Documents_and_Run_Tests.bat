@echo off
setlocal enabledelayedexpansion
rem +-------------------------------------------------------------+
rem |    Author : M.W.Richardson                                  |
rem |    Date   : 10/08/2020                                      |
rem |                                                             |
rem | Batch file to automate the import of documents into         |
rem | TBmanager and then to run all tests and generate reports    |
rem |                                                             |
rem |    Copyright (C) 2020 Liverpool Data Research Associates    |
rem +-------------------------------------------------------------+

set TBED=C:\_LDRA_Toolsuite\1002_RC3
set PRJ=Cashregister
set COMPILER=MinGW200 GCC C/C++ v3.2
set PATH=%TBED%;%PATH%
set ROOT=%~dp0
set CONFIG_DIR=%ROOT%Configuration
set START_TIME=%TIME%

rem Set Paths
rem =========
set PYTHON_PATH=%TBED%\Utils\Python
set PATH=%PYTHON_PATH%;%TBED%;%PATH%

rem Configure relative paths 
rem ========================
set SRC_FILES=%ROOT%%PRJ%.tcf
set WORK_DIR=%WORK%\%PRJ%_tbwrkfls

if exist "%TBED%\contestbed.exe" set TOOL=start "ldra" /wait /min contestbed
if exist "%TBED%\conunit.exe" set TOOL=start "ldra" /wait /min conunit

set FIRST="Jane"
set LAST="Wilson"
set TBI=start "ldra" /wait /min TBini.exe
set TBS=%TBI% /Section="C/C++ %COMPILER% LDRA Testbed"
set TBP=%ROOT%%PRJ%.tbp
set TBM=start "ldra" /wait /min TBmanager.exe %TBP% /first=%FIRST% /last=%LAST%


rem Delete the existing set and work directory
rem ==========================================
@echo Deleting Existing Results
%TOOL% /delete_set=%PRJ%
if exist %WORK_DIR% rmdir /s /q %WORK_DIR%
cd Source
call Clean > nul
if exist inszt_*.c del /F inszt_*.c
cd ..


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
if exist .lock* del /F .lock*            
if exist *.xml del /F *.xml
if exist *.htm del /F *.htm
if exist *.exh del /F *.exh
if exist *.txt del /F *.txt
if exist *.cfg del /F *.cfg
if exist %PRJ%.tbp del /F %PRJ%.tbp
if exist *.tbmspec del /F *.tbmspec
if exist *.log del /F *.log
if exist report_storage rmdir /s /q report_storage 
if exist baselines rmdir /s /q baselines 
if exist tbreq rmdir /s /q tbreq 

xcopy /S /Q /i TBmanager_Template . > nul



rem Open project, add source code from tcf and perform analysis
rem ===========================================================
@echo Add source code and run analysis
%TBM% /add_source_from_tcf="%SRC_FILES%" /analyse_source /close


rem Re-read all documents
rem =====================
@echo Import word documents
echo %ROOT%Requirements\Cashregister_SLR.docx> Word_Docs.txt
echo %ROOT%Requirements\Cashregister_HLR.docx>> Word_Docs.txt
%TBM% /import_from_word_list=Word_Docs.txt /close

@echo Import excel documents
echo %ROOT%Requirements\Cashregister_LLR.xlsx> Excel_Docs.txt
echo %ROOT%HighLevelTests\Cashregister_HLT.xlsx>> Excel_Docs.txt
echo %ROOT%LowLevelTests\Cashregister_LLT.xlsx>> Excel_Docs.txt
%TBM% /import_from_excel_list=Excel_Docs.txt /close


rem Export the source code description and project
rem ==============================================
@echo Export source code description
%TBM% /export_source_desc=Source_Description.xml /close
@echo Export %PRJ%.tbmspec
%TBM% /export_tbmspec=%PRJ%.tbmspec /close


if not exist "%PYTHON_PATH%\python.exe" (
  @echo Unable to set external tasks or map functions, need to set Python path to Python27 or above
) else (
  @echo Set External Tasks Program from LLT "program" attribute
  python.exe %ROOT%Set_External_Tasks.py %PRJ%.tbmspec ExternalTasks.tbmspec
  
  @echo Generate Low Level Requirement to Source Code Mapping from LLR "reference" attribute
  python.exe %ROOT%Generate_Mapping.py %PRJ%.tbmspec Source_Description.xml Mapping.tbmspec

  rem Import External Tasks and Source Code Mapping
  rem =============================================
  @echo Import External Tasks 
  %TBM% /import_tbmspec=ExternalTasks.tbmspec /close

  @echo Import Source Code Mapping 
  %TBM% /import_tbmspec=Mapping.tbmspec /close
)


rem Instrument and build the code
rem =============================
@echo Instrument and build
start "ldra" /wait /min contestbed %SRC_FILES% /212q


rem Perform Code Review & Quality Review
rem ====================================
@echo Perform code review and quality review
%TBM% /verify_code_review_tcis /verify_quality_review_tcis /close


rem Perform External Tasks
rem ======================
@echo Perform external tasks
%TBM% /verify_external_task_tcis /close


rem Perform the Dynamic Analysis
rem ============================
start "ldra" /wait contestbed %SRC_FILES% /32panq /dataset=DynamicAnalysis


rem Generate Dynamic Data Flow Coverage Report
rem ==========================================
@echo Generate dynamic data flow coverage report
start "ldra" /wait /min TBini SCAN_ON_DEMAND=FALSE
start "ldra" /wait /min contestbed %SRC_FILES% /run_required_dyndflow /generate_dyndflow_report /q


rem Perform Unit Tests
rem ==================
@echo Perform unit tests
%TBM% /verify_unit_test_tcis /close


rem Perform Code Coverage Review
rem ============================
@echo Perform code coverage review
%TBM% /verify_code_coverage_tcis /close


rem All the traceability reports get the same name, so rename them each time
rem ========================================================================
@echo Generate reports
%TBM% /proj_coverage_summary_report /proj_coverage_report /traceability_report /source_mapping_report /defect_report /unit_test_regression_report /close

%TBM% /traceability_matrix_req_report="SLR,HLR" /close
for %%i in (%TMR%\*Traceability_Matrix_Report.html) do rename %%i SLR_HLR.html

%TBM% /traceability_matrix_req_report="HLR,LLR" /close
for %%i in (%TMR%\*Traceability_Matrix_Report.html) do rename %%i HLR_LLR.html

%TBM% /traceability_matrix_tci_report="HLR,HLT" /close
for %%i in (%TMR%\*Traceability_Matrix_Report.html) do rename %%i HLR_HLT.html

%TBM% /traceability_matrix_tci_report="LLR,LLT" /close
for %%i in (%TMR%\*Traceability_Matrix_Report.html) do rename %%i LLR_LLT.html

rem Remove unwanted reports
rem =======================
@echo Remove unwanted reports
for %%i in (%TMR%\*Traceability_Matrix_Report.html.txt) do del /F %%i


rem Generate a Baseline
rem ===================
@echo Creating a "Creation" baseline
%TBM% /new_project_baseline="Creation" /close


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
@echo Time taken %hours%:%mins%:%secs%


rem Finally open the report
rem =======================
set REPORT="%ROOT%report_storage\Traceability Summary Report.html"
if exist %REPORT% %REPORT%

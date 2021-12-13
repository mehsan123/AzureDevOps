#-----------------------------------------------------------------------------------
# | Python Script file to automate the import of documents into         |
# | TBmanager and then to run all tests and generate reports           |
#
# Pre-requisites : Requires Python 2.7 or above
#
# Author : J.A.Clare   
# Date   : 15/10/2020
# 
# Copyright (C) 2020 Liverpool Data Research Associates
#-----------------------------------------------------------------------------------

import os
import sys
import datetime
import subprocess
import shutil
from sys import platform as _platform


TBED = "%LDRA_TARGETDIR%"
WORK = "%LDRA_WORKFILESDIR%"

#This is for the windows executables
dotExe = ".exe"
#This is for windows command lines when communication with tbmanager
argumentIndicator = "/" 
if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
#This is for Linux or MacOS.
   dotExe = ""
   argumentIndicator = "-"

CONTESTBED = TBED + os.sep + "contestbed" + dotExe
CONUNIT = TBED + os.sep + "conunit" + dotExe
TBMANAGER = TBED + os.sep + "tbmanager" + dotExe
TBINI = TBED + os.sep + "tbini" + dotExe

PRJ = "Cashregister"
COMPILER = "MinGW200 GCC C/C++ v3.2"
if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
#This is left blank for linux and mac.
   COMPILER = ""
   
ROOT = os.getcwd ()
CONFIG_DIR= ROOT + os.sep + "Configuration"
STARTTIME = datetime.datetime.now().strftime("%H:%M:%S")

PATH = TBED
if "PATH" in os.environ:
    PATH = PATH + os.environ ["PATH"]
bindir = ""
if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    bindir = "bin"
PYTHON_PATH = TBED + os.sep + "utils" + os.sep + "python" + os.sep + bindir + os.sep + "python" + dotExe
PATH = PYTHON_PATH + PATH

SRC_FILES = ROOT + os.sep + PRJ + ".tcf"
WORK_DIR = WORK + os.sep + PRJ + "_tbwrkfls"

TOOL = ""
if os.path.exists ( CONTESTBED ):
   TOOL = CONTESTBED
   
if os.path.exists ( CONUNIT ):
   TOOL = CONUNIT
   
if TOOL == "":
   print ("Cannot find contestbed or conunit in directory: " + TBED)
   exit ( -1 )

#TBmanager setup details
FIRST = "Jane"
LAST = "Wilson"
TBP = ROOT + os.sep + PRJ + ".tbp"
TBMANAGER = TBMANAGER + " " + TBP + " " + argumentIndicator + "first=" + FIRST + " " + argumentIndicator + "last=" + LAST

#TBini base command
TBS = TBINI + " -section=\"C/C++ " + COMPILER + " LDRA Testbed\""

#Delete Existing Results
print ("Deleting Existing Results.")
subprocess.call (TOOL + " -delete_set=" + PRJ, shell = True )
if os.path.exists (WORK_DIR):
    shutil.rmtree (WORK_DIR)

os.chdir ("Source")
sourceDirListing = os.listdir (".")
for file in sourceDirListing:
   if "inszt" in file:
      os.remove (file)
os.chdir ("..")

#Setup the necessary testbed.ini options
print ("Configuring Testbed.ini")
commands = ["COMPILER_SELECTED=\"" + COMPILER + "\"", "CM_TOOL_SELECTED=Subversion", "CM_ADD_VERSION_TO_REPORTS=TRUE", "DYNAMIC_REPORT_CONFIGURATIONS=DO-178C Level A", "FILE_LIMIT=32", "TBRUN_LOCAL_STUB_HIT_COUNTS=TRUE", "TBRUN_TC_SETJMP=TRUE", "METFILE=" + CONFIG_DIR + os.sep + "metpen.dat"]
for command in commands:
    subprocess.call (TBS + " " + command, shell = True )

#Restore the project to its initial state
extensions = [".lock",".xml",".htm",".exh",".txt",".cfg",PRJ + ".tbp", ".tbmspec", ".log"]
projDirListing = os.listdir (".")
for extension in extensions:
    for file in projDirListing:
        if extension in file:
             try:
                  os.remove (file)
             except:
                  print ("Cannot remove file: " + file)
if os.path.exists ("report_storage"):
    shutil.rmtree ("report_storage")
if os.path.exists ("baselines"):
    shutil.rmtree ("baselines")
if os.path.exists ("tbreq"):
    shutil.rmtree ("tbreq")

template_dir = os.listdir ("TBmanager_Template")
for file in template_dir:
    shutil.copyfile ("." + os.sep + "TBmanager_Template" + os.sep + file, "." + os.sep + file)
    

#Open the project, add source code from tcf and perform analysis
print ("Add source code and run analysis")
subprocess.call (TBMANAGER + " " + argumentIndicator + "add_source_from_tcf=" + SRC_FILES + " " + argumentIndicator + "analyse_source " + argumentIndicator + "close",shell = True )

#Re-read all documents
if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    print ("Importing CSV documents")
    with open ('CSV_Docs.txt', 'a+') as CSVDocs:
        CSVDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_SLR.csv\n")
        CSVDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_HLR.csv\n")
        CSVDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_LLR.csv\n")
        CSVDocs.write (ROOT + os.sep + "HighLevelTests" + os.sep + "Cashregister_HLT.csv\n")
        CSVDocs.write (ROOT + os.sep + "LowLevelTests" + os.sep + "Cashregister_LLT.csv")
    subprocess.call (TBMANAGER + " " + argumentIndicator + "import_from_csv_list=CSV_Docs.txt " + argumentIndicator + "close", shell = True )

else:
    print ("Importing word documents")
    with open ('Word_Docs.txt', 'a+') as wordDocs:
       wordDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_SLR.docx\n")
       wordDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_HLR.docx")
    subprocess.call (TBMANAGER + " " + argumentIndicator + "import_from_word_list=Word_Docs.txt " + argumentIndicator + "close", shell = True )

    print ("Importing excel documents")
    with open ('Excel_Docs.txt', 'a+') as excelDocs:
        excelDocs.write (ROOT + os.sep + "Requirements" + os.sep + "Cashregister_LLR.xlsx\n")
        excelDocs.write (ROOT + os.sep + "HighLevelTests" + os.sep + "Cashregister_HLT.xlsx\n")
        excelDocs.write (ROOT + os.sep + "LowLevelTests" + os.sep + "Cashregister_LLT.xlsx")
    subprocess.call (TBMANAGER + " " + argumentIndicator + "import_from_excel_list=Excel_Docs.txt " + argumentIndicator + "close", shell = True )

#Export the source code description and project
print ("Export source code description")
subprocess.call (TBMANAGER + " " + argumentIndicator + "export_source_desc=Source_Description.xml " + argumentIndicator + "close", shell = True)
print ("Export " + PRJ + ".tbmspec")
subprocess.call (TBMANAGER + " " + argumentIndicator + "export_tbmspec=" + PRJ + ".tbmspec " + argumentIndicator + "close", shell = True)

print ("Set External Tasks Program from LLT program attribute")
subprocess.call (PYTHON_PATH + " " + ROOT + os.sep + "Set_External_Tasks.py " + PRJ + ".tbmspec ExternalTasks.tbmspec", shell = True)
print ("Generate Low Level Requirement to Source Code Mapping from LLR reference attribute")
subprocess.call (PYTHON_PATH + " " + ROOT + os.sep + "Generate_Mapping.py " + PRJ + ".tbmspec Source_Description.xml Mapping.tbmspec", shell = True)

#Import External Tasks and Source Code Mapping
print ("Import External Tasks")
subprocess.call (TBMANAGER + " " + argumentIndicator + "import_tbmspec=ExternalTasks.tbmspec " + argumentIndicator + "close", shell = True )
print ("Import Source Code Mapping")
subprocess.call (TBMANAGER + " " + argumentIndicator + "import_tbmspec=Mapping.tbmspec " + argumentIndicator + "close", shell = True )

# Instrument and build the code
print ("Instrument and build")
subprocess.call (CONTESTBED + " " + SRC_FILES + " -212q", shell = True )

#Perform Code Review and Quality Review
print ("Performing Code Review and Quality Review")
subprocess.call (TBMANAGER + " " + argumentIndicator + "verify_code_review_tcis " + argumentIndicator + "verify_quality_review_tcis " + argumentIndicator + "close", shell = True)

#Perform external tasks
print ("Performing External Tasks")
subprocess.call (TBMANAGER + " " + argumentIndicator + "verify_external_task_tcis " + argumentIndicator + "close", shell = True)

#Perform the Dynamic Analysis
print ("Performing Dynamic Analysis")
subprocess.call (CONTESTBED + " " + SRC_FILES + " -32panq -datatset=DynamicAnalysis", shell = True)

#Generate Dynamic Data Flow Coverage Report
print ("Generating Dynamic Data Flow Coverage Report")
subprocess.call (TBINI + " SCAN_ON_DEMAND=TRUE", shell = True)
subprocess.call (CONTESTBED + " " + SRC_FILES + " -run_required_dyndflow -generate_dyndflow_report -q", shell = True)

#Perform Unit Tests
print ("Performing Unit Tests")
subprocess.call (TBMANAGER + " " + argumentIndicator + "verify_unit_test_tcis " + argumentIndicator + "close", shell = True)

#Perform Code Coverage Review
print ("Performing Code Coverage Review")
subprocess.call (TBMANAGER + " " + argumentIndicator + "verify_code_coverage_tcis " + argumentIndicator + "close", shell = True)

#All traceability reports get the same name so rename them each time.
print ("Generating traceability reports")
subprocess.call (TBMANAGER + " " + argumentIndicator + "proj_coverage_summary_report " + argumentIndicator + "proj_coverage_report " + argumentIndicator + "traceability_report " + argumentIndicator + "source_mapping_report " + argumentIndicator + "defect_report " + argumentIndicator + "unit_test_regression_report " + argumentIndicator + "close", shell = True)

tmrFolder = ROOT + os.sep + "report_storage" + os.sep + "Traceability_Matrix_Report"
subprocess.call (TBMANAGER + " " + argumentIndicator + "traceability_matrix_req_report=\"SLR,HLR\" " + argumentIndicator + "close", shell = True )

if os.path.exists (tmrFolder):
    tmrListing = os.listdir (tmrFolder)
    for file in tmrListing:
        if "Traceability_Matrix_Report.html" in file:
            newname = file.replace ("Traceability_Matrix_Report.html", "SLR_HLR.html")
            os.rename (tmrFolder + os.sep + file, tmrFolder + os.sep + newname)

subprocess.call (TBMANAGER + " " + argumentIndicator + "traceability_matrix_req_report=\"HLR,LLR\" " + argumentIndicator + "close", shell = True )

if os.path.exists (tmrFolder):
    tmrListing = os.listdir (tmrFolder)
    for file in tmrListing:
        if "Traceability_Matrix_Report.html" in file:
            newname = file.replace ("Traceability_Matrix_Report.html", "HLR_LLR.html")
            os.rename (tmrFolder + os.sep + file, tmrFolder + os.sep + newname)

subprocess.call (TBMANAGER + " " + argumentIndicator + "traceability_matrix_req_report=\"HLR,HLT\" " + argumentIndicator + "close", shell = True )

if os.path.exists (tmrFolder):
    tmrListing = os.listdir (tmrFolder)
    for file in tmrListing:
        if "Traceability_Matrix_Report.html" in file:
            newname = file.replace ("Traceability_Matrix_Report.html", "HLR_HLT.html")
            os.rename (tmrFolder + os.sep + file, tmrFolder + os.sep + newname)

subprocess.call (TBMANAGER + " " + argumentIndicator + "traceability_matrix_req_report=\"LLR,LLT\" " + argumentIndicator + "close", shell = True )

if os.path.exists (tmrFolder):
    tmrListing = os.listdir (tmrFolder)
    for file in tmrListing:
        if "Traceability_Matrix_Report.html" in file:
            newname = file.replace ("Traceability_Matrix_Report.html", "LLR_LLT.html")
            os.rename (tmrFolder + os.sep + file, tmrFolder + os.sep + newname)

#Remove unwanted reports
print ("Removing unwanted reports")
if os.path.exists (tmrFolder):
    tmrListing = os.listdir (tmrFolder)
    for file in tmrListing:
        if "Traceability_Matrix_Report.html" in file:
            os.remove (tmrFolder + os.sep + file)

#Generate a Baseline
print ("Creating a Creation baseline")
subprocess.call (TBMANAGER + "" + argumentIndicator + "new_project_baseline=\"Creation\" " + argumentIndicator + "close", shell = True)

#Displaying Execution Time
ENDTIME = datetime.datetime.now().strftime("%H:%M:%S")
FMT = '%H:%M:%S'
EXECUTIONTIME = datetime.datetime.strptime(ENDTIME, FMT) - datetime.datetime.strptime(STARTTIME, FMT)
print ("Time Taken: " + str (EXECUTIONTIME))

#Finally open the report
subprocess.call (ROOT + os.sep + "report_storage" + os.sep + "Traceability_Summary_Report.html", shell = True)

# <BEGIN COPYRIGHT HEADER>
# * =========================== LDRA Inc =========================== *
# * UNCLASSIFIED                *
# * FOR OFFICIAL USE ONLY                *

# * No license is required for the dissemination of the commercial information  *
# * contained herein to foreign persons other than those from or in the      *
# * terrorist supporting countries identified in the United States Export     *
# * Administration Regulations (EAR) (15 CFR 730-774). It is the responsibility *
# * of the individual in control of this data to abide by U.S. export laws.     *
# * LDRA PROPRIETARY   ECCN: 7D994           *
# * =========================================================================== *
# <END COPYRIGHT HEADER>
#OverallStaticAnalaysisMC.py
#@author: Ehsan Salehi (ehsan.salehi@ldra-usa.com)
#this script runs LDRA static analysis on the autocode code projects
#this script is to be run on the bamboo server nightly
import fnmatch
import os
import sys
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import bokeh
from bokeh.io import export_png

from bokeh.io import output_file, show
from bokeh.plotting import figure

#List of all the header files to be excluded
Filter_Header =[]
   
#List of all the Source files to be excluded
Filter_Source =[]
#Name of the Set inside of the TCF
SystemTesting = 'systemTesting'
######################################################################################
#  Class CodeReviewViolations 
# To Get all elements of violations
######################################################################################
class CodeReviewReport():
    def __init__(self, SourceCode, Standard, ruleNumber=[]):
        self.SourceCode = SourceCode
        self.Standard = Standard
        self.ruleNumber = ruleNumber
    
    def setSourceCode(SourceCode):
        self.SourceCode = SourceCode
        
    def setStandard(Standard):
        self.Standard = Standard
        
    def setRuleNumber(ruleNumber):
        self.ruleNumber = ruleNumber
    
    def getSourceName (self):
        return self.SourceCode
     
    def getStandardName(self):
        return self.Stanadrd
        
    def getRuleNumber (self):
        return self.ruleNumber
        
    def __str__(self):
        return (self.SourceCode, self.Standard, self.ruleNumber)
        
    def countViolations (self):
        allRules=[]
        violationLevel=[]
        violationCounter = []
        violationName=[]
        for child in self.ruleNumber:
            allRules.append(child.get('ldrarule'))
            

        for i in range (0,len(allRules)):
            if(allRules[i] not in violationName):
                violationName.append(allRules[i])
                violationLevel.append(self.ruleNumber[i].get('level'))
                violationCounter.append(allRules.count(allRules[i]))
            
        return violationName, violationCounter, violationLevel, self.SourceCode
        
        
    def violationPerLevel (self):
        allRules=[]
        violationCat=[]
        violationCounter = []
        violationName=[]
        for child in self.ruleNumber:
            violationLevel=child.get('level')
            if violationLevel not in violationCat:
                violationCat.insert(violationLevel)
            
        for child in self.ruleNumber:
            ruleNumber = child.get('ldrarule')
            
        
            
            
            
            
######################################################################################
#  Function main 
# This function init initialize all the command line argument
######################################################################################
def main():
    SourceMatches = []
    HeaderMatches =[]
    tcfName=''
    if len(sys.argv) < 4:
        print('Please pass the Source Directory Parameter')
        print('The second parameter is the toolsuite path. contestbed and contbbuild import should be in this folder')
        print('The third parameter is the folder you want to store the analysis results')
        print('')
        sys.exit(0)
        
    #run through all steps
    init()
    SourceMatches = findAllSourceCode(SourceMatches)
    print(len(SourceMatches))
    SourceMatches = fixSourceCode(SourceMatches)
    print(len(SourceMatches))
    #HeaderMatches = findAllHeaderFile(HeaderMatches)
    #HeaderMatches = fixHeaderFile(HeaderMatches)
    tcfName = createTCF(SourceMatches, HeaderMatches)
    #runanalysis(tcfName)
    countingViolations()
    
######################################################################################
#  Function init 
# This function init initialize all the command line argument
######################################################################################
def init():
    global sourceRoot, toolsuiteroot, workarearoot
    sourceRoot = sys.argv[1]
    toolsuiteroot = sys.argv[2]
    workarearoot = sys.argv[3]
    print('Source Root: '+sourceRoot)
    print('TOOLSUITE ROOT: ROOT: '+toolsuiteroot)
    print('WORKAREA ROOT: '+sourceRoot)
    #from fourth argument locate directory for specified project
    if not os.path.exists(workarearoot):
        os.makedirs(workarearoot)
        
######################################################################################
#  Function findAllSourceCode 
# This function finds all the source codes that are in the format .c and .cpp 
######################################################################################
def findAllSourceCode(SourceMatches):
    for root, dirnames, filenames in os.walk(sourceRoot):
        for filename in fnmatch.filter(filenames, '*.c'):
            SourceMatches.append('      File = '+ os.path.join(root, filename))
        for filename in fnmatch.filter(filenames, '*.cpp'):
            SourceMatches.append('      File = '+ os.path.join(root, filename))
    print ('The Number of Source code before filtering: '+str(len(SourceMatches)))
    return(SourceMatches)
    
######################################################################################
#  Function fixSourceCode 
# This function delete all the path that are subjected to be removed from the source 
#  code.
######################################################################################
def fixSourceCode(SourceMatches):
    tempSourceMatch=[]
    if (len(SourceMatches) > 0 ):
        i = 0
        
        for match in SourceMatches:
            flag = 0
            
            for element in Filter_Source:
                if element in match:
                    flag = 1
                    
            if flag == 0:
                tempSourceMatch.append(match)
            
    print ('The Number of Source code after filtering: '+str(len(tempSourceMatch)))
    return (tempSourceMatch)  
 
######################################################################################
#  Function findAllHeaderFile 
# This function will find all the header files  path to be included to the sysearch
######################################################################################
def findAllHeaderFile(HeaderMatches):
    for root, dirnames, filenames in os.walk(sourceRoot):
        for filename in fnmatch.filter(filenames, '*.h'):
            HeaderMatches.append('SearchPath = '+ os.path.join(root))
        for filename in fnmatch.filter(filenames, '*.hpp'):
            HeaderMatches.append('SearchPath = '+ os.path.join(root))
   
    HeaderMatches = list (set(HeaderMatches))
    print ('The Number of Header path before filtering: '+str(len(HeaderMatches)))
    return (HeaderMatches)
    
######################################################################################
#  Function fixHeaderFile 
# This function will delete all the header files that are in the filter list
######################################################################################
def fixHeaderFile(HeaderMatches):
    tempHeaderMatches=[]
    if (len(HeaderMatches) > 0 ):
        i = 0
        
        for match in HeaderMatches:
            flag = 0
            
            for element in Filter_Header:
                if element in match:
                    flag = 1
                    
            if flag == 0:
                tempHeaderMatches.append(match)
            
    print ('The Number of headers after filtering: '+str(len(tempHeaderMatches)))
    return (tempHeaderMatches)  
    
######################################################################################
#  Function createPTF 
# This function will create a TCF file
######################################################################################
def createTCF(SourceMatches, HeaderMatches):
    tcfName= sourceRoot+'\\'+SystemTesting+'.tcf'
    f = open(sourceRoot+SystemTesting+'.tcf','w+')
    f.write('# Begin Testbed  Set \n')
    f.write('\n   SET_TYPE = SYSTEM ')
    f.write('\n   SET_NAME = SystemTesting\n')
    f.write('\n   #Begin Source Files\n\n')
    f.write('\n'.join (SourceMatches))
    f.write('\n\n   # End Source Files\n')
    f.write('\n   # Begin Sysearch Include File Entries\n')
    f.write('\n'.join(HeaderMatches))
    #f.write('\nInsertInclude_203 = $(LDRA_CONFIG_ROOT)\LdraSystemHeaders.h\n')
    f.write('\n   # End Sysearch Include Files Entries\n')
    f.write('\n # End Testbed Set\n')
    f.write('\n# Begin Options')
    f.write('\n   open_all_includes = True')
    #f.write('   sysearch = F:\\LDRA\\sysearch_system.dat')
    f.write('\n   include = True')
    f.write('\n# End Options')

    f.close()
    return tcfName

######################################################################################
# Function countviolations 
# sum the violations for each project and output them to a csv file
######################################################################################

def countingViolations():
    violation =[]
    global codeReview
    everySource = []
    violationCount = []
    violationName = []
    violationSource = []
    violationLevel=[]
    print(workarearoot+'\Result.xml')
    codeReview = ET.parse(workarearoot+'\Result.xml')
    root = codeReview.getroot()
    for file in root.findall('files'):
        print (file)
        for glh in file.findall('file'):
            violation.append(glh)

    if (len(violation) == 0):
        sys.exit() 

    for obj in violation:
     
        everySource.append(CodeReviewReport(obj.get('source'),obj.get('model'),obj.findall('violation')))
    
    for i in range (0, len(everySource)-1):
        violationName.append(everySource[i].countViolations()[0])
        violationCount.append(everySource[i].countViolations()[1])
        violationLevel.append(everySource[i].countViolations()[2])
        violationSource.append(everySource[i].countViolations()[3])
    output_file("bars.html")


    p = figure(x_range=violationName[3], height=100, title=" violationCount",toolbar_location=None, tools="")
    p.vbar(x=violationName[3], top=violationCount[3], width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    export_png(p, filename = "Ptable.png")
        
######################################################################################
#  Function runanalysis 
# This function runs all the four phases of the static analysis
######################################################################################
def runanalysis(tcfName):
    #print('Static Analysis is started for: '++prjpath+'\\'+prjname)
    #cppcodestandard = '''"Name of Stanadrd"'''
    #ccodestandard = '''"Name of Standard for c code"'''
    
    #/112n34q run all phases of static analysis
    #-reanalyse_changed_set analyzes set if file has added/removed from set
    #-continue_system_analysis continues analysis even if a file fails analysis
    #-generate_code_review=HTML force generation of HTML code review report.
    os.system('dir')
    command = '{}contestbed.exe {} /112n34q  -reanalyse_changed_set -generate_code_review=HTML -tb_workfiledir={} -auto_macro -auto_macro_value="0"'.format(toolsuiteroot,tcfName, workarearoot) #pass ptf as parameter
    os.system(command)
    command = '{}integration_util.exe /arg=3 /1={}\Result.xml /2={}{} /3='.format(toolsuiteroot,workarearoot,workarearoot, tcfName[-17:-4]+'.glh')
    os.system(command)
    print("here is my command")
    print(command)
    os.system(command)
    
    
    
if __name__ == "__main__":
    main()

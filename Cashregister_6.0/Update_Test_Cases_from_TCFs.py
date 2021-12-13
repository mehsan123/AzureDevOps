#-----------------------------------------------------------------------------------
# Program to parse a .tbmspec file and for each Test Case of type Unit Test
# locate the associated .tcf file and parse it to find the sequence documentation
# Create a description containing each procedure and description of all test cases
#
# Create a new .tbmspec file which contains just the Test Cases of type Unit Test
# Remove any unnecessary tags etc and then update the documentation and description
# fields from the information found in the .tcf file
#
# Pre-requisites : Requires Python 2.7 or above
#
# Author : M.W.Richardson   
# Date   : 01/05/2020
# 
# Copyright (C) 2020 Liverpool Data Research Associates
#-----------------------------------------------------------------------------------

import os
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

# Variables
# ---------
tc_name=''
tc_description=''
tc_documentation=''
tc_tcf=''
tc_number=''
tc_num=0
tcf_documentation=''
tcf_description=''


# ------------------------------------------------------------------------------------------------------------------------
# Function to parse a tcf file
# returns tcf_documentation and tcf_description
# ------------------------------------------------------------------------------------------------------------------------
def parse_tcf(tcf_folder, tcf_name, log):
# List of all the various modes
  Search = 1
  Text = 2
  TestCase = 3

  mode = Search
  filestring = ''
  documentation = ''
  description = ''
  tc_procedure = ''
  tc_description = ''
  
  if not os.path.exists(tcf_folder + os.sep + tcf_name):
    log.write ('parse_tcf: Error: tcf file : ' + tcf_folder + os.sep + tcf_name + ' does not exist\n')
  else: 
    log.write ('parse_tcf: Parsing tcf file : ' + tcf_folder + os.sep + tcf_name + '\n')
  
    # Iterate over every line in the tcf file
    with open(tcf_folder + os.sep + tcf_name, 'r') as tcf:
      for line in tcf:
        if ( mode == Search ):
          if ( '# Begin Text' in line ):
            mode = Text
          elif ( '# Begin Test Case' in line ):
            mode = TestCase
      
        elif ( mode == Text ):
          if ( '# End Text' in line ):
            mode = Search
          else:
            documentation += line
    
        elif ( mode == TestCase ):
          if ( '# End Test Case' in line ):
            mode = Search
            description += tc_procedure + ' : ' + tc_description + '\n'
          elif ( 'Procedure = ' in line ):
            i = line.find ('Procedure = ')
            tc_procedure = line[i+12:-1]
          elif ( 'Description = ' in line ):
            i = line.find ('Description = ')
            tc_description = line[i+14:-1]
            
    log.write ('parse_tcf: documentation = \n' + quoteattr(documentation) + '\n')    
    log.write ('parse_tcf: description   = \n' + quoteattr(description) + '\n')
    return documentation, description

# -----------------------------------------------------------------------------------------------------------------------
  
# Create a log file
# -----------------
log = open('Update_Test_Cases_from_TCFs.log','w')


# Get all the passed arguments
# ----------------------------
if not len(sys.argv) == 4:
	log.write('Error: Incorrect number of arguments! Usage: ' + sys.argv[0] + ' project tbmspec file, testcase file, tcf folder\n' )
	sys.exit(1)

project_tbmspec_file=sys.argv[1]
testcase_tbmspec=sys.argv[2]
tcf_folder=sys.argv[3]

# Check that the tcf folder exists
# --------------------------------
if not os.path.isdir(tcf_folder):
  log.write('Error: The folder ' + tcf_folder + ' does not exist\n')
  sys.exit(1)



# Iterate over every test case of type Unit Test in the tbmspec file
# ------------------------------------------------------------------
tree = ET.parse(project_tbmspec_file)
root = tree.getroot()

for tc in root.findall('TestCase'):
  if (tc.get('type')=='Unit Test'):
    # We now have a TestCase of type Unit Test
    # ----------------------------------------
    tc_num = tc_num+1
    tc_name = tc.get('name')
    tc_number = tc.get('number')
    tc_tcf = tc.get('tcf')
    tc_description = tc.find('Description').text
    desc = tc.find('Description')
    
    # Parse the tcf and get the tcf_documentation and tcf_description
    tcf_documentation, tcf_description = parse_tcf(tcf_folder, tc_tcf, log)
    
    desc.text = quoteattr(tcf_description)

    for attr in tc.findall('CustomAttribute'):
      if (attr.get('name') == 'Documentation'):
        tc_documentation = attr.text
        attr.set ('value', quoteattr(tcf_documentation))
        
    log.write ('Test Case ' + str(tc_num) + ' :\n')
    log.write ('Number      : ' + tc_number + '\n')
    log.write ('TCF         : ' + tc_tcf + '\n')
    log.write ('Description : ' + tc_description + '\n\n')

    # Remove all unnecessary elements
    # -------------------------------
    for tag in tc.findall('Tag'):
      tc.remove(tag)

    for art in tc.findall('Artifact'):
      tc.remove(art)

    for ass in tc.findall('Asset'):
      tc.remove(ass)

      
# Remove everything except the Unit Tests
# ---------------------------------------
for tc in root.findall('TestCase'):
  if not (tc.get('type')=='Unit Test'):
    root.remove(tc)

for req in root.findall('Requirement'):
  root.remove(req)

for doc in root.findall('Document'):
  root.remove(doc)

for prg in root.findall('Program'):
  root.remove(prg)

for rol in root.findall('Role'):
  root.remove(rol)

for mac in root.findall('Macros'):
  root.remove(mac)

for grp in root.findall('GroupSpecification'):
  root.remove(grp)

  
# Finally write the new tbmspec that contains just the Test Cases
# ---------------------------------------------------------------
tree.write (testcase_tbmspec,encoding="UTF-8", xml_declaration=True)

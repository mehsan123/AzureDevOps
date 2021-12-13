#-----------------------------------------------------------------------------------
# Program to read a set and automatically create unit test tcf files
#
# Pre-requisites : Requires Python 2.7 or above
#
# Author : M.W.Richardson   
# Date   : 06/04/2018
# 
# Copyright (C) 2018 Liverpool Data Research Associates
#-----------------------------------------------------------------------------------

import os
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

#-----------------------------------------------------------------------------------------------------------------------
  
# Create a log file
# -----------------
log = open('Create_ut_tcfs.log','w')


# Get all the passed arguments
# ----------------------------
if not len(sys.argv) == 4:
  log.write('Error: Incorrect number of arguments! Usage: ' + sys.argv[0] + ' project name, xml file, tcf folder\n' )
  sys.exit(1)

proj_name  = sys.argv[1]
xml_file   = sys.argv[2]
tcf_folder = sys.argv[3]

log.write('Project Name: ' + proj_name + '\n')
log.write('XML File    : ' + xml_file + '\n')

# Check that the tcf folder exists
# --------------------------------
if not os.path.isdir(tcf_folder):
  log.write('Error: The folder ' + tcf_folder + ' does not exist\n')
  sys.exit(1)


# Find all the functions in the xml file
# --------------------------------------
tree = ET.parse(xml_file)
root = tree.getroot()
files = []

for file in root.findall('file'):
  files.append( file.get('name') )

for file in root.findall('file'):
  file_name = file.get('name')
  log.write('\nFile: ' + file_name + '\n')
  for elem in file.iter():
    if (elem.tag == 'functions'):
      for func in elem.findall('function'):
        func_name = func.get('name')
        if not (func_name == 'main'):
          log.write('  Function: ' + func_name)
          offset = 32 - len(func_name)
          for x in range(0, offset):
            log.write (' ')
          tcf_file = 'ut_' + func_name + '.tcf'
          # if the tcf_file doesn't exist or 
          # if it does exist but contains 'GENERATED_BY = Create_ut_tcfs.bat'
          # Then create the file, else do nothing
          bExists = False
          bUpdate = False
          if os.path.isfile(tcf_folder + os.sep + tcf_file):
            bExists = True
            with open(tcf_folder + os.sep + tcf_file,'r') as tcf:
              for line in tcf:
                if 'GENERATED_BY = Create_ut_tcfs.bat' in line:
                  bExists = False
                  bUpdate = True
                  break
            tcf.close
          
          if bExists == True:
            log.write(tcf_file + ' already exists\n')
          else:
            if bUpdate == True:
              log.write(tcf_file + ' updated\n')
            else:
              log.write(tcf_file + ' created\n')
            tcf = open(tcf_folder + os.sep + tcf_file,'w')
            tcf.write( '# Begin Testbed Set\n' )
            tcf.write( '  # Begin Source Files\n' )
            for f in files:
              tcf.write( '    RelativeFile = .' + os.sep + f + '\n' )
            tcf.write( '  # End Source Files\n' )
            tcf.write( '# End Testbed Set\n\n' )
            
            tcf.write( '# Begin Text\n' )
            tcf.write( 'This sequence tests the function ' + func_name + '.\n' )
            tcf.write( '# End Text\n\n' )

            tcf.write( '# Begin Attributes\n' )
            tcf.write( '  Sequence Name = ut_' + func_name + '\n' )
            tcf.write( '  Language Code = 2\n' )
            tcf.write( '# End Attributes\n\n' )

            tcf.write( '# Begin Isolated Procedure\n' )
            tcf.write( '  File = .' + os.sep + file_name + '\n' )
            tcf.write( '  Procedure = ' + func_name + '\n' )
            tcf.write( '# End Isolated Procedure\n\n' )

            tcf.write( '# Begin Selected Files from Set\n' )
            tcf.write( '  .' + os.sep + file_name + '\n' )
            tcf.write( '# End Selected Files from Set\n\n' )

            tcf.write( '# Begin Excluded Files\n' )
            for f in files:
              if not (file_name == f):
                tcf.write( '  .' + os.sep + f + '\n' )
            tcf.write( '# End Excluded Files\n\n' )

            tcf.write( '# Begin White Files\n' )
            tcf.write( '  .' + os.sep + file_name + '\n' )
            tcf.write( '# End White Files\n\n' )
          

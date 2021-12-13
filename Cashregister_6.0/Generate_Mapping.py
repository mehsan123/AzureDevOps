#-----------------------------------------------------------------------------------
# Program to parse a .tbmspec file and an .xml file containing the description of the
# source code. For each low level requirement, there should be a "Reference" field.
# This "Reference" function is looked up in the .xml file and if found then the
# function is "mapped" to the requirement
# Finally a .tbmspec file is created containing just the updated low level requirements
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

# ------------------------------------------------------------------------------------------------------------------------
# Function to parse an xml file looking for a function "reference"
# returns "path" to the function
# ------------------------------------------------------------------------------------------------------------------------
def parse_xml(xml_file, reference, log):

  set_name = ''
  source_description = ''
  source_file = 'not found'
  
#  log.write ('parse_xml: Searching file ' +  xml_file + ' for function :' + reference + '\n')
  
  # Iterate over every function
  # ---------------------------
  tree = ET.parse(xml_file)
  root = tree.getroot()

  for set in root.findall('set'):
    for file in set.findall('file'):
      for proc in file.findall('procedure'):
        if (proc.get('name')==reference):
          # We now have a Requirement of type Low Level
          # -------------------------------------------
          set_name = set.get('name')
          source_file = file.get('path')
          source_description = proc.get('ds')
          break

  if source_file == 'not found':
    log.write ('parse_xml: reference = ' + reference + ' not found\n')
    
  return set_name, source_file, source_description

# -----------------------------------------------------------------------------------------------------------------------
  
# Create a log file
# -----------------
log = open('Generate_Mapping.log','w')


# Get all the passed arguments
# ----------------------------
if not len(sys.argv) == 4:
  log.write('Error: Incorrect number of arguments! Usage: ' + sys.argv[0] + ' project tbmspec file, source xml file, mapping tbmspec file\n' )
  sys.exit(1)

project_tbmspec=sys.argv[1]
source_xml=sys.argv[2]
mapping_tbmspec=sys.argv[3]

log.write('project_tbmspec : ' + project_tbmspec + '\n' )
log.write('source_xml      : ' + source_xml + '\n' )
log.write('mapping_tbmspec : ' + mapping_tbmspec + '\n\n' )

# Iterate over every requirement of type Low Level in the tbmspec file
# ------------------------------------------------------------------
tree = ET.parse(project_tbmspec)
root = tree.getroot()

for req in root.findall('Requirement'):
  if (req.get('type')=='Low Level'):
    # We now have a Requirement of type Low Level
    # -------------------------------------------

    for attr in req.findall('CustomAttribute'):
      if attr.get('name') == 'Reference':
        reference = attr.get('value')
        set_name, source_file, source_description = parse_xml(source_xml,reference,log)
        log.write ('Requirement reference : ' + reference + '\nset_name : ' + set_name + '\nsource description : ' + source_description + ' \n\n')
        
        # Add a new map element
        map = ET.Element('Map set="' + set_name + '" source_file="' + source_file + '" procedure_ds="'+ source_description + '"')
        req.append (map)
    
    # Remove all unnecessary elements
    # -------------------------------
    for tag in req.findall('Tag'):
      req.remove(tag)

    for art in req.findall('Artifact'):
      req.remove(art)

    for ass in req.findall('Asset'):
      req.remove(ass)

      
# Remove everything except the Low Level Requirements
# ---------------------------------------------------
for req in root.findall('Requirement'):
  if not (req.get('type')=='Low Level'):
    root.remove(req)

for tc in root.findall('TestCase'):
  root.remove(tc)

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
tree.write (mapping_tbmspec,encoding="UTF-8", xml_declaration=True)

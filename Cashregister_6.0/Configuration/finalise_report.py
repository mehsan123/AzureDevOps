# Substitutes all the variables with the passed parameters

import subprocess
import os
import sys

log = open('finalise_report.log','w')
log.write('args = ' + str(len(sys.argv)) + '\n')

if not len(sys.argv) == 10:
  log.write('Incorrect number of parameters\n')
  sys.exit(1)

rep       = sys.argv[1]
proj      = sys.argv[2]
date      = sys.argv[3]
duration  = sys.argv[4]
version   = sys.argv[5]
tmreport  = sys.argv[6]
ddreport  = sys.argv[7]
total     = sys.argv[8]
passed    = sys.argv[9]

log.write('rep   : ' + rep + '\n')
log.write('proj  : ' + proj + '\n')


if int(total) == 0:
  percent = 100
else:
  percent = (int(passed) * 100) / int(total)

log.write('percent = ' + str(percent) + '%\n')

lines=''
try:
  report = open(rep,'r')
  for line in report:
    line = line.replace('%PROJECT%',proj)
    line = line.replace('%TEST_DATE%',date)
    line = line.replace('%DURATION%',duration)
    line = line.replace('%TOOL_SUITE_VERSION%',version)
    line = line.replace('%TEST_MANAGER_REPORT%',tmreport)
    line = line.replace('%DYNAMIC_DATA_FLOW_REPORT%',ddreport)
    line = line.replace('%PASSED_TESTS_PERCENTAGE%',str(percent))
    line = line.replace('%TOTAL_TESTS%',total)
    line = line.replace('%PASSED_TESTS%',passed)
    lines = lines + line
except IOError:
  log.write('Missing file: ' + rep)
  sys.exit(1)
finally:
  report.close()
  
try:
  report = open(rep,'w')
  report.write(lines)
except IOError:
  log.write('Problem writing to file: ' + rep)
  sys.exit(1)
finally:
  report.close()
  log.close()

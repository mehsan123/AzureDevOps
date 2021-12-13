# Appends the test case template html to the html report
# Substitutes all the variables with the passed parameters

import sys
from xml.sax.saxutils import quoteattr

log = open('add_test_case.log','w')

if not len(sys.argv) == 6:
  log.write('Incorrect number of parameters\n')
  sys.exit(1)

rep  = sys.argv[1]
tc   = sys.argv[2]
id   = sys.argv[3]
name = sys.argv[4]
desc = sys.argv[5]

desc = quoteattr(desc)

log.write('rep  : ' + rep + '\n')
log.write('name : ' + name + '\n')

try:
  report = open(rep,'a')
  try:
    with open(tc,"r") as testcase:
      for line in testcase:
        line = line.replace('%TEST_ID%',id)
        line = line.replace('%TEST_NAME%',name)
        line = line.replace('%TEST_DESCRIPTION%',desc)
        log.write(line)
        report.write(line)
  except IOError:
    log.write('Missing file: ' + tc)
    sys.exit(1)

except IOError:
  log.write('Missing file: ' + rep)
  sys.exit(1)
finally:
  report.close()
  log.close()

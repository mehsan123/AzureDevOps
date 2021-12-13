# Appends the tail template html to the html report
# Substitutes all the variables with the passed parameters

import sys
log = open('add_tail.log','w')

if not len(sys.argv) == 4:
  log.write('Incorrect number of parameters\n')
  sys.exit(1)

rep  = sys.argv[1]
tc   = sys.argv[2]
year = sys.argv[3]

log.write('rep : ' + rep + '\n')
log.write('tc  : ' + tc + '\n')

try:
  report = open(rep,'a')
  try:
    with open(tc,"r") as testcase:
      for line in testcase:
        line = line.replace('%COPYRIGHT_YEAR%',year)
        log.write(line)
        report.write(line)
  except IOError:
    print('Missing file: ' + tc)
    sys.exit(1)
  finally:
    testcase.close()
except IOError:
  print('Missing file: ' + rep)
  sys.exit(1)
finally:
  report.close()
  log.close()

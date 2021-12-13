# Compare two files to see if identical
# syntax file_compare.py file1 file2
# returns 0 if files are equal

import sys

if not len(sys.argv) == 3:
  print('Must pass two files to be compared')
  sys.exit(1)

try:
  f1 = open(sys.argv[1],"r")
except IOError:
  print('Missing file: ' + sys.argv[1])
  sys.exit(1)

try:
  f2 = open(sys.argv[2],"r")
except IOError:
  print('Missing file: ' + sys.argv[2])
  sys.exit(1)

line1 = f1.readline()
line2 = f2.readline()

status=0
while line1 and line2:
  if line1 != line2:
    # Files are different
    status=1
    break
  line1 = f1.readline()
  line2 = f2.readline()

f1.close()
f2.close()

sys.exit(status)
 
import os
import sys

address = '16o94qS8ZFEoKUTrZfLd2sLhvDqLKi4hDe'
amount = '.1000'

cmd = "electrum payto" + " " + address + " " + amount
x = os.popen(cmd)
output = x.read()
print output

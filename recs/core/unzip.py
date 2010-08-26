'''
Created on Jul 16, 2010

@author: aloneroad
'''
from zlib import decompress
from sys import argv

filename = argv[1]
output_file = argv[2]

print "Processing..."
data = decompress(open(filename).read())
open(output_file, "w").write(data)
print "Finish."
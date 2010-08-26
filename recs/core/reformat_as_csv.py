#! coding: utf-8
##  Convert from txt to csv google data store format
# 

from base64 import encodestring

def to_csv(input_file, output_file, type):
  """ record template: items,actor,key
  """
  print "Opening input file..."
  lines = open(input_file).read().split("\n")
  output = open(output_file, "w")
  output.write("items,key\n")
  
  print "Processing..."
  key_name_template = type + "/%s" 
  for line in lines:
    try:
      actor, items = line.split("\t")
    except ValueError:  # last line
      continue
    actor = actor[1:-1]   # remove "'" at start and end of nickname
    key = key_name_template % actor
    items = encodestring(items.strip()).replace("\n", "")
    record = "%s,%s\n" % (items, key)
    output.write(record)
  output.close()
  print "Finished"
  
if __name__ == "__main__":
  from sys import argv
  type = argv[1]
  input = argv[2]
  output = argv[3]
  to_csv(input, output, type)
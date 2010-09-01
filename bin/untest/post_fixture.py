#!/bin/env python
import urllib

def main(url, fixture):

  f = open(fixture)
  params = {"format": "json",
            "fixture": f.read()}
  f.close()

  data = urllib.urlencode(params)
  rv = urllib.urlopen(url, data)

  print rv.read()

if __name__ == "__main__":
  import sys
  url = sys.argv[1]
  fixture = sys.argv[2]
  main(url, fixture)

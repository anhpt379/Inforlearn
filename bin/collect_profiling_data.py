#!/usr/local/bin/python

import optparse
import urllib2

parser = optparse.OptionParser()
parser.add_option('--db', action='store_const', const='db',
                  dest='profile_type',
                  help='profile the db calls')
parser.add_option('-o', '--out', action='store',
                  dest='output_file',
                  help='directory to put profiling data')
parser.add_option('-d', '--data', action='store', dest='data',
                  help='post data to include in the request')
parser.set_defaults(profile_type='db',
                    )


def fetch_profile(url, profile_type='db', data=None):
  headers = {'X-Profile': profile_type}

  req = urllib2.Request(url, data, headers)
  resp = urllib2.urlopen(req)

  return resp.read()

def main(options, args):
  if not args:
    raise Exception('need to specify a url')

  url = args[0]
  profile_type = getattr(options, 'profile_type', 'db')
  data = getattr(options, 'data', None)
  output_file = getattr(options, 'output_file', None)

  rv = fetch_profile(url, profile_type, data)

  if output_file:
    f = open(output_file, 'w')
    f.write(rv)
    f.close()
  else:
    print rv






if __name__ == '__main__':
  (options, args) = parser.parse_args()

  main(options, args)

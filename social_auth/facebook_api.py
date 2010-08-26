from social_auth.facebook import Facebook
from django.http import HttpResponse

def check_connect_session(self, request):
  """
  For use in a facebook Connect application running in Google App Engine
  Takes a Google App Engine Request
  http://code.google.com/appengine/docs/webapp/requestclass.html
  and determines if the current user has a valid session
  """

  # our session is stored in cookies - validate them
  params = self.validate_cookie(request.cookies)
  
  if not params:
      return False

  if params.get('expires'):
      self.session_key_expires = int(params['expires'])

  if 'session_key' in params and 'user' in params:
      self.session_key = params['session_key']
      self.uid = params['user']
  else:
      return False

  return True


def validate_cookie(self, cookies):
  """
  Validates parameters passed to a Facebook connect app through cookies

  """
  # check for the hashed secret
  if self.api_key not in cookies:
      return None

  # create a dict of the elements that start with the api_key
  # the resultant dict removes the self.api_key from the beginning
  args = dict([(key[len(self.api_key) + 1:], value) 
                  for key, value in cookies.items() 
                  if key.startswith(self.api_key + "_")])

  # check the hashes match before returning them
  if self._hash_args(args) == cookies[self.api_key]:
      return args

  return None


def get(self):
  API_KEY = ''
  SECRET = ''

  facebookapi = Facebook(API_KEY, SECRET);

  if not facebookapi.check_connect_session(self.request):
      # return login form with Facebook API Key
      return

  user = facebookapi.users.getInfo( 
      [facebookapi.uid], 
      ['uid', 'name', 'birthday', 'relationship_status'])[0]

  template_values = {
      'name': user['name'],
      'birthday': user['birthday'],
      'relationship_status': user['relationship_status'],
      'uid': user['uid'],
      'apikey': API_KEY
    }

  return HttpResponse(str(template_values))
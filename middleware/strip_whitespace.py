class WhitespaceMiddleware(object):
  """Class to strip leading and trailing whitespace from all form fields.

  Note that files are not in POST but in FILES, so this will not touch binary
  data.

  If it turns out that this breaks something we can add an url white/blacklist.
  """
  def _strip_from_values(self, qdict):
    copy = None
    for k, v in qdict.items():
      stripped = v.strip()
      if not v == stripped:
        if not copy:
          copy = qdict.copy()
        copy[k] = stripped
    if copy:
      return copy
    return qdict

  def process_request(self, request):
    request.GET = self._strip_from_values(request.GET)
    request.POST = self._strip_from_values(request.POST)

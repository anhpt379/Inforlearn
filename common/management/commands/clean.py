from optparse import make_option
from django.core.management.base import BaseCommand
import build

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
      make_option(
          '--skip-zip', action='store_true', dest='skip_zip', default=False,
          help='Do not clean up zip files'
          ),
      )

  help = 'Cleans up the results of a build'
  args = ''

  requires_model_validation = False

  def handle(self, *test_labels, **options):
    skip_zip = options.get('skip_zip', False)
    build.clean(skip_zip=skip_zip)

from optparse import make_option
from django.core.management.base import BaseCommand
import build

class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
      make_option('--write-to-file',
                  action='store_true',
                  dest='write_to_file',
                  default=False,
                  help='Write output directly to a file'
          ),
      )

  help = 'Config helper for installation'
  args = ''

  requires_model_validation = False

  def handle(self, *test_labels, **options):
    write_to_file = options.get('write_to_file', False)
    build.config(write_to_file=write_to_file)

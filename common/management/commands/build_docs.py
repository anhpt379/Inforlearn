from django.core.management.base import BaseCommand
import build

class Command(BaseCommand):
  option_list = BaseCommand.option_list

  help = 'Builds the documentation'
  args = ''

  requires_model_validation = False

  def handle(self, *test_labels, **options):
    build.generate_api_docs()
    build.build_docs()

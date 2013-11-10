from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from survivor.models import Pick

class Command(BaseCommand):
    args = '<week>'
    help = 'Command to close editing for picks for a certain round'

    def handle(self, *args, **options):
        for pick in Pick.objects.filter(week=args[0]):
            pick.editable = False
            pick.save()

    
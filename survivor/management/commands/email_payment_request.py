from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from survivor.models import Player
from django.core.mail import send_mail
     
class Command(BaseCommand):

    help = 'Command to send an email to all unpaid players, asking for payment'

    def handle(self, *args, **options):

        for player in Player.objects.filter(paid=False):
            
            email_body = 'Hey ' + player.user.first_name + ',   \
it looks like you haven\'t yet paid for the upcoming EPL Survivor game. \
Please deposit ' + str(player.group.entry_fee) + ' pounds into account:\n\n\
Sort Code: 30-99-02\n\
Account: 14168168\n\n\
Thanks, and good luck!'
            
            send_mail(
                'EPL Survivor Payment Pending',
                email_body,
                'mailer@eplsurvivor.com',
                [player.user.email],
                #['ben@benedwards.co.nz'],
                fail_silently=True
            )
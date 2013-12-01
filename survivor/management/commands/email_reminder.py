from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from survivor.models import Player, Pick
from django.core.mail import send_mail
from django.conf import settings
import json
import requests
     
class Command(BaseCommand):
    args = '<week>'
    help = 'Command to send an email reminder for the upcoming week.'

    def handle(self, *args, **options):
        # add player__user=1 to the filter to only send to me
        for pick in Pick.objects.filter(week=args[0], player__alive=True):
            
            if pick.team:
                email_body = 'Hey ' + pick.player.user.first_name + ', you have picked ' + str(pick.team) + ' for this week\'s EPL Survivor, week #' + str(pick.week) + '. You have until the first game kick-off time if you wish to change this pick. Visit http://www.eplsurvivor.com/edit_pick/' + str(pick.id) + ' to change.\n\nGood Luck!'
            else:
                email_body = 'Hey ' + pick.player.user.first_name + ', you have not yet made a pick for this week\'s EPL Survivor, week #' + str(pick.week) + '. You have until the first game kick-off time to make your pick. Visit http://www.eplsurvivor.com/edit_pick/' + str(pick.id) + ' to enter your pick.\n\nGood Luck!'
            
            send_mail(
                'EPL Survivor Reminder',
                email_body,
                'mailer@eplsurvivor.com',
                [pick.player.user.email],
                #['ben@benedwards.co.nz'],
                fail_silently=True
            )
            
        chatter_text = 'Reminder: Week ' + args[0] + ' picks are closing tomorrow. You have until tomorrow to get your picks in. Don\'t forget!\n\nPosted via Chatter REST API - http://eplsurvivor.com'
        chatter_post = {"body": { "messageSegments" : [{ "type" : "text", "text": chatter_text}]}}
        r = requests.post(settings.SALESFORCE_POST_GROUP_URL, data=json.dumps(chatter_post), headers=settings.SALESFORCE_HEADERS)
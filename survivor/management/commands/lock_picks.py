from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from survivor.models import Pick, Group
from django.conf import settings
import json
import requests

class Command(BaseCommand):
    args = '<week>'
    help = 'Command to close editing for picks for a certain round'

    def handle(self, *args, **options):
        
        chatter_text = 'Week ' + args[0] + ': 1st match started, picks are now locked!\n\nPicks are as follows:\n'
        for pick in Pick.objects.filter(week=args[0]).order_by('player__user__first_name'):
            pick.editable = False
            pick.save()
            
            if pick.player.group.name == 'Tquila' and pick.player.alive:
                chatter_text += pick.player.user.first_name + ' ' + pick.player.user.last_name + ': ' + pick.team.name + '\n'

        chatter_text += '\nGood luck everyone!\n\nPosted via Chatter REST API - http://eplsurvivor.com'
        chatter_post = {"body": { "messageSegments" : [{ "type" : "text", "text": chatter_text}]}}
        r = requests.post(settings.SALESFORCE_POST_GROUP_URL, data=json.dumps(chatter_post), headers=settings.SALESFORCE_HEADERS)
            
        for group in Group.objects.filter(start_round=args[0],locked=False):
            group.locked = True
            group.save()
        
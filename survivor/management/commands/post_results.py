from django.core.management.base import NoArgsCommand, CommandError, BaseCommand
from survivor.models import Pick, Group
from django.conf import settings
import json
import requests

class Command(BaseCommand):
    args = '<week>'
    help = 'Command to close editing for picks for a certain round'

    def handle(self, *args, **options):
        
        chatter_text = 'Week ' + args[0] + ': The results are in!\n\n'
        
        dead_players = ''
        alive_players = ''
        players_remaining = 0
        for pick in Pick.objects.filter(week=args[0]).order_by('player__user__first_name'):
            if pick.player.group.name == 'Tquila' and pick.player.died_at_round == int(args[0]):
                dead_players += pick.player.user.first_name + ' ' + pick.player.user.last_name + '\n'
            
            if pick.player.group.name == 'Tquila' and pick.player.alive:
                alive_players += pick.player.user.first_name + ' ' + pick.player.user.last_name + '\n'
                players_remaining += 1
            
        chatter_text += 'This weeks casualties:\n' + dead_players
        chatter_text += '\nThe rest of you have made it through to next round (well done):\n' + alive_players
        chatter_text += '\n' + str(players_remaining) + ' players remain'
        chatter_text += '\n\nPosted via Chatter REST API - http://eplsurvivor.com'
        
        chatter_post = {"body": { "messageSegments" : [{ "type" : "text", "text": chatter_text}]}}
        r = requests.post(settings.SALESFORCE_POST_GROUP_URL, data=json.dumps(chatter_post), headers=settings.SALESFORCE_HEADERS)
        
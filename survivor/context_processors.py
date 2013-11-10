from survivor.models import Player, Group
from django.db.models import Count

def my_groups(request):
	my_active_groups = []
	for group in Group.objects.filter(active=True).order_by('name'):
		for player in group.player_set.all():
			if player.user == request.user:
				my_active_groups.append(group)
	return {'my_active_groups': my_active_groups}

from django.shortcuts import render_to_response, get_object_or_404
from survivor.models import Player, Group, Comment, Pick, Team, Match
from survivor.forms import CreateGroupForm, JoinGroupForm, CommentForm, LoginForm, RegistrationForm, PickForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms.models import modelformset_factory
import datetime

def index(request):

	if request.method == 'POST' and 'login' in request.POST:

		login_form = LoginForm(request.POST)

		if login_form.is_valid():
			
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']

			user = authenticate(username=username, password=password)
			if user:
				login(request,user)
				return HttpResponseRedirect('/groups/')

	else:
		login_form = LoginForm()

	if request.method == 'POST' and 'register' in request.POST:

		registration_form = RegistrationForm(request.POST)

		if registration_form.is_valid():

			email = registration_form.cleaned_data['email']
			password = registration_form.cleaned_data['password']
			first_name = registration_form.cleaned_data['first_name']
			last_name = registration_form.cleaned_data['last_name']

			user = User.objects.create_user(email, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()

			user = authenticate(username=email, password=password)
			login(request, user)

			return HttpResponseRedirect('/groups/')

	else:
		registration_form = RegistrationForm()

	if request.user.is_authenticated():	
		return HttpResponseRedirect('/groups/')
	else:
		return render_to_response('index.html', RequestContext(request,{'login_form': login_form, 'registration_form' :registration_form}))


def groups(request):

	available_groups = []

	for group in Group.objects.filter(active=True, locked=False).order_by('name'):
		
		user_in_group = False
		
		for player in group.player_set.all():
			if player.user == request.user:
				user_in_group = True
				break
		
		if not user_in_group:
			available_groups.append(group)

	if request.method == 'POST' and 'create' in request.POST:
		create_group_form = CreateGroupForm(request.POST)
		if create_group_form.is_valid():

			# create new group
			new_group = Group()
			new_group.name = create_group_form.cleaned_data['name']
			new_group.password = create_group_form.cleaned_data['password']
			new_group.start_round = create_group_form.cleaned_data['start_round']
			new_group.entry_fee = create_group_form.cleaned_data['entry_fee']
			new_group.active = True
			new_group.save()

			new_player = Player()
			new_player.group = new_group
			new_player.user = request.user
			new_player.alive = True
			new_player.admin = True
			new_player.save()

			for i in range(new_group.start_round, 39):
				new_pick = Pick(player=new_player, week=i)
				new_pick.save()

			return HttpResponseRedirect('/groups/' + str(new_group.id))
	else:
		create_group_form = CreateGroupForm()

	if request.method == 'POST' and 'join' in request.POST:

		join_group_form = JoinGroupForm(request.POST)

		if join_group_form.is_valid():

			group = Group.objects.get(name=join_group_form.cleaned_data['name'])

			new_player = Player()
			new_player.group = group
			new_player.user = request.user
			new_player.alive = True
			new_player.admin = True
			new_player.save()

			for i in range(group.start_round, 39):
				new_pick = Pick(player=new_player, week=i)
				new_pick.save()

			return HttpResponseRedirect('/groups/' + str(group.id))	
		
	else:
		join_group_form = JoinGroupForm()

	if request.user.is_authenticated():
		return render_to_response('groups.html', RequestContext(request, {'available_groups': available_groups, 'create_group_form': create_group_form, 'join_group_form': join_group_form}))
	else:
		return HttpResponseRedirect('/')

def group(request, group_id):

	group = get_object_or_404(Group, pk=group_id)

	# Make sure the logged in user is a player in the request group
	player_exists = False
	for player in group.player_set.all():
		if player.user == request.user:
			player_exists = True

	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment_obj = Comment(user=request.user, created_date=datetime.datetime.now(), comment=comment_form.cleaned_data['comment'], group=group)
			comment_obj.save()

			return HttpResponseRedirect('/groups/' + group_id)
	else:
		comment_form = CommentForm()

	round_numbers = []
	for i in range(group.start_round, 39):
		 round_numbers.append(i)

	table_width = 280 + (len(round_numbers) * 90)

	if request.user.is_authenticated() and player_exists:
		return render_to_response('group_detail.html', RequestContext(request, {'table_width': table_width, 'group': group, 'round_numbers': round_numbers}))
	else:
		return HttpResponseRedirect('/')

def edit_pick(request, pick_id):

	pick = get_object_or_404(Pick, pk=pick_id)
	matches = Match.objects.filter(week=pick.week)

	if request.method == 'POST' and 'save' in request.POST:
		pick_form = PickForm(request.POST, instance=pick)
		if pick_form.is_valid():
			pick.team = pick_form.cleaned_data['team']
			pick.save()

			return HttpResponseRedirect('/groups/' + str(pick.player.group.id))
	else:
		pick_form = PickForm(instance=pick)

	if request.method == 'POST' and 'cancel' in request.POST:
		return HttpResponseRedirect('/groups/' + str(pick.player.group.id))

	if not pick.editable or pick.player.user != request.user or not request.user.is_authenticated():
		return HttpResponseRedirect('/groups/' + str(pick.player.group.id))

	return render_to_response('edit_pick.html', RequestContext(request, {'pick': pick, 'matches': matches, 'pick_form': pick_form}))

def results(request, week_number):

	if not request.user.is_staff:
		return HttpResponseRedirect('/')

	results = Match.objects.filter(week=week_number)
	ResultsFormSet = modelformset_factory(Match, extra=0, fields=('team_one','team_two','winner'))

	if request.method == 'POST':

		results_formset = ResultsFormSet(request.POST, queryset=results)

		if results_formset.is_valid():
			
			results_formset.save()

			picks = Pick.objects.filter(week=week_number)

			for pick in Pick.objects.filter(week=week_number):
				for match in Match.objects.filter(week=week_number):
					if pick.player.alive and (pick.team == match.team_one or pick.team == match.team_two):
						if (pick.team == match.team_one and match.winner == 'Team One') or match.winner == 'Draw':
							pick.result = 'Correct'

						if (pick.team == match.team_two and match.winner == 'Team Two') or match.winner == 'Draw':
							pick.result = 'Correct'

						if (pick.team == match.team_one and match.winner == 'Team Two') or (pick.team == match.team_two and match.winner == 'Team One'):
							pick.result = 'Incorrect'
							player = Player.objects.get(id=pick.player.id)
							player.alive = False
							player.died_at_round = week_number
							player.save()

						pick.save()

			return HttpResponseRedirect('/results/' + str(week_number))

	else:
		results_formset = ResultsFormSet(queryset=results)

	return render_to_response('results.html', RequestContext(request, {'week_number': week_number, 'results_formset': results_formset}))

def dologout(request):
	logout(request)
	return HttpResponseRedirect('/')

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from survivor.models import Group, Comment, Pick, Player, Match
from django.contrib.auth import authenticate, login, logout

class CreateGroupForm(forms.Form):
	name = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)
	start_round = forms.IntegerField()
	entry_fee = forms.IntegerField()

	def clean(self):
		cleaned_data = self.cleaned_data
		group_name = self.cleaned_data['name']
		all_groups = Group.objects.filter(active=True)
		for group in all_groups:
			if group_name:
				if group_name == group.name:
					raise forms.ValidationError("A group with this name already exists.")
		return cleaned_data


class JoinGroupForm(forms.Form):
	name = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100)

	def clean(self):
		cleaned_data = self.cleaned_data
		group = Group.objects.get(name=self.cleaned_data['name'])
		if group.password != self.cleaned_data['password']:
			raise forms.ValidationError("The password you entered is incorrect.")
		return cleaned_data

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1000)

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()

	def clean(self):
		cleaned_data = self.cleaned_data
		user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
		if not user:
			raise forms.ValidationError("The username or password is incorrect.")
		return cleaned_data

class RegistrationForm(forms.Form):
	email = forms.CharField()
	password = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	def clean(self):
		cleaned_data = self.cleaned_data
		users = User.objects.filter(username=self.cleaned_data['email'])
		if users:
			raise forms.ValidationError("The email you have entered already exists.")
		return cleaned_data

class PickForm(ModelForm):
    class Meta:
        model = Pick
        fields = ['team','player']

    def clean(self):
        cleaned_data = self.cleaned_data
        picked_team = self.cleaned_data['team']
        player = Player.objects.get(pk=self.cleaned_data['player'].id)
        all_picks = Pick.objects.filter(player = player)
        for pick in all_picks:
            if picked_team:
                if picked_team == pick.team:
                    raise forms.ValidationError("You have already picked this team for another round in the competition. Please choose another team.")

        return cleaned_data

class ResultForm(ModelForm):
    class Meta:
        model = Match
        fields = ['team_one', 'team_two', 'winner']

    
from django.contrib import admin
from survivor.models import Team, Group, Player, Comment, Pick, Match

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name','logo_image')
    ordering = ['name']

class PlayerInline(admin.TabularInline):
	fields = ['admin', 'paid', 'user', 'alive','died_at_round']
	readonly_fields = ['user']
	model = Player
	extra = 0

class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0

class PickInline(admin.TabularInline):
    model = Pick
    extra = 0

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','locked','active')
    inlines = [PlayerInline,CommentInline]

class PickAdmin(admin.ModelAdmin):
    list_display = ('player','player_alive','group_name','week','team','result')
    list_editable = ['result']
    list_filter = ('editable','player__alive','player__group','week')
    ordering = ['week']

class MatchAdmin(admin.ModelAdmin):
    list_display = ('week','kickoff','team_one','team_two','winner')
    list_editable = ['winner']
    list_filter = ('week',)
    ordering = ['kickoff']

admin.site.register(Team, TeamAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(Match, MatchAdmin)
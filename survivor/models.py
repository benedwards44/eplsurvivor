from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import datetime

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='teamlogos', blank=True)
    
    def logo_image(self):
        return '<img src="/media/%s" width="35" height="35" />' % (self.logo)
    logo_image.allow_tags = True
    
    def __str__(self):
        return '%s' % (self.name)

class Match(models.Model):

    RESULT_OPTIONS = (
        ('Team One', 'Team One'),
        ('Team Two', 'Team Two'),
        ('Draw', 'Draw'),
    )

    kickoff = models.DateTimeField(null=True,blank=True)
    week = models.PositiveSmallIntegerField()
    team_one = models.ForeignKey(Team, related_name='team_one')
    team_two = models.ForeignKey(Team, related_name='team_two')
    winner = models.CharField(max_length=50, choices=RESULT_OPTIONS, blank=True)

class Group(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    locked = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    start_round = models.PositiveSmallIntegerField()
    entry_fee = models.PositiveSmallIntegerField()

    def active_players(self):
        return self.player_set.filter(alive=True).count()

    def prize_pool(self):
        return self.entry_fee * self.player_set.all().count()

class Player(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    paid = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)
    died_at_round = models.PositiveSmallIntegerField(null=True,blank=True)
    admin = models.BooleanField(default=False)
    
    def sorted_picks(self):
        return self.pick_set.order_by('week')
    
    def player_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

class Pick(models.Model):
    
    RESULT_OPTIONS = (
        ('Correct', 'Correct'),
        ('Incorrect', 'Incorrect'),
    )
    
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, blank=True, null=True)
    week = models.PositiveSmallIntegerField()
    editable = models.BooleanField(default=True)
    result = models.CharField(max_length=50, choices=RESULT_OPTIONS, blank=True)
    
    def player_alive(self):
      return self.player.alive

    def group_name(self):
        return self.player.group.name
    
    def __str__(self):
        return '%s %s' % (self.player, self.week)

class Comment(models.Model):
    group = models.ForeignKey(Group)
    parent = models.ForeignKey('self',blank=True, null=True,related_name='children')
    user = models.ForeignKey(User,blank=True, null=True)
    comment = models.TextField()
    created_date = models.DateTimeField(null=True,blank=True)
    
    def save_model(self, request, obj, form, change):
        obj.created_date = datetime.datetime.now()
        obj.user = request.user
        obj.save()
        
    def full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name) 
        
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

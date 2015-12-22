from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Hunt(models.Model):
    hunt_name = models.CharField(max_length=200)
    hunt_number = models.IntegerField(unique=True)
    team_size = models.IntegerField()
    #Very bad things could happen if end date is before start date
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    @property
    def is_locked(self):
        return timezone.now() < self.start_date

    @property
    def is_open(self):
        return timezone.now() > self.start_date and timezone.now() < self.end_date

    @property
    def is_public(self):
        return timezone.now() > self.end_date

    def __unicode__(self):
        return self.hunt_name

class Puzzle(models.Model):
    puzzle_number = models.IntegerField()
    puzzle_name = models.CharField(max_length=200)
    puzzle_id = models.CharField(max_length=8, unique=True) #hex only please
    answer = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    num_required_to_unlock = models.IntegerField(default=1)
    unlocks = models.ManyToManyField("self", blank=True, symmetrical=False)
    hunt = models.ForeignKey(Hunt)
    #Reward upon completion? 
    
    def __unicode__(self):
        return str(self.puzzle_number) + "-" + str(self.puzzle_id) + " " + self.puzzle_name
    
class Team(models.Model):
    team_name = models.CharField(max_length=200)
    solved = models.ManyToManyField(Puzzle, blank=True, related_name='solved_for', through="Solve")
    unlocked = models.ManyToManyField(Puzzle, blank=True, related_name='unlocked_for', through="Unlock")
    unlockables = models.ManyToManyField("Unlockable", blank=True)
    login_info = models.OneToOneField(User)
    hunt = models.ForeignKey(Hunt)
    location = models.CharField(max_length=80, blank=True)

    def __unicode__(self):
        return str(len(self.person_set.all())) + " (" + self.location + ") " + self.team_name

class Person(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    comments = models.CharField(max_length=400, blank=True)
    team = models.ForeignKey(Team, blank=True)
    year = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
    
class Submission(models.Model):
    team = models.ForeignKey(Team)
    submission_time = models.DateTimeField()
    submission_text = models.CharField(max_length=100)
    response_text = models.CharField(blank=True, max_length=400)
    puzzle = models.ForeignKey(Puzzle)
    
    def __unicode__(self):
        return self.submission_text

class Solve(models.Model):
    puzzle = models.ForeignKey(Puzzle)
    team = models.ForeignKey(Team)
    submission = models.ForeignKey(Submission, blank=True)
    
class Unlock(models.Model):
    puzzle = models.ForeignKey(Puzzle)
    team = models.ForeignKey(Team)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.team.team_name + ": " + self.puzzle.puzzle_name

class Message(models.Model):
    team = models.ForeignKey(Team)
    is_response = models.BooleanField()
    text = models.CharField(max_length=400)
    time = models.DateTimeField()

    def __unicode__(self):
        return self.team.team_name + ": " + self.text

class Unlockable(models.Model):
    TYPE_CHOICES = (
        ('IMG', 'Image'),
        ('PDF', 'PDF'),
        ('TXT', 'Text'),
        ('WEB', 'Link'),
    )
    puzzle = models.ForeignKey(Puzzle)
    content_type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='TXT')
    content = models.CharField(max_length=500)
    

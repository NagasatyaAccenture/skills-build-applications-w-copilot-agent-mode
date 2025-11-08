from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from octofit_tracker import settings

from django.db import connection

# Define models for demonstration (in real app, these would be in models.py)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user_email = models.EmailField()
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', password='pass'),
            User.objects.create_user(username='spiderman', email='spiderman@marvel.com', password='pass'),
            User.objects.create_user(username='batman', email='batman@dc.com', password='pass'),
            User.objects.create_user(username='superman', email='superman@dc.com', password='pass'),
        ]

        # Create activities
        Activity.objects.create(user_email='ironman@marvel.com', type='Run', duration=30, team='Marvel')
        Activity.objects.create(user_email='spiderman@marvel.com', type='Swim', duration=45, team='Marvel')
        Activity.objects.create(user_email='batman@dc.com', type='Cycle', duration=60, team='DC')
        Activity.objects.create(user_email='superman@dc.com', type='Yoga', duration=20, team='DC')

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=75)
        Leaderboard.objects.create(team='DC', points=80)

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity workout for heroes', difficulty='Hard')
        Workout.objects.create(name='Sidekick Stretch', description='Flexibility routine for sidekicks', difficulty='Easy')

        # Ensure unique index on email
        with connection.cursor() as cursor:
            cursor.db_conn['auth_user'].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))

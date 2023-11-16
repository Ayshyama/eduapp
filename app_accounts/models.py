from django.contrib.auth.models import AbstractUser
from django.db import models

from app_exercises.models import Exercise


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    email = models.EmailField(unique=True)
    life = models.PositiveSmallIntegerField(default=10)
    exercises_done = models.ManyToManyField(Exercise, through='UserProgress')
    day_streak = models.PositiveSmallIntegerField(default=0)


class UserExerciseConversation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    message = models.TextField()
    is_human = models.BooleanField(default=False)


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class UserStatistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveSmallIntegerField(default=0)
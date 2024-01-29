from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from app_exercises.models import Exercise


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile/%Y/%m/%d/', blank=True)
    email = models.EmailField(unique=True)
    life = models.PositiveSmallIntegerField(default=10)
    exercises_done = models.ManyToManyField(Exercise, through='UserProgress')
    day_streak = models.PositiveSmallIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)


class UserExerciseConversation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    message = models.TextField()
    is_human = models.BooleanField(default=False)


class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class UserStatistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    progress = models.PositiveSmallIntegerField(default=0)


@receiver(m2m_changed, sender=CustomUser.exercises_done.through)
def create_user_progress(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" and not reverse:
        for exercise_pk in pk_set:
            # Check if the UserProgress already exists
            if not UserProgress.objects.filter(user=instance, exercise_id=exercise_pk).exists():
                UserProgress.objects.create(user=instance, exercise_id=exercise_pk)


'''
Signal Receiver:
- The @receiver decorator is used to register the function create_user_progress as 
a signal receiver for the m2m_changed signal, specifically for changes to the 
exercises_done many-to-many field in the CustomUser model.
- The sender argument specifies the model class that sends the signal, which is the
intermediary model that Django automatically creates to manage the many-to-many
relationship between CustomUser and Exercise.
- The signal is triggered whenever the exercises_done field is changed, which can
happen in a variety of ways, including when a new exercise is added to the set or
when an existing exercise is removed from the set.
- The reverse argument is set to True when the change is made on the reverse side of
the relation, which is the Exercise model in this case.
- The pk_set argument is a set of primary keys for the related objects that were added
to the many-to-many field.
- The **kwargs argument allows the function to accept arbitrary keyword arguments.
- When a CustomUser instance has exercises added to its exercises_done set, the create_user_progress function is triggered.
- If the action is post_add (which occurs after new items have been added to the many-to-many field) and the change is not 
happening on the reverse side of the relation, the function iterates over the primary key set of added exercises and 
creates a new UserProgress instance for each one, associating the exercise with the user.
'''
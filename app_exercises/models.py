from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/')


class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)


class Exercise(models.Model):
    name = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    keywords = models.ManyToManyField('Keywords')
    is_test = models.BooleanField(default=False)


class Keywords(models.Model):
    keyword = models.CharField(max_length=100)


class TestAnswer(models.Model):
    name = models.CharField(max_length=500)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)







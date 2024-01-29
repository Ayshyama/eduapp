from django.db import models
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='images/')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.module} | {self.name}'


class Exercise(models.Model):
    name = models.CharField(max_length=100, default='Exercise')
    description = models.TextField()
    code = models.TextField(blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    keywords = models.ManyToManyField('Keywords')
    is_test = models.BooleanField(default=False)

    def __str__(self):
        return self.name[:20]

    def get_absolute_url(self):
        return reverse('exercise', kwargs={'pk': self.pk})


class Keywords(models.Model):
    keyword = models.CharField(max_length=100)

    def __str__(self):
        return self.keyword


class TestAnswer(models.Model):
    name = models.CharField(max_length=500)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.name






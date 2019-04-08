from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # if user is deleted we're going to delete all his posts
    # one-to-many relation
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # after post successfully created -> redirect to certain view
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
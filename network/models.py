from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name="followers", blank=True)

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    content = models.CharField(max_length=260)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    liked_by = models.ManyToManyField(User, related_name="likes", blank=True)
    date = models.DateTimeField(default=timezone.now)

    def data(self, user):
        return { self.id : {
            "content": self.content,
            "date": self.date,
            "creator": self.creator.username,
            "likes": self.liked_by.count(),
        }}

    def __str__(self):
        return f'{self.creator}, posted "{self.content}"'

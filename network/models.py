from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', related_name="followers")

    def follow(self, followed):
        self.following.add(followed)
        self.save()

    def unfollow(self, followed):
        self.following.remove(followed)
        self.save()

    def serialize(self):
        return {
            "username": self.username
        }

class Post(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usrPosts", default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def post(self, message, user):
        self.message = message
        self.user = user
        self.save()

    def __str__(self):
        return self.message

    def serialize(self):
        return {
            "message": self.message,
            "user": self.user.serialize(),
            "created_at": self.created_at.strftime("%b %-d %Y, %-I:%M %p")
        }

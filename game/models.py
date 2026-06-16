from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Match(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)

    user_move = models.CharField(max_length=20)
    ai_move = models.CharField(max_length=20)

    result = models.CharField(max_length=10)

    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username} - {self.result}"


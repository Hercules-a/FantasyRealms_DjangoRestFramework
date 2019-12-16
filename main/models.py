from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save


# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Game(models.Model):
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    authorization = models.ManyToManyField(Token, blank=True)

    def __str__(self):
        return self.login


class Deal(models.Model):
    count = models.IntegerField(default=1, unique=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='deals')

    def __str__(self):
        return '{}, Round: {}'.format(self.game.login, self.count)


class Point(models.Model):
    points = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='points')

    class Meta:
        unique_together = ('user', 'deal')

    def __str__(self):
        return '{} Round {} {}: {}'.format(self.deal.game.login, self.deal.count, self.user.username, self.points)

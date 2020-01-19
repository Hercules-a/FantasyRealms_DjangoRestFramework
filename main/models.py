from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Game(models.Model):
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    authorization = models.ManyToManyField(Token)
    admin = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='admin')

    def __str__(self):
        return self.login

    def scoreboard(self):
        board = {}
        for token in self.authorization.all():
            user = token.user
            score = 0
            for deal in self.deals.all():
                for points in deal.points.filter(user=user):
                    score += points.points
            board.update({user.username: score})
        return sorted(board.items(), key=lambda kv: (kv[-1], kv[0]), reverse=True)

    def users(self):
        users_list = []
        for token in self.authorization.all():
            users_list.append(token.user.username)
        return users_list


class Deal(models.Model):
    count = models.IntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='deals')

    class Meta:
        unique_together = ('count', 'game')

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





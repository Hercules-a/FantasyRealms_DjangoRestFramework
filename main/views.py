from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import GameSimpleSerializer, GameSerializer, UserSerializer, DealSerializer
from .models import Game, Deal, Point
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.http.response import HttpResponseNotAllowed
from django.db.utils import IntegrityError


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        game = Game.objects.create(login=request.data['login'],
                                   password=request.data['password'])
        token = Token.objects.get(key=request.data['token'])
        game.authorization.add(token)
        serializer = GameSerializer(game, many=False)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = Game.objects.all()
        serializer = GameSimpleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = GameSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def join(self, request, *args, **kwargs):
        game = Game.objects.get(login=request.data['login'])
        if game.password == request.data['password']:
            token = Token.objects.get(key=request.data['token'])
            game.authorization.add(token)
            token.user.extend_user.active_game = game
            token.user.extend_user.save()
            serializer = GameSerializer(game, many=False)
            return Response(serializer.data)
        else:
            return HttpResponseNotAllowed('Wrong password!')

    @action(detail=True, methods=['put'])
    def new_deal(self, *args, **kwargs):
        instance = self.get_object()
        count = instance.deals.all().order_by('-count')[0].count + 1
        Deal.objects.create(count=count, game=instance)
        serializer = GameSerializer(instance, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def add_points(self, request, *args, **kwargs):
        instance = self.get_object()
        deal = instance.deals.all().order_by('-count')[0]
        user = Token.objects.get(key=request.data['token']).user
        points = request.data['points']
        try:
            Point.objects.create(points=points, user=user, deal=deal)
        except IntegrityError:
            edit = Point.objects.get(user=user, deal=deal)
            edit.points = points
            edit.save()
        serializer = GameSerializer(instance, many=False)
        return Response(serializer.data)

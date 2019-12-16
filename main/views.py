from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import GameSimpleSerializer, GameSerializer, UserSerializer
from .models import Game
from rest_framework.authtoken.models import Token


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GameSerializer(instance)
        return Response(serializer.data)


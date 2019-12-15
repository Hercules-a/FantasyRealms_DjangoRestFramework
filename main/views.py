from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import GameSimpleSerializer, GameSerializer
from .models import Game


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        film = Game.objects.create(login=request.data['login'], password=request.data['password'])
        serializer = GameSerializer(film, many=False)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        serializer = GameSimpleSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GameSerializer(instance)
        return Response(serializer.data)


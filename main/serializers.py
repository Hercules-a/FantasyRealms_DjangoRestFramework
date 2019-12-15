from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Game, Deal, Point


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class PointSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Point
        fields = ['user', 'points']


class DealSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)

    class Meta:
        model = Deal
        fields = ['count', 'points']


class GameSerializer(serializers.ModelSerializer):
    deals = DealSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ['login', 'password', 'deals']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}


class GameSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['login', 'id']
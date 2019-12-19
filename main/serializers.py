from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Game, Deal, Point, ExtendUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        ExtendUser.objects.create(user=user)
        return user


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
        fields = ['login', 'password', 'scoreboard', 'deals', 'authorization']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}


class GameSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['login', 'id']

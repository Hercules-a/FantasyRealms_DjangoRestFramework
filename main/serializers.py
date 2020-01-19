from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Game, Deal, Point


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class PointSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Point
        fields = ['user', 'points']


class DealSerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()

    class Meta:
        model = Deal
        fields = ['count', 'points']

    def get_points(self, instance):
        points = instance.points.all().order_by('-points')
        return PointSerializer(points, many=True).data


class GameSerializer(serializers.ModelSerializer):
    deals = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ['id', 'login', 'password', 'scoreboard', 'deals', 'users']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def get_deals(self, instance):
        deals = instance.deals.all().order_by('-count')
        return DealSerializer(deals, many=True).data

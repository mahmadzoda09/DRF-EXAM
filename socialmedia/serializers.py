from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    posts_count = serializers.IntegerField(read_only=True, default=0)
    likes_count = serializers.IntegerField(read_only=True, default=0)
    favorites_count = serializers.IntegerField(read_only=True, default=0)
 
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "age","full_name", "posts_count", "likes_count", "favorites_count"]
        extra_kwargs = {"first_name": {"write_only": True},"last_name": {"write_only": True}}

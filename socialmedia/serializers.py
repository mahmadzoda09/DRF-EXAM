from rest_framework import serializers
from django.db.models import Sum

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
    


class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    profile = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
 
    class Meta:
        model = User
        fields = ["id", "username", "full_name", "age", "profile", "statistics"]
 
    def get_profile(self, obj):
        p = getattr(obj, "profile", None)
        return {"bio": p.bio, "city": p.city} if p else None
 
    def get_statistics(self, obj):
        return {
            "posts_count": obj.posts.count(),
            "total_views": obj.posts.aggregate(s=Sum("views"))["s"] or 0,
            "likes_received": Like.objects.filter(post__user=obj).count(),
            "favorites_received": Favorite.objects.filter(post__user=obj).count(),
        }
 
 
class MostActiveSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField()
 
    class Meta:
        model = User
        fields = ["id", "username", "posts_count"]

def short(u):
    return {"id": u.id, "username": u.username, "full_name": u.full_name}
 

class ProfileSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True, default=0)
 
    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "city", "birth_date", "avatar", "posts_count"]
 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = short(instance.user)
        return data

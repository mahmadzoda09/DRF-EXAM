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

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True, default=0)
    favorites_count = serializers.IntegerField(read_only=True, default=0)
    is_popular = serializers.SerializerMethodField()
 
    class Meta:
        model = Post
        fields = ["id", "user", "title", "content", "author", "views",
                  "likes_count", "favorites_count", "is_popular", "created_at"]
 
    def get_author(self, obj):
        return short(obj.user)
 
    def get_is_popular(self, obj):
        return getattr(obj, "likes_count", 0) >= 10
 
 
class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField()
    favorites_count = serializers.IntegerField()
    liked_by = serializers.SerializerMethodField()
    favorited_by = serializers.SerializerMethodField()
    is_popular = serializers.SerializerMethodField()
    is_viral = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
 
    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "views", "likes_count",
                  "favorites_count", "liked_by", "favorited_by",
                  "is_popular", "is_viral", "status"]

    def get_author(self, obj):
        if obj.user:
            return {
                "id": obj.user.id,
                "username": obj.user.username
            }
        else:
            return None


    def get_liked_by(self, obj):
        liked_by = []

        for l in obj.likes.select_related("user"):
            liked_by.append({
                "id": l.user.id,
                "username": l.user.username
            })

        return liked_by


    def get_favorited_by(self, obj):
        favorited_by = []

        for f in obj.favorites.select_related("user"):
            favorited_by.append({
                "id": f.user.id,
                "username": f.user.username
            })

        return favorited_by
    
    def get_is_viral(self, obj):
        if obj.views >= 1000 and obj.likes_count >= 10:
            return True
        else:
            return False
    
    def get_status(self, obj):
        if obj.likes_count > 0:
            return "has_likes"
        else:
            return "no_likes"

    def get_is_popular(self, obj):
        if obj.likes_count >= 10:
            return True
        else:
            return False 


class PopularPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField()
    favorites_count = serializers.IntegerField()
    is_popular = serializers.SerializerMethodField()
 
    class Meta:
        model = Post
        fields = ["id", "title", "likes_count", "favorites_count", "is_popular"]
 
    def get_is_popular(self, obj):
            if obj.likes_count >= 10:
                return True
            else:
                return False 
 
 
class PostShortSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField()
 
    class Meta:
        model = Post
        fields = ["id", "title", "views", "likes_count"]
 
 
class TopPostSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source="id")
    likes_count = serializers.IntegerField()
 
    class Meta:
        model = Post
        fields = ["post_id", "title", "likes_count"]
 
 
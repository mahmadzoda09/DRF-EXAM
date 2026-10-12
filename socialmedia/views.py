from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count , Max , Min , Avg
from .models import *
from .serializers import *

def create_object(serializer_class, request):
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)

def update_object(serializer_class, obj, request):
    serializer = serializer_class(obj, data=request.data, partial=(request.method == "PATCH"))
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["GET", "POST"])                                    
def user_list(request):
    if request.method == "GET":
        users = User.objects.annotate(
            posts_count=Count("posts", distinct=True),
            likes_count=Count("likes", distinct=True),
            favorites_count=Count("favorites", distinct=True),
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    return create_object(UserSerializer, request)


@api_view(["GET", "PUT", "PATCH", "DELETE"])                   
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == "GET":
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    if request.method == "DELETE":
        user.delete()
        return Response(status=204)
    return update_object(UserSerializer, user, request)  


@api_view(["GET"])                                              
def most_active_users(request):
    users = User.objects.annotate(posts_count=Count("posts")).order_by("-posts_count")[:10]
    serializer = MostActiveSerializer(users, many=True)
    return Response(serializer.data)
 
 
@api_view(["GET"])                                              
def user_statistics(request):
    s = User.objects.aggregate(
        total_users=Count("id"), average_age=Avg("age"),
        min_age=Min("age"), max_age=Max("age"),
    )
    s["average_age"] = round(s["average_age"] or 0, 1)
    return Response(s)
 
@api_view(["GET", "POST"])                                      
def profile_list(request):
    if request.method == "GET":
        serializer = ProfileSerializer(Profile.objects.select_related("user").annotate(posts_count=Count("user__posts")), many=True)
        return Response(serializer.data)
    return create_object(ProfileSerializer, request)
 
 
@api_view(["GET", "PUT", "PATCH", "DELETE"])                   
def profile_detail(request, pk):
    profile = Profile.objects.select_related("user").annotate(posts_count=Count("user__posts")).get(pk=pk).first()
    if request.method == "GET":
        return Response(ProfileSerializer(profile).data)
    if request.method == "DELETE":
        profile.delete()
        return Response(status=204)
    return update_object(ProfileSerializer, profile, request)
 
 
@api_view(["GET"])                                            
def city_statistics(request):
    data = Profile.objects.values("city").annotate(users_count=Count("id")).order_by("-users_count")
    return Response(list(data))
 
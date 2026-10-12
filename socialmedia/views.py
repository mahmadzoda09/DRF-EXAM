from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count

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
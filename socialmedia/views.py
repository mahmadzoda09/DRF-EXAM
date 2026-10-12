from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count

from .models import *
from .serializers import *

def create_object(serializer_class, request):
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)      # sends 400 automatically if invalid
    serializer.save()
    return Response(serializer.data, status=201)

@api_view(["GET", "POST"])                                    
def user_list(request):
    if request.method == "GET":
        users = User.objects.annotate(
            posts_count=Count("posts", distinct=True),
            likes_count=Count("likes", distinct=True),
            favorites_count=Count("favorites", distinct=True),
        )
        return Response(UserSerializer(users, many=True).data)
    return create_object(UserSerializer, request)
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.db.models import Count , Max , Min , Avg , Q
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

def posts_qs():
    """Posts with likes_count and favorites_count already counted."""
    return Post.objects.select_related("user").annotate(
        likes_count=Count("likes", distinct=True),
        favorites_count=Count("favorites", distinct=True),
    )

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

@api_view(["GET", "POST"])                                      
def post_list(request):
    if request.method == "GET":
        return Response(PostSerializer(posts_qs(), many=True).data)
    return create_object(PostSerializer, request)
 
 
@api_view(["GET", "PUT", "PATCH", "DELETE"])                    
def post_detail(request, pk):
    post = get_object_or_404(posts_qs(), pk=pk)
    if request.method == "GET":
        return Response(PostDetailSerializer(post).data)
    if request.method == "DELETE":
        post.delete()
        return Response(status=204)
    return update_object(PostSerializer, post, request)
 
 
@api_view(["GET"])                                              
def user_posts(request, pk):
    user = User.objects.get(pk=pk)
    posts = (Post.objects.filter(user=user)
             .annotate(likes_count=Count("likes"))
             .values("id", "title", "likes_count", "views"))
    return Response({
        "user": {"id": user.id, "username": user.username},
        "posts_count": len(posts),
        "results": list(posts),
    })
 
 
@api_view(["GET"])                                              
def popular_posts(request):
    posts = posts_qs().filter(likes_count__gte=10).order_by("-likes_count")
    return Response(PopularPostSerializer(posts, many=True).data)
 
 
@api_view(["GET"])                                              
def post_search(request):
    q = request.query_params.get("q", "")
    posts = posts_qs().filter(Q(title__icontains=q) | Q(content__icontains=q))
    return Response(PostShortSerializer(posts, many=True).data)
 
 
@api_view(["GET"])                                              
def post_filter(request):
    p = request.query_params
    posts = posts_qs()
    if p.get("min_views"):
        posts = posts.filter(views__gte=p["min_views"])
    if p.get("max_views"):
        posts = posts.filter(views__lte=p["max_views"])
    if p.get("user_id"):
        posts = posts.filter(user_id=p["user_id"])
    return Response(PostShortSerializer(posts, many=True).data)
 
 
@api_view(["GET"])                                              
def post_statistics(request):
    post = Post.objects.aggregate(
        total_posts=Count("id"),  total_views=Sum("views"), average_views=Avg("views"),  max_views=Max("views"),  min_views=Min("views"),
    )
    post["total_views"] = post["total_views"] or 0
    post["average_views"] = round(post["average_views"] or 0, 1)
    post["total_likes"] = Like.objects.count()
    post["total_favorites"] = Favorite.objects.count()
    return Response(post)

@api_view(["GET"])                                             
def author_statistics(request):
    users = User.objects.annotate(posts_count=Count("posts")).filter(posts_count__gt=0)
    result = []
    for u in users:
        agg = u.posts.aggregate(total=Sum("views"), avg=Avg("views"))
        result.append({
            "user_id": u.id,
            "username": u.username,
            "posts_count": u.posts_count,
            "total_views": agg["total"] or 0,
            "average_views": round(agg["avg"] or 0, 1),
            "likes_received": Like.objects.filter(post__user=u).count(),
        })
    return Response(result)

@api_view(["GET", "POST"])                                      
def like_list(request):
    if request.method == "GET":
        likes = Like.objects.select_related("user", "post")
        return Response(LikeSerializer(likes, many=True).data)
    return create_object(LikeSerializer, request)
 
 
@api_view(["DELETE"])                                           
def like_delete(request, pk):
    Like.objects.get(pk=pk).delete()
    return Response(status=204)
 
 
@api_view(["GET"])                                              
def post_likes(request, pk):
    post = Post.objects.get(pk=pk)
    likes = post.likes.select_related("user")
    return Response({
        "post_id": post.id,
        "likes_count": likes.count(),
        "users": [{"id": l.user.id, "username": l.user.username} for l in likes],
    })
 
 
@api_view(["GET"])                                              
def top_posts(request):
    posts = posts_qs().order_by("-likes_count")[:10]
    return Response(TopPostSerializer(posts, many=True).data)
 
 
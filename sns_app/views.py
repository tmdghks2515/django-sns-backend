from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Comment, PostLike, BlackUser
from .serializers import PostSerializer, CommentSerializer, UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def like_post(request):
    user_id = request.data.get('userId')
    post = get_object_or_404(Post, id=request.data.get('postId'))
    user = get_object_or_404(User, id=user_id)
    blacks = BlackUser.objects.filter(Q(black_user__id=user_id) | Q(blacked_user__id=user_id))

    if any(black.black_user.id == post.author.id or black.blacked_user.id == post.author.id for black in blacks):
        return JsonResponse({'msg': '블랙리스트 입구컷이요'})

    try:
        exist_post_like = PostLike.objects.get(post=post, author=user)
        exist_post_like.delete()
        print("PostLike deleted.")

    except PostLike.DoesNotExist:
        new_post_like = PostLike(post=post, author=user)
        new_post_like.save()
        print("PostLike saved.")

    return Response()


@api_view(['POST'])
def black_user(request):
    user = get_object_or_404(User, id=request.data.get('black_user_id'))
    blacked_user = get_object_or_404(User, id=request.data.get('blacked_user_id'))
    BlackUser(
        black_user=user,
        blacked_user=blacked_user,
        reason=request.data.get('reason')
    ).save()

    return Response()


@api_view(['GET'])
def post_list(request):
    all_posts = Post.objects.all()

    user_id = request.data.get('user_id')
    blacks = BlackUser.objects.filter(Q(black_user__id=user_id) | Q(blacked_user__id=user_id))

    black_user_ids = []
    for black in blacks:
        if black.black_user.id == user_id:
            black_user_ids.append(black.blacked_user.id)
        if black.blacked_user.id == user_id:
            black_user_ids.append(black.black_user.id)

    filtered_posts = [post for post in all_posts if post.author.id not in black_user_ids]
    serialized_posts = serialize('json', filtered_posts)
    return JsonResponse({'filtered_posts': serialized_posts}, safe=False)


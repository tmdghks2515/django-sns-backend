from django.contrib.auth.models import User
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
    post = get_object_or_404(Post, id=request.data.get('postId'))
    user = get_object_or_404(User, id=request.data.get('userId'))
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

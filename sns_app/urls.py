from django.urls import path, include
from rest_framework import routers

from . import views
from .views import like_post, black_user

router = routers.DefaultRouter()
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)
router.register('user', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('post/like', like_post),
    path('user/black', black_user)
]

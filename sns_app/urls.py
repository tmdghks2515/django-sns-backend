from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter() #DefaultRouter를 설정
router.register('Post', views.PostViewSet) #itemviewset 과 item이라는 router 등록
router.register('Comment', views.CommentViewSet) #itemviewset 과 item이라는 router 등록

urlpatterns = [
    path('', include(router.urls))
]
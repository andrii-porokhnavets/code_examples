from django.urls import path

from .views import LikeList, analytics

urlpatterns = [
    path('', LikeList.as_view()),
    path('analytics/', analytics),
]

from django.urls import path

from .views import UserActivityDetail

urlpatterns = [
    path('<int:pk>/activity/', UserActivityDetail.as_view()),
]

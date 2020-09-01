from django.urls import path

from .views import PostList, like

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:post_pk>/like/', like),
]

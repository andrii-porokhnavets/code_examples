from rest_framework import generics

from .models import User
from .serializers import UserActivitySerializer


class UserActivityDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer

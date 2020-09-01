from rest_framework import serializers

from .models import User


class UserActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'last_request']

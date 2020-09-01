from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

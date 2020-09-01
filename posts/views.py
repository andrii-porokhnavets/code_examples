from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from likes.models import Like
from likes.serializers import LikeSerializer
from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST', 'DELETE'])
def like(request, post_pk):
    if not Post.objects.filter(pk=post_pk).exists():
        return Response({'message': 'Post was not found'}, status=status.HTTP_404_NOT_FOUND)

    existing_like = Like.objects.filter(post__pk=post_pk, user=request.user).first()

    if request.method == 'DELETE':
        if existing_like is None:
            return Response({'message': 'Like was not found'}, status.HTTP_400_BAD_REQUEST)

        existing_like.delete()

        return Response(status.HTTP_204_NO_CONTENT)

    serializer = LikeSerializer(existing_like)
    status_code = status.HTTP_200_OK
    error_occurred = False

    if existing_like is None:
        serializer = LikeSerializer(data={'post': post_pk, 'user': request.user.id})

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            error_occurred = True

    return Response(serializer.data if not error_occurred else serializer.errors, status=status_code)

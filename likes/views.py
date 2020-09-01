from datetime import date

from django.db.models import Count
from django.db.models.functions import TruncDate

from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Like
from .serializers import LikeSerializer


class LikeList(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


@api_view()
def analytics(request):
    try:
        date_from = date.fromisoformat(request.GET['date_from']) if 'date_from' in request.GET else None
        date_to = date.fromisoformat(request.GET['date_to']) if 'date_to' in request.GET else date.today()
    except ValueError:
        return Response({'message': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

    # qs = Like.objects.values(date=TruncDate('created_at')).filter(date__lte=date_to)
    qs = Like.objects.extra(select={'day': 'date(created_at)'}).values(date=TruncDate('created_at')).filter(date__lte=date_to)

    if date_from is not None:
        qs = qs.filter(date__gte=date_from)

    res = qs.annotate(count=Count('id'))

    return Response(list(res))

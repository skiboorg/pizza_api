from .serializers import *
from .models import *
from rest_framework import generics


class GetAll(generics.ListAPIView):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        return Promotion.objects.filter(is_active=True)
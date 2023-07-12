from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from . import seriaizers
from .models import (
    OrderTestInfo,
    OrderTestInfoStudent,
    OrderTestPack,
    OrderTestPackStudent,
)


class OrderTestInfoCreateView(generics.CreateAPIView):
    queryset = OrderTestInfo.objects.all()
    serializer_class = seriaizers.OrderTestInfoSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

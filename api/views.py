from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import *


class ProductAPIList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(store__user=user)


class StoreAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Store.objects.filter(user=user)


class StoreAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = (IsOwner, IsAuthenticated)

    def get_queryset(self):
        user = self.request.user
        return Store.objects.filter(user=user)
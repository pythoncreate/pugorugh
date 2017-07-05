from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.response import Response

from . import serializers
from . import models

AGE_RANGES = {
    'b': list(range(0, 6)),
    'y': list(range(6, 18)),
    'a': list(range(18, 72)),
    's': list(range(72, 192))
}

STATUSES = ['liked', 'disliked']


def get_age_ranges(keys='b,y,a,s'):
    """Returns age ranges in years."""
    data = []
    for key in keys.split(','):
        data.extend(AGE_RANGES[key])
    return data


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogFilterView(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DogSerializer


class DogViewSet(viewsets.ModelViewSet):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    #view for dog/<pk>/liked
    @detail_route(methods=['post', 'put'])
    def liked(self,request,pk=None):
        user = request.user
        dogs = models.UserDog.objects.filter(status="l", user=user)
        serializer = serializers.UserDogSerializer(dogs)
        return Response(serializer.data)


class UserPrefViewSet(viewsets.ModelViewSet):
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer


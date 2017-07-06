from bisect import bisect
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from rest_framework.response import Response

from . import serializers
from . import models

STATUSES = ['liked', 'disliked']


AGES = {
    'b': list(range(0, 6)),
    'y': list(range(6, 18)),
    'a': list(range(18, 72)),
    's': list(range(72, 192))
}


def get_ages(keys='b,y,a,s'):
    """Returns age ranges in years."""
    data = []
    for key in keys.split(','):
        data.extend(AGES[key])
    return data


class UserRegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class DogFilterView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.DogSerializer

    def get_ids(self, queryset=None):
        if queryset is not None:
            return [userdog.dog.pk for userdog in queryset]
        return []

    def filter_pref(self, dog_filter, user_prefs):
        userdog_query = models.UserDog.objects.filter(user=user_prefs.user.pk
                                                      ).select_related('dog')
        ages = get_ages(user_prefs.age)
        queryset = models.Dog.objects.filter(
            gender__in = user_prefs.gender.split(','),
            size__in = user_prefs.size.split(','),
            age__in = ages
        )
        if dog_filter not in STATUSES:
            dogs = self.get_ids(userdog_query)
            queryset = queryset.exclude(pk__in=dogs)
        else:
            userdog_query = userdog_query.filter(status=dog_filter[0])
            dogs = self.get_ids(userdog_query)
            queryset = queryset.filter(pk__in=dogs)

        return queryset.order_by('pk')

    def get_queryset(self):
        user = self.request.user
        dog_filter = self.kwargs.get('dog_filter')
        # Get user preferences
        user_prefs = get_object_or_404(models.UserPref, user=user)
        # Get age ranges(months) based on user preference selections
        queryset = self.filter_pref(dog_filter, user_prefs)
        return queryset

    def get_object(self):
        pk = int(self.kwargs.get('pk'))
        # Filter the query for the NEXT dog by pk.
        queryset = self.get_queryset().filter(
            pk__gt=pk
        )
        obj = queryset.first()
        if not obj:
            raise Http404
        return obj


class DogViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer

    #view for dog/<pk>/liked
    @detail_route(methods=['post', 'put'])
    def liked(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'l'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)

    # view for dog/<pk>/disliked
    @detail_route(methods=['post', 'put'])
    def disliked(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'd'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)


    # /api/dog/<pk>/undecided/
    @detail_route(methods=['post', 'put'])
    def undecided(self, request, pk=None):
        user = request.user
        dog = self.get_object()
        user_dog, created = models.UserDog.objects.get_or_create(
            user=user, dog=dog
        )
        user_dog.status = 'u'
        user_dog.save()
        serializer = serializers.UserDogSerializer(user_dog)
        return Response(serializer.data)


class UserPrefViewSet(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """View to get and update User Preferences."""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    # /api/user/preferences/
    @list_route(methods=['get', 'put'])
    def preferences(self, request, pk=None):
        user = request.user
        user_pref = models.UserPref.objects.get(user=user)

        if request.method == 'PUT':
            data = request.data
            user_pref.age = data.get('age') or user_pref.age
            user_pref.gender = data.get('gender')
            user_pref.size = data.get('size')
            user_pref.save()

        serializer = serializers.UserPrefSerializer(user_pref)
        return Response(serializer.data)
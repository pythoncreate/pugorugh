from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings

STATUS = (
    ('l', 'liked'),
    ('d', 'disliked')
)

AGE = (
    ('b', 'baby'),
    ('y', 'young'),
    ('a', 'adult'),
    ('s', 'senior')
)

GENDER = (
    ('m', 'male'),
    ('f', 'female'),
    ('u', 'unknown')
)

GENDER_PREF = (
    ('m', 'male'),
    ('f', 'female'),
)

SIZE = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown')
)

SIZE_PREF = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
)


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255, default='')
    breed = models.CharField(max_length=255, default='Unknown Breed')
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER, max_length=1)
    size = models.CharField(choices=SIZE, max_length=2)

    @property
    def get_image_url(self):
        return self.image_filename.name

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User)
    dog = models.ForeignKey(Dog, related_name='dogs')
    status = models.CharField(choices=STATUS, max_length=2)

    class Meta:
        unique_together = ('user', 'dog')

    def __str__(self):
        return '{} {} {}'.format(self.user, self.dog, self.get_status_display())


class UserPref(models.Model):
    user = models.OneToOneField(User)
    age = models.CharField(max_length=7, default='b,y,a,s')
    gender = models.CharField(max_length=3, default='m,f')
    size = models.CharField(max_length=8, default='s,m,l,xl')

    def __str__(self):
        return '{} preferences'.format(self.user)


def create_user_preference(sender, **kwargs):
    user = kwargs['instance']

    if kwargs['created']:
        UserPref.objects.create(user=user)

post_save.connect(create_user_preference, sender=User)
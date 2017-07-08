from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.conf import settings

GENDER = (
    ('m', 'male'),
    ('f', 'female'),
    ('u', 'unknown')
)

SIZE = (
    ('s', 'small'),
    ('m', 'medium'),
    ('l', 'large'),
    ('xl', 'extra large'),
    ('u', 'unknown')
)

STATUS = (
    ('l', 'liked'),
    ('d', 'disliked'),
)


class Dog(models.Model):
    name = models.CharField(max_length=255, default='unknown')
    image_filename = models.CharField(max_length=255, default='')
    breed = models.CharField(max_length=255, default='Unknown Breed')
    age = models.IntegerField(default=1, blank=True)
    gender = models.CharField(choices=GENDER, max_length=14,default="Unknown")
    size = models.CharField(choices=SIZE, max_length=12, default="Unkonwn")

    @property
    def get_image_url(self):
        return self.image_filename.name

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=1)

    def __str__(self):
        return '{} {} {}'.format(self.user, self.dog, self.get_status_display())


class UserPref(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
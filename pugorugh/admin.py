from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Dog)
admin.site.register(models.UserDog)
admin.site.register(models.UserPref)


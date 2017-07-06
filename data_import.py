import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from pugorugh.models import Dog
import json

with open('pugorugh/static/dog_details.json', 'r') as file:
    data = json.load(file)

    for item in data:
        Dog.objects.create(**item)

import django
django.setup()

from client.models import ModelList

m = ModelList.objects.all()

print(m)
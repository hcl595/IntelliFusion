from django.db import models

# Create your models here.
class ModelList(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    type = models.TextField()
    name = models.TextField()
    url = models.URLField()
    APIKey = models.TextField(default='\\')
    LaunchCompiler = models.FileField(default='\\')
    LaunchPath = models.FileField(default='\\')

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    Account = models.CharField(max_length=15)
    Email = models.EmailField()
    Password = models.TextField()

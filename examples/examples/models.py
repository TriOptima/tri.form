from django.db import models


class Foo(models.Model):
    name = models.CharField(max_length=255)
    a = models.IntegerField()
    b = models.BooleanField()


class Bar(models.Model):
    b = models.ForeignKey(Foo, on_delete=models.CASCADE)
    c = models.CharField(max_length=255)

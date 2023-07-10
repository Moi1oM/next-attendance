from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    tmi = models.TextField()
    time = models.DateTimeField()
    url = models.URLField()

    def __str__(self):
        return self.name + " : " + str(self.time)
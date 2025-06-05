from django.db import models

class Upload(models.Model):
    name = models.CharField(max_length=100)
    upload = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.description}"

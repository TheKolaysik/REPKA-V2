"""
Definition of models.
"""

from django.db import models
   
class Shops(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


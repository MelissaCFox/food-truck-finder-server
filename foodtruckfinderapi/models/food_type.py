from django.db import models

class FoodType(models.Model):
    type = models.CharField(max_length=50)

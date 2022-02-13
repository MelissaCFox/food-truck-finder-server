from django.db import models

class Neighborhood(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    profile_img_src = models.ImageField(upload_to='neighborhoods', height_field=None,
                                      width_field=None, max_length=100, null=True)
    linkNG = models.TextField()
    
    days_with_trucks = models.ManyToManyField("Day", through="TruckLocation", related_name="neighborhoods")

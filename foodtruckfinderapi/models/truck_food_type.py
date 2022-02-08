from django.db import models

class TruckFoodType(models.Model):
    type = models.ForeignKey("FoodType", on_delete=models.CASCADE, related_name="trucks")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name="types")

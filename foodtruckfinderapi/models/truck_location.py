from django.db import models

class TruckLocation(models.Model):
    neighborhood = models.ForeignKey("Neighborhood", on_delete=models.CASCADE, related_name="neighborhood_locations")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name="truck_locations")
    day = models.ForeignKey("Day", on_delete=models.CASCADE, related_name="day_locations")

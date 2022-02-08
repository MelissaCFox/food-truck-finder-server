from django.db import models

class TruckOwner(models.Model):
    user_account = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="trucks")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE)

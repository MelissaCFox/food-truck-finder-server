from django.db import models

class UserTruckFavorite(models.Model):
    user_account = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="user_favorites")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE)

from django.db import models

class UserSuggestion(models.Model):
    user_account = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="user_suggestions")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name="truck_suggestions")
    neighborhood = models.ForeignKey("Neighborhood", on_delete=models.CASCADE)
    date = models.DateField()
    message = models.TextField()
    read = models.BooleanField()
    include_contact = models.BooleanField()

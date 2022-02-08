from django.db import models

class UserTruckReview(models.Model):
    user_account = models.ForeignKey("UserAccount", on_delete=models.CASCADE, related_name="user_reviews")
    truck = models.ForeignKey("Truck", on_delete=models.CASCADE, related_name="truck_reviews")
    review = models.TextField()
    date = models.DateField()
    rating = models.IntegerField()
    anonymous = models.BooleanField()


    @property
    def author(self):
        """custom 'author' property checks if the current user
        is the author of a truck review

        Returns:
            boolean/bit data type
        """
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

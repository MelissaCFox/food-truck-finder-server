from django.db import models

from foodtruckfinderapi.models.user_truck_review import UserTruckReview

class Truck(models.Model):
    name = models.CharField(max_length=55)
    description = models.TextField()
    website_url = models.TextField(default="")
    facebook_url = models.TextField(default="")
    instagram_url = models.TextField(default="")
    twitter_url = models.TextField(default="")
    profile_img_src = models.TextField()
    hours = models.CharField(max_length=55)
    dollars = models.IntegerField()

    food_types = models.ManyToManyField("FoodType", through="TruckFoodType", related_name="trucks")
    owners = models.ManyToManyField("UserAccount", through="TruckOwner",
                                    related_name="trucks_owned")
    favorites = models.ManyToManyField("UserAccount", through="UserTruckFavorite",
                                       related_name="favorite_trucks")



    @property
    def favorite(self):
        """new custom 'favorite' property that checks if the active
        user has marked truck as a favorite

        Returns:
            boolean/bit data type
        """
        return self.__favorite

    @favorite.setter
    def favorite(self, value):
        self.__favorite = value
    
    
    @property
    def owner(self):
        """custom 'owner' property checks if the active user is an
        owner of that truck

        Returns:
            boolean/bit data type
        """
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value


    @property
    def user_rating(self):
        """calculates average user_rating based on the reviews that have
        been submitted for that truck

        Returns:
            an integer (if at least one review/rating has been submitted),
            or a string if no reviews/ratings exist yet
        """
        reviews = UserTruckReview.objects.filter(truck=self)

        total_rating = 0
        if len(reviews) > 0:
            for review in reviews:
                total_rating += review.rating

            average_rating = total_rating / len(reviews)
            rounded_average = round(average_rating, 1)
            return rounded_average
        else:
            return "No ratings yet"

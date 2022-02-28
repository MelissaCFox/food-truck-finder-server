from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from rest_framework import routers
from foodtruckfinderapi.views import (register_user, login_user, FoodTypeView, DayView,
                                    NeighborhoodView, TruckFoodTypeView, TruckLocationView,
                                    TruckView, UserSuggestionView, UserTruckFavoriteView,
                                    UserTruckReviewView, UserAccountView, TruckOwnerView)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'foodtypes', FoodTypeView, 'foodtype')
router.register(r'days', DayView, 'day')
router.register(r'neighborhoods', NeighborhoodView, 'neighborhood')
router.register(r'truckFoodTypes', TruckFoodTypeView, 'truckFoodType')
router.register(r'truckLocations', TruckLocationView, 'truckLocation')
router.register(r'trucks', TruckView, 'truck')
router.register(r'suggestions', UserSuggestionView, 'suggestion')
router.register(r'userTruckFavorites', UserTruckFavoriteView, 'userTruckFavorite')
router.register(r'userTruckReviews', UserTruckReviewView, 'userTruckReview')
router.register(r'users', UserAccountView, 'user')
router.register(r'truckOwners', TruckOwnerView, 'truckOwner')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

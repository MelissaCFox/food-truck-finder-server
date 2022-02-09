from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import (Truck, UserAccount)



class TruckView(ViewSet):

    def list(self, request):
        """Handle GET requests to trucks resource

        Returns:
            Response: JSON serialized list of truck instances
        """
        trucks=Truck.objects.all()
        user_account = UserAccount.objects.get(pk = request.auth.user.id)
        ## set custom favorite and owner properties (booleans)
        for truck in trucks:
            truck.owner = user_account in truck.owners.all()
            truck.favorite = user_account in truck.favorites.all()

        serializer=TruckSerializer(trucks, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single truck

        Returns:
            Response: JSON serialized truck instance
        """
        try:
            truck=Truck.objects.get(pk=pk)
            user_account = UserAccount.objects.get(pk = request.auth.user.id)
            ## set custom favorite and owner properties (booleans)
            truck.owner = user_account in truck.owners.all()
            truck.favorite = user_account in truck.favorites.all()

            serializer = TruckSerializer(truck)
            return Response(serializer.data)
        except Truck.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single truck

        Returns:
            Response: JSON serialized truck instance
        """
        truck = Truck(
            name = request.data['name'],
            description = request.data['description'],
            website_url = request.data['websiteURL'],
            facebook_url = request.data['facebookURL'],
            instagram_url = request.data['instagramURL'],
            twitter_url = request.data['twitterURL'],
            profile_img_src = request.data['profileImgSrc'],
            hours = request.data['hours'],
            dollars = request.data['dollars'],
        )


        try:
            truck.save()
            truck.food_types.set(request.data['foodTypes'])
            serializer = TruckSerializer(truck, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for a truck

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            truck = Truck.objects.get(pk=pk)
            truck.name = request.data['name']
            truck.description = request.data['description']
            truck.website_url = request.data['websiteURL']
            truck.facebook_url = request.data['facebookURL']
            truck.instagram_url = request.data['instagramURL']
            truck.twitter_url = request.data['twitterURL']
            truck.profile_img_src = request.data['profileImgSrc']
            truck.hours = request.data['hours']
            truck.dollars = request.data['dollars']

            truck.save()
            
            truck.food_types.set(request.data['foodTypes'])
            
            serializer = TruckSerializer(truck)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except Truck.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        """Handle DELETE request for a single truck

        Returns:
            Response: 204 or 404 status code
        """
        try:
            truck = Truck.objects.get(pk=pk)
            truck.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Truck.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = ('id', 'name','description', 'website_url', 'facebook_url', 'instagram_url',
                  'twitter_url', 'profile_img_src', 'hours', 'dollars',
                  'food_types', 'favorite', 'owner', 'user_rating')
        depth = 1

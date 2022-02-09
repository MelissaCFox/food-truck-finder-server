from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import UserTruckFavorite, Truck, UserAccount


class UserTruckFavoriteView(ViewSet):

    def list(self, request):
        """Handle GET requests to user_truck_favorites resource

        Returns:
            Response: JSON serialized list of user_truck_favorite instances
        """
        favorites=UserTruckFavorite.objects.all()

        serializer=UserTruckFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single user_truck_favorite

        Returns:
            Response: JSON serialized user_truck_favorite instance
        """
        try:
            user_truck_favorite=UserTruckFavorite.objects.get(pk=pk)
            serializer = UserTruckFavoriteSerializer(user_truck_favorite)
            return Response(serializer.data)
        except UserTruckFavorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single user_truck_favorite

        Returns:
            Response: JSON serialized user_truck_favorite instance
        """
        user_truck_favorite = UserTruckFavorite()

        user_truck_favorite.user_account = UserAccount.objects.pk(pk=request.author.user.id)
        user_truck_favorite.truck = Truck.objects.get(pk = request.data['truck'])
        
        try:
            user_truck_favorite.save()
            serializer = UserTruckFavoriteSerializer(user_truck_favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        """Handle DELETE request for a single user_truck_favorite

        Returns:
            Response: 204 or 404 status code
        """
        try:
            user_truck_favorite = UserTruckFavorite.objects.get(pk=pk)
            user_truck_favorite.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except UserTruckFavorite.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserTruckFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTruckFavorite
        fields = ('id', 'truck','user_account')
        depth = 1

from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import TruckFoodType
from foodtruckfinderapi.models.food_type import FoodType
from foodtruckfinderapi.models.truck import Truck


class TruckFoodTypeView(ViewSet):

    def list(self, request):
        """Handle GET requests to truck_food_types resource

        Returns:
            Response: JSON serialized list of truck_food_type instances
        """
        truck_food_types=TruckFoodType.objects.all()

        serializer=TruckFoodTypeSerializer(truck_food_types, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single truck_food_type

        Returns:
            Response: JSON serialized truck_food_type instance
        """
        try:
            truck_food_type=TruckFoodType.objects.get(pk=pk)
            serializer = TruckFoodTypeSerializer(truck_food_type)
            return Response(serializer.data)
        except TruckFoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single truck_food_type

        Returns:
            Response: JSON serialized truck_food_type instance
        """
        truck_food_type = TruckFoodType()
        type = FoodType.objects.get(pk=request.data['foodTypeId'])
        truck = Truck.objects.get(pk = request.data['truckId'])
        truck_food_type.type = type
        truck_food_type.truck = truck
        
        try:
            truck_food_type.save()
            serializer = TruckFoodTypeSerializer(truck_food_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)
   
    
    def destroy(self, request, pk=None):
        """Handle DELETE request for a single truck_food_type

        Returns:
            Response: 204 or 404 status code
        """
        try:
            truck_food_type = TruckFoodType.objects.get(pk=pk)
            truck_food_type.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TruckFoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TruckFoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckFoodType
        fields = ('id', 'truck','type')


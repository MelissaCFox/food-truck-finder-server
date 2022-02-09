from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import FoodType


class FoodTypeView(ViewSet):

    def list(self, request):
        """Handle GET requests to food_types resource

        Returns:
            Response: JSON serialized list of food_type instances
        """
        food_types=FoodType.objects.all()

        serializer=FoodTypeSerializer(food_types, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single food_type

        Returns:
            Response: JSON serialized food_type instance
        """
        try:
            food_type=FoodType.objects.get(pk=pk)
            serializer = FoodTypeSerializer(food_type)
            return Response(serializer.data)
        except FoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single food_type

        Returns:
            Response: JSON serialized food_type instance
        """
        food_type = FoodType()
        food_type.type = request.data['type']
        
        try:
            food_type.save()
            serializer = FoodTypeSerializer(food_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE request for a single food_type

        Returns:
            Response: 204 or 404 status code
        """
        try:
            food_type = FoodType.objects.get(pk=pk)
            food_type.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except FoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class FoodTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodType
        fields = ('id', 'type')
        depth = 1

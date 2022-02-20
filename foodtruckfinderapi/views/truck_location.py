from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from foodtruckfinderapi.models import TruckLocation
from foodtruckfinderapi.models.day import Day
from foodtruckfinderapi.models.neighborhood import Neighborhood
from foodtruckfinderapi.models.truck import Truck
from foodtruckfinderapi.views.truck import TruckSerializer


class TruckLocationView(ViewSet):

    def list(self, request):
        """Handle GET requests to truck_locations resource

        Returns:
            Response: JSON serialized list of truck_location instances
        """
        neighborhood_id = self.request.query_params.get('neighborhoodId', None)
        day_id = self.request.query_params.get('dayId', None)
        truck_id = self.request.query_params.get('truckId', None)

        filter_params = Q()
        if neighborhood_id:
            filter_params &= Q(neighborhood_id = neighborhood_id)
        if day_id:
            filter_params &= Q(day_id = day_id)
        if truck_id:
            filter_params &= Q(truck_id = truck_id)

        locations = TruckLocation.objects.filter(filter_params)


        serializer=TruckLocationSerializer(locations, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single truck_location

        Returns:
            Response: JSON serialized truck_location instance
        """
        try:
            truck_location=TruckLocation.objects.get(pk=pk)
            serializer = TruckLocationSerializer(truck_location)
            return Response(serializer.data)
        except TruckLocation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single truck_location

        Returns:
            Response: JSON serialized truck_location instance
        """
        truck_location = TruckLocation()
        truck_location.neighborhood = Neighborhood.objects.get(pk=request.data['neighborhood'])
        truck_location.day = Day.objects.get(pk=request.data['day'])
        truck_location.truck = Truck.objects.get(pk = request.data['truck'])
        
        try:
            truck_location.save()
            serializer = TruckLocationSerializer(truck_location, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for a truck_location

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            truck_location = TruckLocation.objects.get(pk=pk)
            truck_location.neighborhood = Neighborhood.objects.get(pk=request.data['neighborhood'])

            truck_location.save()
            serializer = TruckLocationSerializer(truck_location)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except TruckLocation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        """Handle DELETE request for a single truck_location

        Returns:
            Response: 204 or 404 status code
        """
        try:
            truck_location = TruckLocation.objects.get(pk=pk)
            truck_location.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TruckLocation.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TruckLocationSerializer(serializers.ModelSerializer):
    truck = TruckSerializer()

    class Meta:
        model = TruckLocation
        fields = ('id', 'truck','neighborhood', 'day')
        depth = 1



from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
from foodtruckfinderapi.models import Neighborhood


class NeighborhoodView(ViewSet):

    def list(self, request):
        """Handle GET requests to neighborhoods resource

        Returns:
            Response: JSON serialized list of neighborhood instances
        """
        search_text = self.request.query_params.get('q', None)
        if search_text is not None:
            neighborhoods=Neighborhood.objects.filter(
                Q(name__contains=search_text) |
                Q(description__contains=search_text)
            ).distinct()
        else:
            neighborhoods=Neighborhood.objects.all()
        
        serializer=NeighborhoodSerializer(neighborhoods, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single neighborhood

        Returns:
            Response: JSON serialized neighborhood instance
        """
        try:
            food_type=Neighborhood.objects.get(pk=pk)
            serializer = NeighborhoodSerializer(food_type)
            return Response(serializer.data)
        except Neighborhood.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class NeighborhoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'description', 'profile_img_src', 'linkNG', 'map_img_src', 'days_with_trucks')
        depth = 1

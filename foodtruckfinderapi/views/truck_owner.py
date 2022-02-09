from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import TruckOwner, Truck, UserAccount


class TruckOwnerView(ViewSet):

    def list(self, request):
        """Handle GET requests to truck_owners resource

        Returns:
            Response: JSON serialized list of truck_owner instances
        """
        owners=TruckOwner.objects.all()

        serializer=TruckOwnerSerializer(owners, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single truck_owner

        Returns:
            Response: JSON serialized truck_owner instance
        """
        try:
            truck_owner=TruckOwner.objects.get(pk=pk)
            serializer = TruckOwnerSerializer(truck_owner)
            return Response(serializer.data)
        except TruckOwner.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single truck_owner

        Returns:
            Response: JSON serialized truck_owner instance
        """
        truck_owner = TruckOwner()

        truck_owner.user_account = UserAccount.objects.pk(pk=request.author.user.id)
        truck_owner.truck = Truck.objects.get(pk = request.data['truck'])

        try:
            truck_owner.save()
            serializer = TruckOwnerSerializer(truck_owner, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        """Handle DELETE request for a single truck_owner

        Returns:
            Response: 204 or 404 status code
        """
        try:
            truck_owner = TruckOwner.objects.get(pk=pk)
            truck_owner.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TruckOwner.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class TruckOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TruckOwner
        fields = ('id', 'truck','user_account')
        depth = 1
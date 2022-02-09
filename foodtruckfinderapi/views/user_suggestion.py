from datetime import date
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import UserSuggestion, Truck, UserAccount
from foodtruckfinderapi.models.neighborhood import Neighborhood


class UserSuggestionView(ViewSet):

    def list(self, request):
        """Handle GET requests to user_suggestions resource

        Returns:
            Response: JSON serialized list of user_suggestion instances
        """
        categories=UserSuggestion.objects.all()

        serializer=UserSuggestionSerializer(categories, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single user_suggestion

        Returns:
            Response: JSON serialized user_suggestion instance
        """
        try:
            user_suggestion=UserSuggestion.objects.get(pk=pk)
            serializer = UserSuggestionSerializer(user_suggestion)
            return Response(serializer.data)
        except UserSuggestion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single user_suggestion

        Returns:
            Response: JSON serialized user_suggestion instance
        """
        user_account = UserAccount.objects.get(pk = request.auth.user.id)
        truck = Truck.objects.get(pk = request.data['truckId'])
        neighborhood = Neighborhood.objects.get(pk = request.data['neighborhoodId'])

        user_suggestion = UserSuggestion.objects.create(
            user_account = user_account,
            truck = truck,
            date = date.today(),
            message = request.data['message'],
            neighborhood = neighborhood,
            include_contact = request.data['includeContact'],
            read = False,
        )

        try:
            user_suggestion.save()
            serializer = UserSuggestionSerializer(user_suggestion, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for a user_suggestion

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            user_suggestion = UserSuggestion.objects.get(pk=pk)
            user_suggestion.read = request.data['read']

            user_suggestion.save()

            serializer = UserSuggestionSerializer(user_suggestion)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except UserSuggestion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, pk=None):
        """Handle DELETE request for a single user_suggestion

        Returns:
            Response: 204 or 404 status code
        """
        try:
            user_suggestion = UserSuggestion.objects.get(pk=pk)
            user_suggestion.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except UserSuggestion.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserSuggestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSuggestion
        fields = ('id', 'user_account', 'truck','neighborhood', 'message', 'date', 'read',
                  'include_contact')
        depth = 2

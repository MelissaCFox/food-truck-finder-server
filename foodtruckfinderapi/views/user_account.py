from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodtruckfinderapi.models import UserAccount
from foodtruckfinderapi.views.truck import TruckSerializer
from foodtruckfinderapi.views.user_truck_favorite import UserTruckFavoriteSerializer


class UserAccountView(ViewSet):

    def list(self, request):
        """Handle GET requests to user_accounts resource

        Returns:
            Response: JSON serialized list of user_account instances
        """
        user_accounts=UserAccount.objects.all()

        serializer=UserAccountSerializer(user_accounts, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single user_account

        Returns:
            Response: JSON serialized user_account instance
        """
        try:
            user_account=UserAccount.objects.get(pk=pk)
            serializer = UserAccountSerializer(user_account)
            return Response(serializer.data)
        except UserAccount.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserAccountSerializer(serializers.ModelSerializer):
    favorites = UserTruckFavoriteSerializer(many=True)

    class Meta:
        model = UserAccount
        fields = ('id', 'user', 'owner', 'favorites', 'reviews', 'trucks')
        depth = 2

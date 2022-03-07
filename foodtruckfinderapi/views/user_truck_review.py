from datetime import date
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import DjangoModelPermissions
from django.db.models import Q
from foodtruckfinderapi.models import UserTruckReview, Truck, UserAccount


class UserTruckReviewView(ViewSet):

    permission_classes = [ DjangoModelPermissions ]
    queryset = UserTruckReview.objects.none()

    def list(self, request):
        """Handle GET requests to reviews resource

        Returns:
            Response: JSON serialized list of review instances
        """
        ## check for query params
        truck_id = self.request.query_params.get('truckId', None)
        if truck_id is not None:
            reviews = UserTruckReview.objects.filter(
                Q(truck_id=truck_id)
            ).order_by('-date')

        else:
            reviews=UserTruckReview.objects.all()

        user_account = UserAccount.objects.get(pk = request.auth.user.id)
        for review in reviews:
            review.author = review.user_account == user_account

        serializer=UserTruckReviewSerializer(reviews, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        """Handle GET request for a single review

        Returns:
            Response: JSON serialized review instance
        """
        try:
            review=UserTruckReview.objects.get(pk=pk)

            user_account = UserAccount.objects.get(pk = request.auth.user.id)
            review.author = review.user_account == user_account

            serializer = UserTruckReviewSerializer(review)
            return Response(serializer.data)
        except UserTruckReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):
        """Handle POST request for a single review

        Returns:
            Response: JSON serialized review instance
        """
        user_account = UserAccount.objects.get(pk = request.auth.user.id)
        truck = Truck.objects.get(pk = request.data['truckId'])

        review = UserTruckReview.objects.create(
            user_account = user_account,
            truck = truck,
            date = date.today(),
            review = request.data['review'],
            rating = request.data['rating'],
            anonymous = request.data['anonymous']
        )

        try:
            review.save()
            serializer = UserTruckReviewSerializer(review, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None):
        """Handle PUT requests for a review

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            review = UserTruckReview.objects.get(pk=pk)

            review.review = request.data['review']
            review.rating = request.data['rating']
            review.anonymous = request.data['anonymous']

            review.save()

            serializer = UserTruckReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        except UserTruckReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, pk=None):
        """Handle DELETE request for a single review

        Returns:
            Response: 204 or 404 status code
        """
        try:
            review = UserTruckReview.objects.get(pk=pk)
            review.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except UserTruckReview.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserTruckReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTruckReview
        fields = ('id', 'review', 'date','rating', 'anonymous', 'truck',
                  'user_account', 'author')
        depth = 2

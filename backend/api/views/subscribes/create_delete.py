from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.subscribes.limit_recipe import LimitSerialisers
from api.serializers.subscribes.serializers import (
    SubscriptionSerializers,
    SubscribeValidationSerializers,
    SubscribeValidationDeleteSerializers
)
from recipes.models import Subscription


class SubscribeCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        limit = LimitSerialisers(data={}, context={'request': request})
        limit.is_valid(raise_exception=True)
        validation_serializer = SubscribeValidationSerializers(
            data=kwargs,
            context={'request': request}
        )
        validation_serializer.is_valid(raise_exception=True)
        author = validation_serializer.validated_data['author']
        subscription = Subscription.objects.create(client=request.user,
                                                   author=author)
        serializer = SubscriptionSerializers(
            subscription,
            context=({'recipes_limit': limit.validated_data['recipes_limit']})
        ).data

        return Response(serializer, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        validation_serializer = SubscribeValidationDeleteSerializers(
            data=kwargs,
            context={'request': request}
        )
        validation_serializer.is_valid(raise_exception=True)
        validation_serializer.validated_data['subscribe'].delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

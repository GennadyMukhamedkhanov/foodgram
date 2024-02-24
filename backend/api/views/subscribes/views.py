from rest_framework import status
from rest_framework.pagination import PageNumberPagination
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


class SubscribeListView(APIView):
    def get(self, request):
        page_size = request.query_params.get('limit')
        paginator = PageNumberPagination()
        if page_size and int(page_size) > 0:
            paginator.page_size = request.query_params.get('limit')

        limit = LimitSerialisers(data={}, context={'request': request})
        limit.is_valid(raise_exception=True)

        subscribes = Subscription.objects.filter(client=request.user)
        paginated_queryset = paginator.paginate_queryset(subscribes, request)
        serializer = SubscriptionSerializers(
            paginated_queryset, many=True,
            context=(
            {'recipes_limit': limit.validated_data['recipes_limit']})).data

        return Response(serializer, status=status.HTTP_200_OK)


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

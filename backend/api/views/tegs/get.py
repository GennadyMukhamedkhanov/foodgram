from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.serializers.tegs.serializers import TegSerialisers
from api.services.tags.get import TegGetService


class TegsGetView(APIView):
    def get(self, request, **kwargs):
        teg = TegGetService.execute({
            'id': kwargs['id']
        })
        serializer = TegSerialisers(teg).data
        return Response(serializer, status=status.HTTP_200_OK)

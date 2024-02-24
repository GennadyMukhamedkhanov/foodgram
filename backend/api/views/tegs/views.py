from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.tegs.serializers import TegSerialisers
from api.services.tags import TegListService, TegGetService


class TegsListView(APIView):
    def get(self, request):
        tegs = TegListService.execute({})
        return Response(tegs)

class TegsGetView(APIView):
    def get(self, request, **kwargs):
        teg = TegGetService.execute({
            'id':kwargs['id']
        })
        return Response(teg)


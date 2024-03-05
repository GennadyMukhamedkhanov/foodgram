from rest_framework.response import Response
from rest_framework.views import APIView
from api.services.tags.list import TegListService


class TegsListView(APIView):
    def get(self, request):
        tegs = TegListService.execute({})
        return Response(tegs)
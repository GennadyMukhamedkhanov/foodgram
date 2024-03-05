from service_objects.services import Service
from django import forms

from api.serializers.tegs.serializers import TegSerialisers
from recipes.models import Tag


class TegListService(Service):
    def process(self):
        tegs = Tag.objects.all()
        serializer = TegSerialisers(tegs, many=True).data
        return serializer
from service_objects.services import Service
from django import forms

from api.serializers.tegs.serializers import TegSerialisers
from recipes.models.tag.models import Tag


class TegListService(Service):
    def process(self):
        tegs = Tag.objects.all()
        serializer = TegSerialisers(tegs, many=True).data
        return serializer

class TegGetService(Service):
    id = forms.IntegerField()

    def process(self):
        id = self.cleaned_data['id']
        tegs = Tag.objects.filter(id=id)
        if not tegs.exists():
            raise ValueError('the id is not specified correctly')
        serializer = TegSerialisers(tegs.first()).data
        return serializer
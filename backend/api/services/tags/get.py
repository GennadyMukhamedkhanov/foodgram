from service_objects.services import Service
from django import forms
from recipes.models import Tag

class TegGetService(Service):
    id = forms.IntegerField()

    def process(self):
        id_tag = self.cleaned_data['id']
        tegs = self.get_tags(id_tag)
        self.tegs_check(tegs)

        return tegs.first()

    @staticmethod
    def get_tags(id_tag):
        return Tag.objects.filter(id=id_tag)

    @staticmethod
    def tegs_check(tegs):
        if not tegs.exists():
            raise ValueError('the id is not specified correctly')

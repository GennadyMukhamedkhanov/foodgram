from service_objects.services import Service
from recipes.models import Recipe


class RecipesListService(Service):
    def process(self):
        return Recipe.objects.all()

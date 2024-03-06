from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.services.recipes.add import RecipesAddService
from api.services.recipes.list import RecipesListService
from api.serializers.recipes.creating_recipe_serializers import (
    CreatingRecipeSerializer)
from api.serializers.recipes.recipes_list_serializers import (
    RecipesListSerializers)


class RecipesListAddView(APIView):
    def get(self, request):
        data = RecipesListService.execute({})
        serializer = RecipesListSerializers(
            data, many=True, context=({'request': request})
        ).data

        return Response({'results': serializer})

    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        data = RecipesAddService.execute(
            {
                'ingredients': request.data.get('ingredients'),
                'tags': request.data.get('tags'),
                'name': request.data.get('name'),
                'text': request.data.get('text'),
                'cooking_time': int(request.data.get('cooking_time')),
                'image': request.data.get('image'),
                'author': request.user
            }

        )
        serializer = CreatingRecipeSerializer(data).data
        return Response(serializer)

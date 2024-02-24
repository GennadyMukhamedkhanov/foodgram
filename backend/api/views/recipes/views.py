from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from service_objects.errors import InvalidInputsError

from api.permissions.recipes import IsAuthor
from api.serializers.recipes.creating_recipe_serializers import \
    CreatingRecipeSerializer
from api.serializers.recipes.recipes_list_serializers import \
    RecipesListSerializers
from api.services.recipes import RecipesListService, RecipesAddService, \
    RecipesPatchService, RecipesDeleteService
from recipes.models import Recipe


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
                'ingredients': request.data['ingredients'],
                'tags': request.data['tags'],
                'name': request.data['name'],
                'text': request.data['text'],
                'cooking_time': int(request.data['cooking_time']),
                'image': request.data['image'],
                'author': request.user
            }

        )
        serializer = CreatingRecipeSerializer(data).data
        return Response(serializer)


class RecipesGetPatchDeleteView(APIView):
    def get(self, request, **kwargs):
        data = get_object_or_404(Recipe, id=kwargs['id'])

        return Response(
            RecipesListSerializers(data, context={'request': request}).data)

    def patch(self, request, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthor]
        self.check_permissions(request)
        self.check_object_permissions(
            request=request,
            obj=Recipe.objects.get(id=kwargs['id'])
        )

        try:
            data = RecipesPatchService.execute(
                {
                    'id': kwargs['id'],
                    'ingredients': request.data.get('ingredients'),
                    'tags': request.data.get('tags'),
                    'name': request.data.get('name'),
                    'text': request.data.get('text'),
                    'cooking_time': request.data.get('cooking_time'),
                    'image': request.data.get('image'),
                    'author': request.user
                }
            )
        except InvalidInputsError as error:
            return Response(error.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreatingRecipeSerializer(data).data
        return Response(serializer)

    def delete(self, request, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthor]
        self.check_permissions(request)
        self.check_object_permissions(
            request=request,
            obj=Recipe.objects.get(id=kwargs['id'])
        )

        RecipesDeleteService.execute(
            {
                'id': kwargs['id'],
            }
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

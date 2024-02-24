from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from api.serializers.users.serializers import (UserCreateSerializer,
                                               UsersGetSerialisers,
                                               TokenSerializer, TokenObject,
                                               UserChangePassword)
from users.models import User


class UserListCreateView(APIView):
    def get(self, request):
        page_size = request.query_params.get('limit')
        #page = request.query_params.get('page')
        users = User.objects.all()
        paginator = PageNumberPagination()
        if page_size and int(page_size) > 0:
            paginator.page_size = page_size

        # if page and int(page) > 0:
        #     paginator.page_number = page

        paginated_queryset = paginator.paginate_queryset(users, request)
        ser = UsersGetSerialisers(paginated_queryset, many=True).data

        return paginator.get_paginated_response(ser)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(UsersGetSerialisers(obj).data,
                        status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, **kwargs):
        obj = get_object_or_404(User, id=kwargs['id'])

        return Response(
            UsersGetSerialisers(obj).data,
            status=status.HTTP_200_OK
        )


class PersonalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = request.user
        serializer = UsersGetSerialisers(instance).data
        return Response(serializer, status=status.HTTP_200_OK)


class SetPasswordView(APIView):
    def post(self, request):
        serializer = UserChangePassword(data={
            'id': request.user.id,
            'password': request.data['password']
        })
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['id']
        obj.set_password(request.data['new_password'])
        obj.save()

        return Response({'password': 'изменен'})


class TokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['user']
        token = Token.objects.filter(user=obj)
        if not token.exists():
            token = Token.objects.create(user=obj)
        else:
            token = token.first()

        return Response({
            'Token': token.key
        })


class TokenLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TokenObject(data={}, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data['obj_token']
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers.users.serializers import (UserCreateSerializer,
                                               UsersGetSerialisers,
                                               )
from users.models import User


class UserListCreateView(APIView):
    def get(self, request):
        page_size = request.query_params.get('limit')
        users = User.objects.all()
        paginator = PageNumberPagination()
        if page_size and int(page_size) > 0:
            paginator.page_size = page_size

        paginated_queryset = paginator.paginate_queryset(users, request)
        ser = UsersGetSerialisers(paginated_queryset, many=True).data

        return paginator.get_paginated_response(ser)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response(UsersGetSerialisers(obj).data,
                        status=status.HTTP_201_CREATED)

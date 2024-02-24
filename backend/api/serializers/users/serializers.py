from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from users.models import User


class UsersGetSerialisers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            'password'
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TokenSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(
            email=attrs['email']
        )
        if (not user.exists()) or (
                not user.first().check_password(attrs['password'])):
            raise ValidationError('Data is not valid')
        attrs['user'] = user.first()

        return attrs


class TokenObject(serializers.Serializer):

    def validate(self, attrs):
        obj_token = Token.objects.filter(user=self.context['user'])
        if not obj_token.exists():
            raise ValidationError('The user is not logged in')
        attrs['obj_token'] = obj_token.first()
        return attrs


class UserChangePassword(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    password = serializers.CharField()

    def validate(self, attrs):
        obj_user = attrs['id']
        if not obj_user.check_password(attrs['password']):
            raise ValidationError('Incorrect password')
        return attrs

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers


class LimitSerialisers(serializers.Serializer):

    def validate(self, attrs):
        try:
            recipes_limit = int(self.context['request'].query_params['recipes_limit'])
            if recipes_limit < 1:
                recipes_limit = 1
        except (ValueError, MultiValueDictKeyError):
            recipes_limit = 1
        attrs['recipes_limit'] = recipes_limit

        return attrs

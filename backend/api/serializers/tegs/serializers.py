from rest_framework import serializers

from recipes.models.tag.models import Tag


class TegSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'name',
            'color',
            'slug'
        )

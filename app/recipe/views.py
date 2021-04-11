from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import redis
import os
import json
from core.models import Tag, Ingredient

from recipe import serializers


# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=os.environ.get('REDIS_HOST'),
                                   port=os.environ.get('REDIS_PORT'), db=0)


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Manage ingredients in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def perform_create(self, serializer):
        """Create a new ingredient"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""

        ingredients = None

        if not redis_instance.get(f'ingredientsx:{self.request.user.email}'):
            print('not in cache')
            ingredients = self.queryset.filter(
                user=self.request.user).order_by('-name')
            ingredients_to_cache = f'{list(ingredients.values())}'
            redis_instance.setex(f'ingredientsx:{self.request.user.email}', 60,
                                 json.dumps(ingredients_to_cache))
        else:
            print('in cache')
            ingredients = redis_instance.get(
                f'ingredientsx:{self.request.user.email}').decode(
                "utf-8").replace('"', "").replace("'", '"')
            ingredients = eval(ingredients)
            return ingredients

        ingredients = self.queryset.filter(
            user=self.request.user).order_by('-name')

        return ingredients

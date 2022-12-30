from rest_framework import serializers

from core.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):

    categories = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'price_rrc', 'categories']

    def get_categories(self, instance):
        return list(instance.categories.values_list('name', flat=True))



from rest_framework import serializers

from core.models import ItemInShoppingBasket, Shop, ProductInfo, ShoppingBasket


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']


class ProductInfoSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    name = serializers.CharField(source='product__name')
    model = serializers.CharField(source='product__model')
    class Meta:
        model = ProductInfo
        fields = ['price', 'name', 'model']


class ItemSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    product = ProductInfoSerializer(source='product_info')
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = ItemInShoppingBasket
        fields = ['id', 'shop', 'product', 'quantity']

    def get_total_price(self, instance: ItemInShoppingBasket):
        return instance.product_info.price * instance.quantity


class ItemInShoppingBasketSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product_info.product.name')
    shop = serializers.CharField(source='product_info.shop.name')
    price = serializers.DecimalField(source='product_info.price', max_digits=8, decimal_places=2)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = ItemInShoppingBasket
        fields = ['name', 'shop', 'price', 'quantity', 'total_price']

    def get_total_price(self, instance):
        return '{:.2f}'.format(instance.total_price)


class BasketSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    items = ItemInShoppingBasketSerializer(many=True)
    class Meta:
        model = ShoppingBasket
        fields = ['items', 'total_quantity', 'total_price']

    def get_total_quantity(self, instance):
        return sum([i.quantity for i in instance.items.all()])

    def get_total_price(self, instance):
        total_price = sum([i.total_price for i in instance.items.all()])
        return '{:.2f}'.format(total_price)


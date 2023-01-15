from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Product, ShoppingBasket
from core.serializers.products import ProductSerializer
from core.serializers.shopping_basket import BasketSerializer


class ProductsView(views.APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: ProductSerializer()})
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class BasketView(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketSerializer
    def get(self, request, *args, **kwargs):
        shopping_basket = ShoppingBasket.objects.prefetch_related('items__product_info', 'items__shop').get(user=request.user)
        serializer = BasketSerializer(shopping_basket)
        return Response(serializer.data)

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Product
from core.serializers import ProductSerializer


class ProductsView(views.APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: ProductSerializer()})
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)






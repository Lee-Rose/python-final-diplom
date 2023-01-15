from django.urls import path

from core.views import ProductsView, BasketView

urlpatterns = [
    path('products/', ProductsView.as_view()),
    path('basket/', BasketView.as_view()),

]
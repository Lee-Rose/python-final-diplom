from django.urls import path

from core.views import ProductsView

urlpatterns = [
    path('products/', ProductsView.as_view()),

]
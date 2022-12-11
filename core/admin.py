from django.contrib import admin
from django.contrib.admin import register

from core.models import Shop, Category, Product, Parameter, ProductParameter


admin.site.register(Parameter)

admin.site.register(ProductParameter)


@register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'model', 'price_rrc']
    list_display_links = ['id', 'name', 'model']
    list_filter = ['categories']
    search_fields = ['name', 'model']
    ordering = ['name', 'price_rrc']

    autocomplete_fields = ['categories']
    # raw_fields = ['categories']


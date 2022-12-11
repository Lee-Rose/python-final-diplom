from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampModel(models.Model):
    created_at = models.DateTimeField('created', auto_now_add=True)
    updated_at = models.DateTimeField('updated', auto_now=True)

    class Meta:
        abstract = True


class Shop(TimeStampModel):
    """
    Store information.The store has a url or filename from which the products will be loaded.
    """
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    def __str__(self):
        return self.name


class Category(TimeStampModel):
    """
    Categories of various products.
    """
    name = models.CharField(max_length=50, unique=True)
    shops = models.ManyToManyField(Shop, related_name='categories')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(TimeStampModel):
    """
    Product information. One product can belong to several categories or be uncategorized.
    """
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    model = models.CharField(max_length=100, blank=True)
    price_rrc = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='recommended price')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-name',)
        constraints = [
            models.CheckConstraint(check=models.Q(price_rrc__gt=0), name='price_rrc_is_positive'),
        ]

    def __str__(self):
        return f'{self.name}, {self.model}'


class ProductInfo(TimeStampModel):
    """
    Information about a product in a particular store.
    """
    external_id = models.PositiveIntegerField()
    product = models.ForeignKey(Product, verbose_name='Product', related_name='product_infos', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='product_detail', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Product Information'
        verbose_name_plural = 'Products information'
        constraints = [
            models.CheckConstraint(check=models.Q(price__gt=0), name='price_is_positive'),
            models.UniqueConstraint(fields=['shop', 'external_id'], name='unique_product_info')
        ]


class Parameter(models.Model):
    """
    Ability to add custom fields (characteristics) of products.
    """
    name = models.CharField(max_length=50, verbose_name='parameter', unique=True)

    class Meta:
        verbose_name = 'Name parameter'
        verbose_name_plural = 'Names parameters'


class ProductParameter(models.Model):
    """
    The value of the product parameter, does not depend on the store (the same for all stores).
    """
    product = models.ForeignKey(Product, related_name='product_parameters', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='+', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Product parameter'
        verbose_name_plural = " List parameters"
        constraints = [
            models.UniqueConstraint(fields=['product', 'parameter'], name='unique_product_parameter'),
        ]


class Order(TimeStampModel):
    """
    Simple order form, has a number, order status and delivery date.
    """
    class StatusChoices(models.TextChoices):

        NOT_DELIVERED = 'not_delivered', 'Not delivered'
        DELIVERED = 'delivered', 'Delivered'

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.NOT_DELIVERED)
    number = models.IntegerField(max_length=10)
    delivered_at = models.DateTimeField(blank=True, null=True)


class OrderItem(models.Model):
    """
    Quantity of the product in the order.
    """
    order = models.ForeignKey(Order, related_name='ordered_items',on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_info', 'order'], name='unique_order_product_info'),
            models.CheckConstraint(check=models.Q(quantity__gt=1), name='check_quantity'),
        ]

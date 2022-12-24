from uuid import uuid4

from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
# Create your models here.
from django.utils.text import slugify

from store.validators import validate_file_size


class Collection(models.Model):
    title = models.CharField(max_length=225)
    feature_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Customer(models.Model):
    # first_name = models.CharField(max_length=225)
    # last_name = models.CharField(max_length=225)
    email = models.EmailField()
    phone = models.CharField(max_length=225, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Product(models.Model):
    slug = models.SlugField(null=True)
    name = models.CharField(max_length=225, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='store/images',
        validators=[validate_file_size])


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'delivered'),
    )
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('Failed', 'Failed')
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=225, choices=STATUS, default='Pending')
    payment_status = models.CharField(max_length=225, choices=PAYMENT_STATUS, default='Pending')

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    number = models.PositiveIntegerField()
    street = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    state = models.CharField(max_length=225)
    country = models.CharField(max_length=225)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    zipcode = models.CharField(max_length=5)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    date_created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=225)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

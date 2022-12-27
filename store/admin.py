from django.contrib import messages
from django.utils.html import format_html

from .models import *


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'orders', 'date_created']
    list_editable = ['phone']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['name__istartswith']
    search_help_text = 'What are you looking for'
    date_hierarchy = 'date_created'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['items', 'date_created']
    list_per_page = 10


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['name', 'price', 'inventory_status', 'collection_title']
    list_editable = ['price']
    list_filter = ['collection', 'date_added']
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Product is getting low'
        return 'OK'

    @admin.action(description='Clear_inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

    class Media:
        css = {
            'all': ['store/styles2.css']
        }


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['feature_product']
    list_display = ['title', 'products_count']
    search_fields = ['title']

    def products_count(self):
        return self.products.count()

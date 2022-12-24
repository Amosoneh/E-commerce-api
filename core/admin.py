from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from store.admin import ProductAdmin, ProductImageInline
from store.models import Product
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
        }),
    )


# admin.site.register(User, UserAdmin)
class CustomProductAdmin(ProductAdmin):
    inlines = [ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

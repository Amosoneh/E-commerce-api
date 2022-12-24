from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('carts', views.CartViewSet, basename='cart')
router.register('products', views.ProductViewSet, basename='product')
router.register('orders', views.OrderViewSet, basename='order')
router.register('collections', views.CollectionViewSet, basename='collection')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items-detail')

urlpatterns = router.urls + carts_router.urls + products_router.urls

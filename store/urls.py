from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet,\
    ReviewViewSet,CartViewSet,CartItemViewSet,CustomerViewset, OrderViewSet

router = routers.DefaultRouter()
router.register("products",viewset=ProductViewSet,basename="products")
router.register("collections",viewset=CollectionViewSet)
router.register('carts',viewset=CartViewSet)
router.register('customers',viewset=CustomerViewset)
router.register('orders',viewset=OrderViewSet,basename='orders')

products_router = routers.NestedDefaultRouter(router,'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router,"carts",lookup="cart")
carts_router.register("items",viewset=CartItemViewSet,basename="cart-items")

urlpatterns = router.urls + products_router.urls + carts_router.urls

# if we have specific patterns we need to include
'''
urlpatterns = [
path("",include(router.urls)),
path("other patterns", ..)
]
'''
from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register("products",viewset=ProductViewSet,basename="products")
router.register("collections",viewset=CollectionViewSet)

products_router = routers.NestedDefaultRouter(router,'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')
urlpatterns = router.urls + products_router.urls

# if we have specific patterns we need to include
'''
urlpatterns = [
path("",include(router.urls)),
path("other patterns", ..)
]
'''
from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from .views import ProductViewSet, CollectionViewSet

router = DefaultRouter() # SimpleRouter
router.register("products",viewset=ProductViewSet)
router.register("collections",viewset=CollectionViewSet)

urlpatterns = router.urls

# if we have specific patterns we need to include
'''
urlpatterns = [
path("",include(router.urls)),
path("other patterns", ..)
]
'''
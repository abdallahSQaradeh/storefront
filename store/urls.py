from django.urls import path
from .views import \
ProductDetail,ProductList, \
collection_detail, \
CollectionList

urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/<int:id>/", ProductDetail.as_view()),
     path('collections/', 
         CollectionList.as_view(),
         name='collection-list'),
    path('collections/<int:pk>', 
         collection_detail,
         name='collection-detail')
]
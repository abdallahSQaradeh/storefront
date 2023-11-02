from django.urls import path
from .views import \
ProductDetail,ProductList, \
collection_detail, \
collection_list

urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/<int:id>/", ProductDetail.as_view()),
     path('collections/', 
         collection_list,
         name='collection-list'),
    path('collections/<int:pk>', 
         collection_detail,
         name='collection-detail')
]
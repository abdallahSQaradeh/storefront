from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Product,Collection,OrderItem
from .serializers import ProductSerializer,CollectionSeralizer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request":self.request}
    
    def destroy(self, request, *args, **kwargs):
        '''
        the destroy method itself retrieve the object from the db to delete it  
        '''
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':"Product cannot be deleted because it is associated with order item"}
                        ,status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# for retreive only view sets (get item and get list) use ReadOnlyModelViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products'))
    serializer_class = CollectionSeralizer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
            return Response({ "error":" cannot delete the collection because it has products"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)





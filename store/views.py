from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSeralizer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field ='id'
    
        
    def delete(self,request,id):
        product = get_object_or_404(Product,pk=id)
        if product.orderitems.count() > 0:
            return Response({'error':"Product cannot be deleted because it is associated with order item"}
                            ,status = status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {"request":self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products'))
    serializer_class = CollectionSeralizer

    def delete(self, request, pk):
        collection =get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk=pk)
        if collection.products.count() > 0:
            return Response({ "error":" cannot delete the collection because it has products"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)        


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count("products")).all()
    serializer_class = CollectionSeralizer

    def get_serializer_context(self):
        return {'request':self.request}



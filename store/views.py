from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSeralizer

class ProductDetail(APIView):
    def get(self, request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request,id):
        product = get_object_or_404(Product,pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request,id):
        product = get_object_or_404(Product,pk=id)
        if product.orderitems.count() > 0:
            return Response({'error':"Product cannot be deleted because it is associated with order item"}
                            ,status = status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serialzer = ProductSerializer(queryset, many=True,context={'request':request})
        return Response(serialzer.data)
    def post(self,request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count = Count('products')),pk=pk)
    if request.method == 'GET':
        serializer = CollectionSeralizer(collection)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = CollectionSeralizer(instance=collection,
                                         data = request.data)
        serializer.save()
        return Response(serializer.data,status = status.HTTP_200_OK)
    elif request.method =='DELETE':
        if collection.products.count() > 0:
            return Response({ "error":" cannot delete the collection because it has products"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method =='GET':
        queryset = Collection.objects.all()
        serializer = CollectionSeralizer(queryset, many=True)
        return Response(serializer.data)
    elif request.method =='POST':
        serializer = CollectionSeralizer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
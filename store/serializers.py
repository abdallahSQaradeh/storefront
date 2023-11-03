from decimal import Decimal
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Product, Collection,Review


class CollectionSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.SerializerMethodField(method_name='calculate_products_count')
    
    def calculate_products_count(self, collection:Collection):
        return collection.products.count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'inventory',
            'price',
            'price_with_tax',
            'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length =255)
    price = serializers.DecimalField( source="unit_price" ,max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # # collection = serializers.PrimaryKeyRelatedField(queryset =Collection.objects.all()  )
    # # collection = serializers.StringRelatedField() must select_related
    # # collection = CollectionSeralizer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1) 
    
    # def validate(self, attrs):
    #     if attrs['unit_price'] < 0:
    #         return ValidationError("Price shouldn't be smaller than zero")
    #     return True

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 2 # added field
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id,**validated_data)

        
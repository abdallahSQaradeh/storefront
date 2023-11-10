from decimal import Decimal
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Product, Collection,Review,Cart,CartItem,Customer


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

class CartItemProductSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product =CartItemProductSerailizer()
    total_price= serializers.SerializerMethodField(method_name='calculate_total_price')
    

    def calculate_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price


    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many=True,read_only = True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart:Cart):
        dir(cart)
        total_price = sum([item.quantity * item.product.unit_price for item in cart.items.all()])
        return total_price

    class Meta:
        model = Cart
        fields = ['id','items','total_price']
       
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(pk= product_id).exists():
            raise ValidationError("No product with the given id was found ")
        return product_id

    '''
    because when we add the same product to the item we don't wan't to add
    the product, but we do need to update the quantity of the item
    so we cannot rely on the default save method from the ModelSerializer
    '''
    def save(self, **kwargs):
        self.is_valid(raise_exception=True)
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context.get('cart_id')
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance =cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id,
                                                **self.validated_data)
        return self.instance


    class Meta:
        model =CartItem
        fields = ['id','product_id','quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    '''Even though we have the user_id in the model, but we cannot see it in the endpoint cause it is created 
    at the run time, so we need to add to the serializer'''
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date','membership']
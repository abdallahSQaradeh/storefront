from django.contrib import admin
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',
                                          on_delete=models.SET_NULL,
                                            null=True,
                                            related_name="+") 
    ''' this create circular dpendency cause django will create another collection variable in the Product 
    class, to work around it we can specify the related name to be "+" to prevent django from creating the
    reverse relationship
    '''
    def __str__(self):
        return self.title + f'- {self.id}'
    
    class Meta:
        ordering =['title']
    
class Promotion(models.Model): 
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #product_set, default relation name

class Product(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255) #varchar(255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(0)]) #9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='products')
    promotions = models.ManyToManyField(Promotion
                                        #, related_name="productts"
                                        )
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'

    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    '''
    class Meta:
        ordering =["-email"]
        db_table = "store_customers"
        indexes = [models.Index(fields=['last_name','first_name'])]
    '''    

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name','user__last_name']
        permissions = [
            ('view_history','Can view history')
        ] # this needs migrations, and it's not recommended to add specific permission via the model
        # it will be reflected in the auth_permissions table


class Order(models.Model):
    PAYMENT_STATUS=[
        ('P','Pending'),
        ('C','Completed'),
        ('F','Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


    class Meta:
        # permissions = [ (codename, description)]
        permissions = [ ('cacel_order','Can cancel order') ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # place the price of the product at the time the item is ordered

class Address(models.Model):
    street = models.CharField(max_length=255)
    cirty = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) # one address for each customer 

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    # we shouldn't call the uuid4, since it will be hardcoded to the migrations
    # and will be the default for all carts
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)]) 

    class Meta:
        unique_together = [['cart','product']]

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
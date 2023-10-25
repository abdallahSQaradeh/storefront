from django.db import models

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)

class Promotion(models.Model): 
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    #product_set, default relation name

class Product(models.Model):
    title = models.CharField(max_length=255) #varchar(255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=6) #9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion
                                        #, related_name="productts"
                                        )

class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'

    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email = models.DateField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

class Order(models.Model):
    PAYMENT_STATUS=[
        ('P','Pending'),
        ('C','Completed'),
        ('F','Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # place the price of the product at the time the item is ordered

class Address(models.Model):
    street = models.CharField(max_length=255)
    cirty = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) # one address for each customer 

class Cart(models.Model):
    created_At = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField() 
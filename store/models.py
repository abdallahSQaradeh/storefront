from django.db import models

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
    description = models.TextField()
    unit_price = models.DecimalField(decimal_places=2,max_digits=6) #9999.99
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT)
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
    first_name = models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    '''
    class Meta:
        ordering =["-email"]
        db_table = "store_customers"
        indexes = [models.Index(fields=['last_name','first_name'])]
    '''    

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name','last_name']


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
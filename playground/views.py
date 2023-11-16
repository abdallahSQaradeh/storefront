from django.shortcuts import render
from django.core.mail import send_mail,mail_admins,BadHeaderError
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.db.models.aggregates import Avg,Sum,Max,Count,Min 
from django.contrib.contenttypes.models import ContentType # represents the django_content_type table
from store.models import Product, Order,Collection
from store.models import OrderItem
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):
    try:
        send_mail("Test Email","hello from me",recipient_list=["a@q.c"],fail_silently=False,from_email="from@me.com",)
    except BadHeaderError:
        return HttpResponse("You are using fake emails headers")

    products = Product.objects.filter(last_update__year=2021)
    queryset = Product.objects.filter(Q(inventory__lt=10)& Q(unit_price__lt=20))
    # Q object are preferable when it comes to OR operator
    # otherwise we can use .filter(...).filter() \ .filter(field1, filed2)
    '''
    F object is to reference a particular field in the table or in the reference table
    e.g: .filter(inventory=F("collection__id"))
    '''
    f_queryset = Product.objects.filter(inventory=F('unit_price'))
    sorted = Product.objects.order_by('unit_price','-title')
    # earliest , latest similar to order_by()[0]
    fields_values = OrderItem.objects.values('product__id').distinct()
    # list the poducts that have been ordered
    products_ordered = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by("title")
    return render(request,'hello.html',{'name':'Abdallah','products':products_ordered}) 

def orders_customers_items(request):
    '''Get the last 5 orders with their customer and items (include product)'''
    queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-palced_at')[:5]

    return render(request, 'hello.html',{'result':queryset})

def aggregaetes(request):
    result = Product.objects.aggregate(count =Count('id'), min_price = Min('unit_price'))

def querying_generic_realtionships(request):
    # this will get the content type id for the Product model from the django_contetnt_type
    queryset = TaggedItem.objects.get_tags_for(Product,1)
       
    return render(request, 'hello.html',{'result':list(queryset)})

def create_object(request):
    colleaction = Collection()
    colleaction.title ='Video games'
    colleaction.featured_product_id=1
    colleaction.save()
    return render(request, 'hello.html',{})

def update_object(request):
    colleaction = Collection.objects.filter(pk=11).update(featured_product=None)
    colleaction.save()
    return render(request, 'hello.html',{})
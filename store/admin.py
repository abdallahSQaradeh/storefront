from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'unit_price',
        'inventory_status',
        'collection' # will display the string repesentation
        # to get a specific property from the related model,
        #  we can define a method. .g collection_title
        ,'collection_title'
        ]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection'] # this to enhance the query and prevent django from 
    # having a query for each product
    
    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        return 'ok'
    
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count = Count('product') )



# Register your models here.
#admin.site.register(models.Collection)
# admin.site.register(models.Product)
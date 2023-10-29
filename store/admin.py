from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models



class InventoryFilter(admin.SimpleListFilter):
    title = "inventory" # appears after by
    parameter_name = "inventory" # will be used in the query string

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [ 
            ('<10','low')
        ] # each tuple represnts one of the filters
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        # self.value() return the selected filter
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug':['title']
    }
    #fields,exclude,readonly_fields
    autocomplete_fields=['collection']
    search_fields = ['title']
    list_display = [
        'title',
        'unit_price',
        'inventory_status',
        'collection' # will display the string repesentation
        # to get a specific property from the related model,
        #  we can define a method. .g collection_title
        ,'collection_title'
        ]
    actions = ['clear_inventory']
    list_filter = ['collection','last_update',InventoryFilter]
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
    
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,
                           f'{updated_count} Products were succefully updated',
                           messages.SUCCESS
                           )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith','last_name__istartswith']
    

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = ( 
            reverse("admin:store_order_changelist" ) 
            + '?'
            + urlencode({
                'customer__id':customer.id
            })
        )
        return format_html('<a href={}>{}</a>',url,customer.orders_count) 

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(orders_count = Count('order'))

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num =1 # must add at least one order item
    max_num = 10 
    autocomplete_fields = ['product']

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    autocomplete_fields = [ 'customer' ]
    inlines = [ OrderItemInline]
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        #reverse('admin: app_model_page')
        url = (
            reverse("admin:store_product_changelist")
              + '?'
              + urlencode({
                  'collection__id': collection.id
              }) 
               )
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count = Count('product') )



# Register your models here.
#admin.site.register(models.Collection)
# admin.site.register(models.Product)
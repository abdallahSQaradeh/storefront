from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin, UpdateModelMixin,DestroyModelMixin
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticated,IsAdminUser,DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,Collection,OrderItem,\
    Review,Cart, CartItem, Customer, Order
from .serializers import CreateOrderSerializer, OrderSerializer, ProductSerializer,CollectionSeralizer, \
    ReviewSerializer,CartSerializer,CartItemSerializer,\
          AddCartItemSerializer, UpdateCartItemSerializer,\
          CustomerSerializer, UpdateOrderSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly,FullDjangoModelPermissions,CustomerHistoryPermission

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['collection_id']
    search_fields = ['title','description']
    ordering_fields =  ['unit_price','last_update']
    

    '''we use the context object to provide the serializer with more data'''
    def get_serializer_context(self):
        return {"request":self.request}

    def destroy(self, request, *args, **kwargs):
        '''
        the destroy method itself retrieve the object from the db to delete it  
        '''
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':"Product cannot be deleted because it is associated with order item"}
                        ,status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# for retreive only view sets (get item and get list) use ReadOnlyModelViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products'))
    serializer_class = CollectionSeralizer
    permission_classes=[IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count()>0:
            return Response({ "error":" cannot delete the collection because it has products"},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() this will return all the reviews regardless the product id
    # we need to override the get_queryset
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        '''our url has two ids, product_pk and pk'''
        return {'product_id':self.kwargs['product_pk']}
    
    def get_queryset(self):
        return Review.objects.filter(product_id =self.kwargs['product_pk'] )
    

class CartViewSet(CreateModelMixin,
                 RetrieveModelMixin,
                 DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)

class CartItemViewSet(ModelViewSet):
    http_method_names =[ 'post','patch','delete','get']
    def get_serializer_class(self):
        '''
        we need to override the class serializer, in order to pass
        desired data and not all the data in the prev serializer
        '''
        if self.request.method =='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id =self.kwargs['cart_pk'])
    
class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser,FullDjangoModelPermissions]

    '''all the methods that responding to requests called actions,
    such as the create and retrieve methods from the above mixins'''
    @action(detail=False, methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    # also we can add permission_classes to this decorator
    # detail=True - it will be available on /customers/{id}/me
    # detail = False - it will be available on /customers/me
    def me(self,request:Request):
        (customer,created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method =='GET':    
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method =='PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
    @action(detail=True, permission_classes=[CustomerHistoryPermission])
    def history(self,request,pk):
        return Response("Hist")
    

class OrderViewSet(ModelViewSet):
    '''we need only the admin user to delete or update the order'''
    http_method_names = ['get','patch','delete','head','options']
    
    def get_permissions(self):
        if self.request.method in ['PUT','PATCH','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data = request.data,context={'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method =='POST':
            return CreateOrderSerializer
        elif self.request.method =='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        # we are breaking the command query seperation by creating and retrieving at the same time
        (customer_id,createed) = Customer.objects.only('id').get_or_create(user_id = user.id)
        queryset = Order.objects.filter(customer_id = customer_id )
        return queryset
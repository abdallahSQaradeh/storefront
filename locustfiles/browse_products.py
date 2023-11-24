from locust import HttpUser, between,task
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1,5) # gonna randomly wait 1,5 seconds before performing the tasks

    @task(2) # weight 2
    def view_products(self):
        print("View products")
        collection_id = randint(2,6)
        self.client.get(f"/store/products/?collection_id={collection_id}", name="/store/products")
    
    @task(4) # the user is twice more probably to do this task
    def view_product(self):
        print("View product")        
        product_id = randint(1,1000)
        self.client.get(f'/store/products/{product_id}',
                        name="/store/products/:id")
    @task(1)
    def add_to_cart(self):
        print("Add to cart")
        product_id = randint(1,10)
        self.client.post(
            f'/store/carts/{self.cart_id}/items/',
            name="/store/carts/items",
            json={'product_id':product_id, 'quantity':1}
        )

    def on_start(self):# gets called every time a new user start browsing our website
        print("On Start")        
        response = self.client.post(f'/store/carts/')
        result = response.json()
        self.cart_id = result['id']


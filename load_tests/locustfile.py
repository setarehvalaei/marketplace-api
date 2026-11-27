
from locust import HttpUser, task, between


class MarketplaceUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_products(self):
        self.client.get("/products", name="GET /products")

    @task
    def get_best_selling_products(self):
        self.client.get("/products/best-selling", name="GET /products/best-selling")

    @task
    def get_product(self):
        self.client.get("/products/1", name="GET /products/{product_id}")

    @task
    def get_vendors(self):
        self.client.get("/vendors", name="GET /vendors")

    @task
    def get_popular_vendors(self):
        self.client.get("/vendors/popular", name="GET /vendors/popular")

    @task
    def get_vendor_products(self):
        self.client.get("/vendors/1/products", name="GET /vendors/{vendor_id}/products")

    @task
    def get_cart(self):
        self.client.get("/cart", name="GET /cart")

    @task
    def get_orders(self):
        self.client.get("/orders", name="GET /orders")




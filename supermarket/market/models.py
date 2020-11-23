from django.db import models

# Create your models here.

class Product(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    def increase_inventory(self, amount):
        pass

    def decrease_inventory(self, amount):
        pass

class Customer(models.Model):
    user = None
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.IntegerField()

    def deposit(self, amount):
        pass

    def spend(self, amount):
        pass


class OrderRow(models.Model):
    product = None
    order = None
    amount = models.IntegerField()


class Order(models.Model):
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()
    status = None

    @staticmethod
    def initiate(customer):
        pass

    def add_product(self, product, amount):
        pass

    def remove_product(self, product, amount=None):
        pass

    def submit(self):
        pass

    def cancel(self):
        pass

    def send(self):
        pass

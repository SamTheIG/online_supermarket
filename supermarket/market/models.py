from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    def increase_inventory(self, amount):
        self.inventory += amount
        self.save()

    def decrease_inventory(self, amount):
        if self.inventory < amount:
            raise Exception('The Min of inventory is 0')
        else:
            self.inventory -= amount
            self.save()

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.IntegerField(default=20000)

    def __str__(self):
        name = self.user.username
        return name
        
    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            raise Exception('The Min of balance is 0')
        else:
            self.balance -= amount
            self.save()


class OrderRow(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='rows')
    amount = models.IntegerField()


class Order(models.Model):
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    order_time = models.DateTimeField()
    total_price = models.IntegerField()
    status = models.IntegerField()

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

from django.db import models

from django.contrib.auth.models import User
from datetime import datetime


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    balance = models.PositiveIntegerField(default=20000)

    def __str__(self):
        return self.user.username

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
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="rows")
    amount = models.PositiveIntegerField()


class Order(models.Model):
    # Status values. DO NOT EDIT
    STATUS_SHOPPING = 1
    STATUS_SUBMITTED = 2
    STATUS_CANCELED = 3
    STATUS_SENT = 4
    status = (
        (STATUS_SHOPPING, 'در حال خرید'),
        (STATUS_SUBMITTED, 'ثبت‌شده'),
        (STATUS_CANCELED, 'لغوشده'),
        (STATUS_SENT, 'ارسال‌شده')
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    order_time = models.DateTimeField(default=datetime.now())
    total_price = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=status)

    def __str__(self):
        return self.customer.user.username

    @staticmethod
    def initiate(customer):
        n = Order.objects.filter(customer=customer).count()
        if n == 0:
            o = Order(customer=customer, status=1)
            o.save()
        else:
            lst = Order.objects.all()
            count = 0
            while True:
                n1 = lst[count]
                if n1.status == 1:
                    o = n1
                    break
                count += 1
                if count == n:
                    o = Order(customer=customer, status=1)
                    o.save()
                    break
        return o

    def add_product(self, product, amount):
        if amount == 0:
            raise Exception('The amount can not be 0')
        elif amount > product.inventory:
            raise Exception('you can not add a product more than it inventory')
        else:
            a1 = OrderRow.objects.filter(product=product, order=self)
            if list(a1) == []:
                or1 = OrderRow(product=product, order=self, amount=amount)
                or1.save()
                price = product.price
                order_price = amount * price
                self.total_price += order_price
                self.save()
            else:
                or1 = a1[0]
                or1.amount += amount
                or1.save()
                price = product.price
                order_price = amount * price
                self.total_price += order_price
                self.save()

    def remove_product(self, product, amount=None):
        a1 = OrderRow.objects.filter(product=product, order=self)
        if list(a1) == []:
            raise Exception('This OrderRow does not exist')
        else:
            or1 = a1[0]
            if amount == None:
                price = product.price
                order_price = or1.amount * price
                or1.delete()
                self.total_price -= order_price
                self.save()
            else:
                or1.amount -= amount
                or1.save()
                price = product.price
                order_price = amount * price
                self.total_price -= order_price
                self.save()

    def submit(self):
        if self.status == 1:
            or1 = OrderRow.objects.filter(order=self)
            if len(or1) != 0:
                for item in or1:
                    p1 = Product.objects.filter(name=item.product)[0]
                    p1_price = p1.price * item.amount
                    self.total_price += p1_price
                    if p1.inventory < item.amount:
                        raise Exception('you can not add a product with amount more than the inventory')
                    else:
                        p1.decrease_inventory(item.amount)
                        p1.save()

                    c1 = self.customer
                    if c1.balance < p1_price:
                        raise Exception('you can not add a product with price more than your balance')

                    elif c1.balance < self.total_price:
                        raise Exception('Your balance is less then total price')
                    else:
                        c1.spend(p1_price)
                        c1.save()
                self.status = 2
                self.order_time = datetime.now()
                self.save()
            else:
                raise Exception('you cant submit empty order')
        else:
            raise Exception('you cant submit order that is not shopping')
    def cancel(self):
        if self.status == 2:
            or1 = OrderRow.objects.filter(order=self)
            for item in or1:
                p1 = Product.objects.filter(name=item.product)[0]
                p1_price = p1.price * item.amount
                p1.increase_inventory(item.amount)
                p1.save()

                c1 = self.customer
                c1.deposit(p1_price)
                c1.save()
            self.status = 3
            self.total_price = 0
            self.save()
        else:
            raise Exception('you do not have a SUBMITTED order to cancel')

    def send(self):
        if self.status == 2:
            self.status = 4
        else:
            raise Exception('you can not SEND a non SUBMITTED order')

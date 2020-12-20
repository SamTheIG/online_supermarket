from django.db import models



from django.contrib.auth.models import User



import datetime





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

    balance = models.PositiveIntegerField(default=20000)



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

    order_time = models.DateTimeField(default=datetime.datetime.now)

    total_price = models.IntegerField(null=True)

    status = models.IntegerField()

    def __unicode__(self):
        return self.customer


    @staticmethod

    def initiate(customer):
        n = len(list(Order.objects.all()))
        if n == 0:
            o = Order()
            o.order_time = datetime.datetime.now()
            o.customer = customer
            o.status = 1
            o.save()
        else:
            count = 0
            for item in list(Order.objects.all()):
                if item.status == 1:
                    o = item
                    break
                count += 1
            if count == len(list(Order.objects.all())) - 1:
                o = Order()
                o.order_time = datetime.datetime.now()
                o.customer = customer
                o.status = 1
                o.save()
        return o



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



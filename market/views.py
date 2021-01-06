from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import json
from django.contrib.auth.models import User
from .models import *
"""
    You can define utility functions here if needed
    For example, a function to create a JsonResponse
    with a specified status code or a message, etc.

    DO NOT FORGET to complete url patterns in market/urls.py
"""


def product_insert(request):
    if request.method != 'POST':
        data = {"message": "Wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)

    if request.method == 'POST':
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        p = Product.objects.all()
        pcode = data_raw["code"]
        for item in p:
            if item.code == pcode:
                data = {"message": "Duplicate code"}
                return JsonResponse(data, status=400)
                break
        pname = data_raw["name"]
        pprice = data_raw["price"]
        if pprice < 0:
            data = {"message": "Wrong type of price"}
            return JsonResponse(data, status=400)
        if data_raw.get("inventory") == None:
            pinventory = 0
        else:
            pinventory = data_raw["inventory"]
        p1 = Product()
        p1.code = pcode
        p1.name = pname
        p1.price = pprice
        p1.inventory = pinventory
        p1.save()
        num = p1.id
        data = {"id": num}
        return JsonResponse(data, status=201)


def product_list(request):
    if request.method != 'GET':
        data = {"message": "wrong type of request (must be get)"}
        return JsonResponse(data, status=400)
    if request.method == 'GET':
        r = request.GET.get('search')
        if r == None:
            products = Product.objects.all()
            data = {"products": list(products.values("code", "name", "price", "inventory"))}
            return JsonResponse(data, status=200)
        else:
            products = Product.objects.filter(name__contains = r)
            data = {"products": list(products.values("code", "name", "price", "inventory"))}
            return JsonResponse(data, status=200)


def product_details(request, product_id):
    if request.method != 'GET':
        data = {"message": "Wrong type of request(must be GET)"}
        return JsonResponse(data, status=400)
    if request.method == 'GET':
        a = Product.objects.filter(id = product_id)
        b = list(a)
        if b == []:
            data = {"message": "Product Not Found."}
            return JsonResponse(data, status=404)
        else:
            c = b[0]
            data = {"id": c.id, "code": c.code, "name": c.name, "price": c.price, "inventory": c.inventory}
            return JsonResponse(data, status=200)


def product_edit(request, product_id):
    if request.method != 'POST':
        data = {"message": "Wrong type of request(must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        a = Product.objects.filter(id = product_id)
        b = list(a)
        if b == []:
            data = {"message": "Product Not Found."}
            return JsonResponse(data, status=404)
        else:
            p = b[0]
            data_raw = request.body.decode('utf-8')
            data_raw = json.loads(data_raw)
            if data_raw.get("amount") == None:
                data = {"message": "wtf man there is no amount here!"}
                return JsonResponse(data, status=400)
            else:
                pamount = data_raw["amount"]
            try:
                pamount = int(pamount)
            except:
                data = {"message": "wtf that was not an integer!"}
                return JsonResponse(data, status=400)
            if pamount < 0:
                pamount = -pamount
                if p.inventory < pamount:
                    data = {"message": "Not enough inventory"}
                    return JsonResponse(data, status=400)
                else:
                    p.inventory -= pamount
                    p.save()
            else:
                p.inventory += pamount
                p.save()
            data = {"id": p.id, "code": p.code, "name": p.name, "price": p.price, "inventory": p.inventory}
            return JsonResponse(data, status=200)


def customer_register(request):
    # todo: test the register
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        cusername = data_raw["username"]
        from django.contrib.auth.models import User
        U = User.objects.all()
        u = User()
        u.username = cusername
        for item in U:
            if item.username == cusername:
                data = {"message": "Username already exists"}
                return JsonResponse(data, status=400)
        cfirst_name = data_raw["first_name"]
        u.first_name = cfirst_name
        clast_name = data_raw["last_name"]
        u.last_name = clast_name
        cemail = data_raw["email"]
        u.email = cemail
        cpassword = data_raw["password"]
        u.password = cpassword
        u.save()
        c1 = Customer()
        c1.user = u
        cphone = data_raw["phone"]
        c1.phone = cphone
        caddress = data_raw["address"]
        c1.address = caddress
        try:
            c1.save()
        except:
            data = {"message": "F me man"}
            return JsonResponse(data, status=400)
        num = c1.id
        data = {"id": num}
        return JsonResponse(data, status=201)


def customer_list(request):
    if request.method != 'GET':
        data = {"message": "wrong type of request (must be get)"}
        return JsonResponse(data, status=400)
    if request.method == 'GET':
        r = request.GET.get('search')
        if r == None:
            custo = list()
            customers = Customer.objects.all()
            for item in customers:
                cid = item.id
                cusername = item.user.username
                cfirst_name = item.user.first_name
                clast_name = item.user.last_name
                cemail = item.user.email
                cphone = item.phone
                caddress = item.address
                cbalance = item.balance
                data0 ={
                "id": cid,
                "username": cusername,
                "first_name": cfirst_name,
                "last_name": clast_name,
                "email": cemail,
                "phone": cphone,
                "address": caddress,
                "balance": cbalance
                }
                custo.append(data0)
            data = {"customers": custo}
            return JsonResponse(data, status=200)
        else:
            custo = list()
            customers = Customer.objects.all()
            for item in customers:
                cid = item.id
                cusername = item.user.username
                cfirst_name = item.user.first_name
                clast_name = item.user.last_name
                cemail = item.user.email
                cphone = item.phone
                caddress = item.address
                cbalance = item.balance
                data0 = {
                    "id": cid,
                    "username": cusername,
                    "first_name": cfirst_name,
                    "last_name": clast_name,
                    "email": cemail,
                    "phone": cphone,
                    "address": caddress,
                    "balance": cbalance
                        }
                custo.append(data0)
            custo1 = list()
            for item in custo:
                r1 = item["username"].lower().find(r.lower())
                r2 = item["first_name"].lower().find(r.lower())
                r3 = item["last_name"].lower().find(r.lower())
                r4 = item["address"].lower().find(r.lower())
                if r1 != -1:
                    custo1.append(item)
                    break
                if r2 != -1:
                    custo1.append(item)
                    break
                if r3 != -1:
                    custo1.append(item)
                    break
                if r4 != -1:
                    custo1.append(item)
                    break
            data = {"customers": custo1}
            return JsonResponse(data, status=200)


def customer_details(request, customer_id):
    if request.method != 'GET':
        data = {"message": "wrong type of request (must be GET)"}
        return JsonResponse(data, status=400)
    if request.method == 'GET':
        customer = Customer.objects.filter(id=customer_id)
        if list(customer) == []:
            data = {"message": "Customer Not Found."}
            return JsonResponse(data, status=404)
        customer = customer[0]
        cid = customer.id
        cusername = customer.user.username
        cfirst_name = customer.user.first_name
        clast_name = customer.user.last_name
        cemail = customer.user.email
        cphone = customer.phone
        caddress = customer.address
        cbalance = customer.balance
        data = {
            "id": cid,
            "username": cusername,
            "first_name": cfirst_name,
            "last_name": clast_name,
            "email": cemail,
            "phone": cphone,
            "address": caddress,
            "balance": cbalance
        }
        return JsonResponse(data, status=200)


def customer_edit(request, customer_id):
    # todo: fix the bug in editing profile
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        customer = Customer.objects.filter(id=customer_id)
        if list(customer) == []:
            data = {"message": "Customer Not Found."}
            return JsonResponse(data, status=404)
        customer = customer[0]
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        if data_raw.get("id") != None:
            data = {"message": "Cannot edit customers indentity and credentials"}
            return JsonResponse(data, status=403)
        if data_raw.get("username") != None:
            data = {"message": "Cannot edit customers indentity and credentials"}
            return JsonResponse(data, status=403)
        if data_raw.get("password") != None:
            data = {"message": "Cannot edit customers indentity and credentials"}
            return JsonResponse(data, status=403)
        if data_raw.get("first_name") != None:
            u = customer.user
            u.first_name = data_raw["first_name"]
            u.save()
        if data_raw.get("last_name") != None:
            u = customer.user
            u.last_name = data_raw["last_name"]
            u.save()
        if data_raw.get("email") != None:
            u = customer.user
            u.email = data_raw["email"]
            u.save()
        if data_raw.get("phone") != None:
            customer.phone = data_raw["phone"]
            customer.save()
        if data_raw.get("address") != None:
            customer.address = data_raw["address"]
            customer.save()
        if data_raw.get("balance") != None:
            customer.balance = data_raw["balance"]
            customer.save()
        # customer = Customer.objects.filter(id=customer_id)
        # customer = customer[0]
        cid = customer.id
        cusername = customer.user.username
        cfirst_name = customer.user.first_name
        clast_name = customer.user.last_name
        cemail = customer.user.email
        cphone = customer.phone
        caddress = customer.address
        cbalance = customer.balance
        data = {
            "id": cid,
            "username": cusername,
            "first_name": cfirst_name,
            "last_name": clast_name,
            "email": cemail,
            "phone": cphone,
            "address": caddress,
            "balance": cbalance
        }
        return JsonResponse(data, status=200)


def customer_login(request):
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        cuser = data_raw.get("username")
        cpass = data_raw.get("password")
        if cuser is None:
            data = {"message": "no username found"}
            return JsonResponse(data, status=400)
        if cpass is None:
            data = {"message": "no password found"}
            return JsonResponse(data, status=400)
        C = Customer.objects.all()
        for item in C:
            u = item.user
            if u.username == cuser:
                if u.check_password(cpass):
                    data = {"message": "You are logged in successfully."}
                    request.session['customer_id'] = item.id
                    return JsonResponse(data, status=200)
                elif u.password == cpass:
                    data = {"message": "You are logged in successfully."}
                    request.session['customer_id'] = item.id
                    return JsonResponse(data, status=200)
                else:
                    data = {"message": "Password is incorrect."}
                    return JsonResponse(data, status=404)
            else:
                data = {"message": "Username is incorrect."}
                return JsonResponse(data, status=404)


def customer_logout(request):
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        C = Customer.objects.all()
        for item in C:
            try:
                if request.session['customer_id'] == item.id:
                    del request.session['customer_id']
                    data = {"message": "You are logged out successfully."}
                    return JsonResponse(data, status=200)
            except KeyError:
                pass
        data = {"message": "You are not logged in."}
        return JsonResponse(data, status=403)


def customer_profile(request):
    if request.method != 'GET':
        data = {"message": "wrong type of request (must be GET)"}
        return  JsonResponse(data, status=400)
    if request.method == 'GET':
        C = Customer.objects.all()
        for item in C:
            try:
                if request.session['customer_id'] == item.id:
                    u = item.user
                    data = {"id": item.id, "username": u.username, "first_name": u.first_name,
                            "last_name": u.last_name, "email": u.email, "phone": item.phone,
                            "address": item.address, "balance": item.balance}
                    return JsonResponse(data, status=200)
            except:
                data = {"message": "You are not logged in."}
                return JsonResponse(data, status=403)


def shopping_cart(request):
    if request.method != 'GET':
        data = {"message": "wrong type of request (must be GET)"}
        return JsonResponse(data, status=400)
    if request.method == 'GET':
        C = Customer.objects.all()
        for item in C:
            try:
                if request.session['customer_id'] == item.id:
                    o = Order.objects.filter(customer = item, status = 1)
                    o = o[0]
                    total_price = o.total_price
                    or1 = OrderRow.objects.filter(order = o)
                    if list(or1) is []:
                        data = {"total_price": total_price, "items": []}
                        return JsonResponse(data, status=200)
                    products = list()
                    for item in or1:
                        product = item.product
                        code = product.code
                        name = product.name
                        price = product.price
                        amount = item.amount
                        products.append({"code": code, "name": name, "price": price, "amount": amount})
                    data = {"total_price": total_price, "items": products}
                    return JsonResponse(data, status=200)
            except:
                data = {"message": "You are not logged in."}
                return JsonResponse(data, status=403)


def add_items(request):
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        errors = list()
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        C = Customer.objects.all()
        for item in C:
            try:
                assert request.session['customer_id'] == item.id
            except:
                data = {"message": "You are not logged in."}
                return JsonResponse(data, status=403)
            o = Order.objects.filter(customer = item, status = 1)
            o = o[0]
            for p in data_raw:
                code = p.get("code")
                amount = p.get("amount")
                product = Product.objects.filter(code = code)
                if product == []:
                    errors.append({"code": code, "message": "product not found"})
                else:
                    product = product[0]
                if amount > product.inventory:
                    errors.append({"code": code, "message": "not enough inventory"})
                o.add_product(product, amount)
                o.save()
            total_price = o.total_price
            or1 = OrderRow.objects.filter(order = o)
            products = list()
            for item in or1:
                product = item.product
                code = product.code
                name = product.name
                price = product.price
                amount = item.amount
                products.append({"code": code, "name": name, "price": price, "amount": amount})
            if len(errors) == 0:
                data = {"total_price": total_price, "items": products}
                return JsonResponse(data, statsu=200)
            else:
                data = {"total_price": total_price, "errors": errors, "items": products}
                return JsonResponse(data, status=400)


def remove_items(request):
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        errors = list()
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        C = Customer.objects.all()
        for item in C:
            try:
                assert request.session['customer_id'] == item.id
            except:
                data = {"message": "You are not logged in."}
                return JsonResponse(data, status=403)
            o = Order.objects.filter(customer = item, status = 1)
            o = o[0]
            for p in data_raw:
                code = p.get("code")
                amount = p.get("amount")
                product = Product.objects.filter(code = code)
                if product == []:
                    errors.append({"code": code, "message": "product not found"})
                else:
                    product = product[0]
                o.remove_product(product, amount)
                o.save()
                total_price = o.total_price
                or1 = OrderRow.objects.filter(order = o)
                products = list()
                for item in or1:
                    product = item.product
                    code = product.code
                    name = product.name
                    price = product.price
                    amount = item.amount
                    products.append({"code": code, "name": name, "price": price, "amount": amount})
                if len(errors) == 0:
                    data = {"total_price": total_price, "items": products}
                    return JsonResponse(data, statsu=200)
                else:
                    data = {"total_price": total_price, "errors": errors, "items": products}
                    return JsonResponse(data, status=400)


def submit(request):
    if request.method != 'POST':
        data = {"message": "wrong type of request (must be POST)"}
        return JsonResponse(data, status=400)
    if request.method == 'POST':
        errors = list()
        data_raw = request.body.decode('utf-8')
        data_raw = json.loads(data_raw)
        C = Customer.objects.all()
        for item in C:
            try:
                assert request.session['customer_id'] == item.id
            except:
                data = {"message": "You are not logged in."}
                return JsonResponse(data, status=403)
            o = Order.objects.filter(customer = item)
            try:
                o.submit()
            except Exception as e:
                print(str(e))
            return HttpResponse('fuck')

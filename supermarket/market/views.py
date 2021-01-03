from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

import json
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

def customer_insert(request):
    if request.method != 'POST':
        return HttpResponse('you need to request with POST method')
    elif request.method == 'POST':
        return HttpResponse('you asked to add a new customer')

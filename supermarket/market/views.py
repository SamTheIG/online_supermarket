from django.shortcuts import render, HttpResponse


"""
    You can define utility functions here if needed
    For example, a function to create a JsonResponse
    with a specified status code or a message, etc.

    DO NOT FORGET to complete url patterns in market/urls.py
"""



# Create your views here.
def product_insert(request):
    # hint: you should check request method like below
    if request.method != 'POST':
        return HttpResponse('you asked to add a new product')
        pass  # return appropriate error message
    pass  # main logic and return normal response

def product_list(request):
    if request.method == 'GET':
        return HttpResponse('you asked for the products list')

def customer_insert(request):
    if request.method != 'POST':
        return HttpResponse('you need to request with POST method')
    elif request.method == 'POST':
        return HttpResponse('you asked to add a new customer')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from products.models import *
from django.contrib.auth import logout, login, authenticate
import logging
from django.http import HttpResponse
from products.forms import RegisterForm, LoginForm

logger = logging.getLogger(__name__)

def product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #create empty cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products,'cartItems': cartItems}
    return render(request, 'product.html', context)


def index(request):
    context = {}
    return render(request, 'index.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #create empty cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,'cartItems': cartItems}
    return render(request, 'cart.html', context)




def check(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #create empty cart
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'check.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         total = float(data['form']['total'])
#         order.transaction_id = transaction_id
#
#         if total == order.get_cart_total:
#             order.complete =True
#         order.save()
#
#         if order.shipping == True:
#             Address.objects.create(
#                 customer=customer,
#                 order=order,
#                 address=data['shipping']['address'],
#                 city=data['shipping']['city'],
#                 state=data['shipping']['state'],
#                 zipcode=data['shipping']['zipcode'],
#             )
#
#     else:
#         print('User is not logged in')
#
#     return JsonResponse('Payment ok ', safe = False)

# @login_required
# def processOrder(request):
#     if request.user.is_authenticated:
#         transaction_id = datetime.datetime.now().timestamp()
#         data = json.loads(request.body)
#
#         customer = request.user.customer
#
#         try:
#             order = Order.objects.get(customer=customer, complete=False)
#             order.transaction_id = transaction_id
#         except Order.DoesNotExist:
#             order = Order.objects.create(customer=customer, transaction_id=transaction_id)
#
#         total = float(data['form']['total'])
#
#         if total == order.get_cart_total:
#             order.complete = True
#
#         order.save()
#
#         if order.shipping:
#             Address.objects.create(
#                 customer=customer,
#                 order=order,
#                 address=data['shipping']['address'],
#                 city=data['shipping']['city'],
#                 state=data['shipping']['state'],
#                 zipcode=data['shipping']['zipcode'],
#             )
#
#         return JsonResponse('Payment ok', safe=False)
#
#     return JsonResponse('User is not authenticated', status=400)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            Address.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                phone_number=data['shipping']['phone_number'],

            )

        if created:  # Проверяем, был ли заказ создан в этом запросе
            print('transaction_id:', transaction_id)

    else:
        print('User is not logged in')

    return JsonResponse('Payment ok', safe=False)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(
                email=form.cleaned_data["email"],
                username=form.cleaned_data["email"],
            )
            user.set_password(form.cleaned_data["password"])
            user.save()
            customer = Customer(user = user,
                                name=form.cleaned_data["name"],
                                email=form.cleaned_data["email"],)
            customer.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request=request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is None:
                return HttpResponse("BadRequest", status=400)
            login(request, user)
            return redirect("product")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("product")


from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product


def index(request):
    products = Product.objects.all()
    response = render(request, 'index.html', {"products": products})
    # cache.set(f"products-view-{title}-{purchases__count}", response, 60 * 60)
    return response


def products(request):
    if request.GET.get("product"):
        product = Product.objects.filter(title=f"{request.GET.get('product')}").first()
        return HttpResponse(f"""Title: {product.title},price: {product.price}""")

    get_all_products = Product.objects.all()
    prod_for_view = " "
    for data in get_all_products:
        get_data = f'<br>Product name - {data.title}. Price - {data.price}.'
        prod_for_view += get_data
    return HttpResponse(prod_for_view)



def cart(request):
    context = {}
    return render(request, 'cart.html', context)


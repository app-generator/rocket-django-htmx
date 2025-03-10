from django.http import HttpResponse
from django.shortcuts import render, redirect
from apps.tables.forms import ProductForm
from apps.common.models import Product
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.tables.utils import product_filter

# Create your views here.

def products_list(request):
    filters = product_filter(request)
    product_list = Product.objects.filter(**filters)

    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 5)
    products = paginator.page(page)

    return render(request, "partials/products_list.html", {"products": products})


def datatables(request):
  filters = product_filter(request)
  product_list = Product.objects.filter(**filters)
  form = ProductForm()

  page = request.GET.get('page', 1)
  paginator = Paginator(product_list, 5)
  products = paginator.page(page)

  context = {
    'segment'  : 'datatables',
    'parent'   : 'apps',
    'form'     : form,
    'products' : products
  }
  
  return render(request, 'apps/datatables.html', context)


@login_required(login_url='/users/signin/')
def add_product(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        product = form.save()
        filters = product_filter(request)
        product_list = Product.objects.filter(**filters)
        return render(request, 'partials/products_list.html', {'products': product_list})
    else:
        return HttpResponse("")

    # return products_list(request)  


@login_required(login_url='/users/signin/')
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponse("")


@login_required(login_url='/users/signin/')
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = int(request.POST.get('price'))
        product.info = request.POST.get('info')
        product.save()
        filters = product_filter(request)
        product_list = Product.objects.filter(**filters)
        return render(request, 'partials/products_list.html', {'products': product_list})
    return render(request, 'partials/product_row.html', {'product': product})
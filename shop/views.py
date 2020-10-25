from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
# Create your views here.
from .models import Category, Product, ProductType


def product_list(request, category_slug=None):
    category = None
    product_types = ProductType.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/shop.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'product_types': product_types,
                   })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,

                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    products = Product.objects.filter(available=True)
    return render(request, 'shop/single-product.html', {'product': product,
                                                     'cart_product_form': cart_product_form,
                                                     'products': products, }
                  )

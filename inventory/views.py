from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.store.models import Product, Supplier, Buyer, Order

@login_required(login_url='login')
def dashboard(request):
    enterprise = request.user.enterprise
    if enterprise:
        total_product = Product.objects.filter(enterprise=enterprise).count()
        total_supplier = Supplier.objects.filter(enterprise=enterprise).count()
        total_buyer = Buyer.objects.filter(enterprise=enterprise).count()
        total_oder = Order.objects.filter(enterprise=enterprise).count()
        orders = Order.objects.filter(enterprise=enterprise).order_by('-id')
    elif request.user.is_superuser:
        total_product = Product.objects.count()
        total_supplier = Supplier.objects.count()
        total_buyer = Buyer.objects.count()
        total_oder = Order.objects.count()
        orders = Order.objects.all().order_by('-id')
    else:
        total_product = 0
        total_supplier = 0
        total_buyer = 0
        total_oder = 0
        orders = Order.objects.none()

    context = {
        'product': total_product,
        'supplier': total_supplier,
        'buyer': total_buyer,
        'order': total_oder,
        'orders': orders,
        'enterprise': enterprise,
    }
    return render(request, 'dashboard.html', context)
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import datetime


from users.models import User
from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    OrderItem,
    Delivery
)
from .forms import (
    EditBuyerForm,
    SupplierForm,
    BuyerForm,
    SeasonForm,
    DropForm,
    ProductForm,
    OrderForm,
    DeliveryForm,
    OrderItemFormSet
)

# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_supplier=True)
                Supplier.objects.create(user=user, name=name, address=address)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Buyer views
@login_required(login_url='login')
def create_buyer(request):

    forms = BuyerForm()
    if request.method == 'POST':
        forms = BuyerForm(request.POST)
        if forms.is_valid():
            cpf = forms.cleaned_data['cpf']
            cleaned_cpf = ''.join(filter(str.isdigit, cpf))

            name = forms.cleaned_data['name']
            address = 'nao_informado'
            email = forms.cleaned_data['email']
            username = cleaned_cpf
            password = 'Trotsky@123'  # Senha padrão
            function = forms.cleaned_data['function']
            salary = 0.01
            cpf = cleaned_cpf
            pis = forms.cleaned_data['pis']
            rg = forms.cleaned_data['rg']
            nascimento = forms.cleaned_data['nascimento']
            estado_civil = 'solteiro'
            escolaridade = 'nao_informado'
            setor= forms.cleaned_data['setor']
   

            
            user = User.objects.create_user(username=username, password=password, email=email, is_buyer=True)
            Buyer.objects.create(user=user,
                                    name=name,
                                    address=address,
                                    function=function,
                                    salary=salary,
                                    cpf=cpf,
                                    pis=pis,
                                    rg=rg,
                                    nascimento=nascimento,
                                    estado_civil=estado_civil,
                                    escolaridade=escolaridade,
                                    setor=setor
                                    )
            return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addbuyer.html', context)

class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'

def delete_buyer(request, pk):
    buyer = Buyer.objects.get(id=pk)
    user = buyer.user
    buyer.delete()
    user.delete()
    return redirect('buyer-list')

def edit_buyer(request, pk):
    buyer = Buyer.objects.get(id=pk)
    exclude_fields=['retype_password','salary', 'address', 'password','estado_civil','escolaridade']

    if request.method == 'POST':
              
        forms = EditBuyerForm(request.POST, exclude_fields=exclude_fields)
        
        if forms.is_valid():
            cpf = forms.cleaned_data['cpf']
            cleaned_cpf = ''.join(filter(str.isdigit, cpf))
            buyer.user.name = forms.cleaned_data['name']
            buyer.address = 'nao_informado'
            buyer.user.email = forms.cleaned_data['email']
            buyer.function = forms.cleaned_data['function']
            buyer.salary = 0.01
            buyer.cpf = cleaned_cpf
            buyer.pis = forms.cleaned_data['pis']
            buyer.rg = forms.cleaned_data['rg']
            buyer.nascimento = forms.cleaned_data['nascimento']
            buyer.estado_civil = 'solteiro'
            buyer.escolaridade = 'nao_informado'      
            buyer.setor = forms.cleaned_data['setor']
            buyer.user.save() 
            buyer.save()
            
            return redirect('buyer-list')
        else:
            print(forms.errors)
    else:
        data_banco = str(buyer.nascimento)
        data_objeto = datetime.strptime(data_banco, "%Y-%m-%d")
        data_formatada = data_objeto.strftime("%Y-%m-%d")
        print(data_formatada)

        forms = EditBuyerForm(             
            exclude_fields=exclude_fields,       
            initial={
                'name': buyer.name,       
                'email': buyer.user.email,    
                'function': buyer.function,         
                'cpf': buyer.cpf,
                'pis': buyer.pis,
                'rg': buyer.rg,
                'nascimento': data_formatada,
                'setor': buyer.setor,
            }
        )
    
    context = {
        'buyer': buyer,
        'form': forms
    }
    return render(request, 'store/editbuyer.html', context)

# Season views
@login_required(login_url='login')
def create_season(request):
    forms = SeasonForm()
    if request.method == 'POST':
        forms = SeasonForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('season-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSeason.html', context)


class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'


# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addCategory.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/category_list.html'
    context_object_name = 'drop'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm()
    formset = OrderItemFormSet()
    if request.method == 'POST':
        user = request.user
        forms = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)        

        if forms.is_valid() and formset.is_valid() and user.is_supplier:            
            order = forms.save(commit=False)
            order.save()            
            formset.instance = order
            
            isinstances = formset.save(commit=False)
            for instance in isinstances:
                instance.save()

            return redirect('order-list')
    context = {
        'form': forms,
        'formset': formset,
    }
    return render(request, 'store/addOrder.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.annotate(
            item_count=Count('items')
        ).order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm()
    if request.method == 'POST':
        forms = DeliveryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addelivery.html', context)

@login_required(login_url='login')
def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    detail = OrderItem.objects.filter(order=order)
    order_itens = detail.count()
    estoque= Product.objects.all()
    mensagem_erro = "zero"

    for item in detail:
        if item.quantity > Product.objects.get(id=item.product.id).quantity:
            if mensagem_erro == "zero":
                mensagem_erro = f"Estoque insuficiente para o(s) produto(s): {item.product.name}"
            else:
                mensagem_erro +=f", {item.product.name}"

    if mensagem_erro != "zero":
        mensagem_erro += ".\n Por favor, ajuste a quantidade antes de processar o pedido."

    if request.method == 'POST':        
        for item in detail:
            for product in estoque:
                if item.product.id == product.id:
                    product.quantity -= item.quantity
                    product.save()
        order.status = 'complete'
        order.supplier = Supplier.objects.get(user=request.user)
        order.delivered_date = timezone.now()
        order.save()
        return redirect('order-list')

    
    context = {
        'order': order,
        'details': detail,
        'order_itens': order_itens,
        'mensagem_erro': mensagem_erro
    }
    return render(request, 'store/order_detail.html', context)

@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.supplier = Supplier.objects.get(user=request.user)
    order.status = 'decline'
    order.delivered_date = timezone.now()
    order.save()
    return redirect('order-list')

class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'
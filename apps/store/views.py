from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime


from apps.users.models import User
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
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=name,
                    is_supplier=True,
                    enterprise=request.user.enterprise
                )
                Supplier.objects.create(
                    user=user,
                    name=name,
                    address=address,
                    enterprise=request.user.enterprise
                )
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'

    def get_queryset(self):
        if self.request.user.enterprise:
            return Supplier.objects.filter(enterprise=self.request.user.enterprise)
        if self.request.user.is_superuser:
            return Supplier.objects.all()
        return Supplier.objects.none()


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm(enterprise=request.user.enterprise)
    if request.method == 'POST':
        forms = BuyerForm(request.POST, enterprise=request.user.enterprise)
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
            setor = forms.cleaned_data['setor']

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name,
                is_buyer=True,
                enterprise=request.user.enterprise
            )
            Buyer.objects.create(
                user=user,
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
                setor=setor,
                enterprise=request.user.enterprise
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

    def get_queryset(self):
        if self.request.user.enterprise:
            qs = Buyer.objects.filter(enterprise=self.request.user.enterprise)
        elif self.request.user.is_superuser:
            qs = Buyer.objects.all()
        else:
            qs = Buyer.objects.none()

        q = self.request.GET.get('q', '').strip()
        if q:
            clean_q = q.lstrip('#').strip()
            if clean_q.isdigit():
                qs = qs.filter(
                    Q(sub_id=int(clean_q)) |
                    Q(name__icontains=q) |
                    Q(cpf__icontains=q)
                )
            else:
                qs = qs.filter(
                    Q(name__icontains=q) |
                    Q(cpf__icontains=q) |
                    Q(user__email__icontains=q) |
                    Q(function__icontains=q) |
                    Q(setor__name__icontains=q)
                )
        return qs.order_by('sub_id', 'id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context


@login_required(login_url='login')
def delete_buyer(request, pk):
    if request.user.enterprise:
        buyer = get_object_or_404(Buyer, id=pk, enterprise=request.user.enterprise)
    elif request.user.is_superuser:
        buyer = get_object_or_404(Buyer, id=pk)
    else:
        return redirect('buyer-list')
    user = buyer.user
    buyer.delete()
    user.delete()
    return redirect('buyer-list')


@login_required(login_url='login')
def edit_buyer(request, pk):
    if request.user.enterprise:
        buyer = get_object_or_404(Buyer, id=pk, enterprise=request.user.enterprise)
    elif request.user.is_superuser:
        buyer = get_object_or_404(Buyer, id=pk)
    else:
        return redirect('buyer-list')

    exclude_fields = ['retype_password', 'salary', 'address', 'password', 'estado_civil', 'escolaridade']

    if request.method == 'POST':
        forms = EditBuyerForm(request.POST, exclude_fields=exclude_fields, enterprise=request.user.enterprise)
        if forms.is_valid():
            cpf = forms.cleaned_data['cpf']
            cleaned_cpf = ''.join(filter(str.isdigit, cpf))
            buyer.name = forms.cleaned_data['name']
            buyer.user.first_name = forms.cleaned_data['name']
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
        data_formatada = buyer.nascimento.strftime("%Y-%m-%d") if buyer.nascimento else ""

        forms = EditBuyerForm(             
            exclude_fields=exclude_fields,
            enterprise=request.user.enterprise,
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
            season = forms.save(commit=False)
            season.enterprise = request.user.enterprise
            season.save()
            return redirect('season-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSeason.html', context)


class SeasonListView(ListView):
    model = Season
    template_name = 'store/season_list.html'
    context_object_name = 'season'

    def get_queryset(self):
        if self.request.user.enterprise:
            return Season.objects.filter(enterprise=self.request.user.enterprise)
        if self.request.user.is_superuser:
            return Season.objects.all()
        return Season.objects.none()


# Drop views
@login_required(login_url='login')
def create_drop(request):
    forms = DropForm()
    if request.method == 'POST':
        forms = DropForm(request.POST)
        if forms.is_valid():
            drop = forms.save(commit=False)
            drop.enterprise = request.user.enterprise
            drop.save()
            return redirect('drop-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addCategory.html', context)


class DropListView(ListView):
    model = Drop
    template_name = 'store/category_list.html'
    context_object_name = 'drop'

    def get_queryset(self):
        if self.request.user.enterprise:
            return Drop.objects.filter(enterprise=self.request.user.enterprise)
        if self.request.user.is_superuser:
            return Drop.objects.all()
        return Drop.objects.none()


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            product = forms.save(commit=False)
            product.enterprise = request.user.enterprise
            product.save()
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'

    def get_queryset(self):
        if self.request.user.enterprise:
            return Product.objects.filter(enterprise=self.request.user.enterprise)
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.none()


# Order views
@login_required(login_url='login')
def create_order(request):
    forms = OrderForm(enterprise=request.user.enterprise)
    formset = OrderItemFormSet(enterprise=request.user.enterprise)
    if request.method == 'POST':
        user = request.user
        forms = OrderForm(request.POST, enterprise=request.user.enterprise)
        formset = OrderItemFormSet(request.POST, enterprise=request.user.enterprise)        

        if forms.is_valid() and formset.is_valid() and (user.is_supplier or user.is_admin or user.is_superuser):            
            order = forms.save(commit=False)
            order.enterprise = request.user.enterprise
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
        if self.request.user.enterprise:
            qs = Order.objects.filter(enterprise=self.request.user.enterprise)
        elif self.request.user.is_superuser:
            qs = Order.objects.all()
        else:
            qs = Order.objects.none()

        context['order'] = qs.annotate(
            item_count=Count('items')
        ).order_by('-id')
        return context


# Delivery views
@login_required(login_url='login')
def create_delivery(request):
    forms = DeliveryForm(enterprise=request.user.enterprise)
    if request.method == 'POST':
        forms = DeliveryForm(request.POST, enterprise=request.user.enterprise)
        if forms.is_valid():
            delivery = forms.save(commit=False)
            delivery.enterprise = request.user.enterprise
            delivery.save()
            return redirect('delivery-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addelivery.html', context)


@login_required(login_url='login')
def order_detail(request, pk):
    if request.user.enterprise:
        order = get_object_or_404(Order, id=pk, enterprise=request.user.enterprise)
        estoque = Product.objects.filter(enterprise=request.user.enterprise)
    elif request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
        estoque = Product.objects.all()
    else:
        return redirect('order-list')

    detail = OrderItem.objects.filter(order=order)
    order_itens = detail.count()
    mensagem_erro = "zero"

    for item in detail:
        prod = Product.objects.filter(id=item.product.id).first()
        if prod and item.quantity > prod.quantity:
            if mensagem_erro == "zero":
                mensagem_erro = f"Estoque insuficiente para o(s) produto(s): {item.product.name}"
            else:
                mensagem_erro += f", {item.product.name}"

    if mensagem_erro != "zero":
        mensagem_erro += ".\n Por favor, ajuste a quantidade antes de processar o pedido."

    if request.method == 'POST':        
        for item in detail:
            for product in estoque:
                if item.product.id == product.id:
                    product.quantity -= item.quantity
                    product.save()
        order.status = 'complete'
        supplier = Supplier.objects.filter(user=request.user).first()
        if supplier:
            order.supplier = supplier
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
    if request.user.enterprise:
        order = get_object_or_404(Order, id=pk, enterprise=request.user.enterprise)
    elif request.user.is_superuser:
        order = get_object_or_404(Order, id=pk)
    else:
        return redirect('order-list')

    supplier = Supplier.objects.filter(user=request.user).first()
    if supplier:
        order.supplier = supplier
    order.status = 'decline'
    order.delivered_date = timezone.now()
    order.save()
    return redirect('order-list')


class DeliveryListView(ListView):
    model = Delivery
    template_name = 'store/delivery_list.html'
    context_object_name = 'delivery'

    def get_queryset(self):
        if self.request.user.enterprise:
            return Delivery.objects.filter(enterprise=self.request.user.enterprise)
        if self.request.user.is_superuser:
            return Delivery.objects.all()
        return Delivery.objects.none()
from django import forms

from .models import (
    Season, 
    Drop, 
    Product, 
    Order, 
    Delivery, 
    Supplier, 
    Buyer,
    OrderItem, 

)

class SupplierForm(forms.Form):
    name = forms.CharField(
        label="Nome completo",  
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o nome',
        'placeholder': 'Nome completo',
        
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Please enter address',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Please enter email',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Please enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Please enter password',
    }))
    retype_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Please enter retype_password',
    }))

class BuyerForm(forms.Form):
    name = forms.CharField(
        label="Nome completo",  
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o nome',
        'placeholder': 'Nome completo',
    }))

    address = forms.CharField(
        label="Endereço",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o endereço',
        'placeholder': 'Endereço',
    }))
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o email',
        'placeholder': 'exemplo@Email.com',
    }))
    username = forms.CharField(
        label="Nome de usuário",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o nome de usuário',
        'placeholder': 'Nome de usuário',
    }))
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a senha',
        'placeholder': 'Senha',
    }))
    retype_password = forms.CharField(
        label="Redigite a senha",
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a senha novamente',
        'placeholder': 'Redigite a senha',
    }))
    function = forms.CharField(
        label="Função",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'function',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a função',
        'placeholder': 'Função',
    }))
    salary = forms.DecimalField(
        label="Salário",
        widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'salary',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o salário',
        'placeholder': 'Salário',
    }))
    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'cpf',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o CPF',
        'placeholder': 'CPF',
    }))
    pis = forms.CharField(
        label="PIS",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'pis',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o PIS',
        'placeholder': 'PIS',
    }))
    rg = forms.CharField(
        label="RG",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'rg',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o RG',
        'placeholder': 'RG',
    }))
    nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
        'class': 'form-control',
        'id': 'nascimento',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a data de nascimento',
        'type': 'date',
        'placeholder': 'Data de Nascimento',
    }))
    estado_civil = forms.ChoiceField(
        label="Estado Civil",
        choices=[
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('separado', 'Separado(a)'),
        ('uniao_estavel', 'União Estável'),
        ('outro', 'Outro'),
    ], widget=forms.Select(
        
        attrs={
        'class': 'form-control',
        'id': 'estado_civil',
        'data-val': 'true',
        'data-val-required': 'Por favor selecione o estado civil',
        
    }))
    escolaridade = forms.CharField(
        label="Escolaridade",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'escolaridade',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a escolaridade',
        'placeholder': 'Escolaridade',
    }))
    setor = forms.ModelChoiceField(
        label="Setor",
        queryset=Season.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'setor',
            'data-val': 'true',
            'data-val-required': 'Por favor selecione o setor',
        }))    
    

class EditBuyerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', [])  # Extrair aqui
        super().__init__(*args, **kwargs)
        
        for field in exclude_fields:
            if field in self.fields:
                del self.fields[field]    
    name = forms.CharField(
        label="Nome completo",  
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'name',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o nome',
        'placeholder': 'Nome completo',
    }))

    address = forms.CharField(
        label="Endereço",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o endereço',
        'placeholder': 'Endereço',
    }))
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o email',
        'placeholder': 'exemplo@Email.com',
    }))
    
    password = forms.CharField(
        label="Senha",
        required=False,
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a senha',
        'placeholder': 'Senha',
    }))
    retype_password = forms.CharField(
        required=False,
        label="Redigite a senha",
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'retype_password',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a senha novamente',
        'placeholder': 'Redigite a senha',
    }))
    function = forms.CharField(
        label="Função",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'function',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a função',
        'placeholder': 'Função',
    }))
    salary = forms.DecimalField(
        label="Salário",
        widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'salary',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o salário',
        'placeholder': 'Salário',
    }))
    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'cpf',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o CPF',
        'placeholder': 'CPF',
    }))
    pis = forms.CharField(
        label="PIS",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'pis',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o PIS',
        'placeholder': 'PIS',
    }))
    rg = forms.CharField(
        label="RG",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'rg',
        'data-val': 'true',
        'data-val-required': 'Por favor digite o RG',
        'placeholder': 'RG',
    }))
    nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
        'class': 'form-control',
        'id': 'nascimento',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a data de nascimento',
        'type': 'date',
        'placeholder': 'Data de Nascimento',
    }))
    estado_civil = forms.ChoiceField(
        label="Estado Civil",
        choices=[
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('separado', 'Separado(a)'),
        ('uniao_estavel', 'União Estável'),
        ('outro', 'Outro'),
    ], widget=forms.Select(
        
        attrs={
        'class': 'form-control',
        'id': 'estado_civil',
        'data-val': 'true',
        'data-val-required': 'Por favor selecione o estado civil',
        
    }))
    escolaridade = forms.CharField(
        label="Escolaridade",
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'escolaridade',
        'data-val': 'true',
        'data-val-required': 'Por favor digite a escolaridade',
        'placeholder': 'Escolaridade',
    }))
    setor = forms.ModelChoiceField(
        label="Setor",
        queryset=Season.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'setor',
            'data-val': 'true',
            'data-val-required': 'Por favor selecione o setor',
        }))

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'id': 'description'})
        }


class DropForm(forms.ModelForm):
    class Meta:
        model = Drop
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'})
        }



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit_of_measurement', 'show_size', 'size']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'id': 'unit_of_measurement'}),
            'show_size': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'show_size'}),
            'size': forms.TextInput(attrs={'class': 'form-control', 'id': 'size'})
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["buyer", ]

        labels = {
            'buyer': 'Colaborador',  # ✅ Label definido aqui
        }

        widgets = {
            'buyer': forms.Select(
                attrs={'class': 'form-control', 'id': 'buyer','data-live-search': 'true'}),
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
    

class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        label="Produto",
        queryset=Product.objects.filter(is_active=True),
         widget=forms.Select(attrs={
        'class': 'form-select product-select',
        'data-live-search': 'true'
    }))

    quantity = forms.IntegerField(
        label="Quantidade",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control quantity-input',
            'min': '1'
        })
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']    


from django.forms import inlineformset_factory

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,  # Quantidade de forms vazios para adicionar
    can_delete=True,
    fields=['product', 'quantity']
)

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'

        widgets = {
            'order': forms.Select(attrs={'class': 'form-control', 'id': 'order'}),
            'courier_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'courier_name'}),
        }

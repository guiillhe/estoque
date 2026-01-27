from django.db import models

from users.models import User


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"

    def __str__(self):
        return self.name


class Buyer(models.Model):
    ESTADO_CIVIL_CHOICES = [
        ('solteiro', 'Solteiro(a)'),
        ('casado', 'Casado(a)'),
        ('divorciado', 'Divorciado(a)'),
        ('viuvo', 'Viúvo(a)'),
        ('separado', 'Separado(a)'),
        ('uniao_estavel', 'União Estável'),
        ('outro', 'Outro'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False,blank=False, null=False)
    address = models.CharField(max_length=220)
    function = models.CharField(max_length=120, default='')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cpf = models.CharField(max_length=14, unique=True, default='')
    pis = models.CharField(max_length=14, unique=True, default='')
    rg = models.CharField(max_length=30, unique=True,default='')
    nascimento = models.DateField(default=None, null=True, blank=True)
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL_CHOICES, default='solteiro')
    escolaridade = models.CharField(max_length=50, default='')
    created_date = models.DateField(auto_now_add=True)
    setor = models.ForeignKey("Season", verbose_name="Setor", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):        
        return self.name


class Drop(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    quantity= models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    unit_of_measurement = models.CharField(max_length=50)
    show_size = models.BooleanField(default=False)
    size = models.CharField(max_length=50,null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


    def __str__(self):
        return self.name

class OrderItem(models.Model):
    """Tabela intermediária para relacionamento Order-Product com quantidade"""
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Pedido"
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name="Produto"
    )
    
    quantity = models.PositiveIntegerField(
        default=1,        
        verbose_name="Quantidade"
    ) 
    
    
   
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        unique_together = ['order', 'product']  # Evita duplicatas
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Pedido #{self.order.id})"    
    

class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pendente'),
        ('decline', 'Negado'),
        ('approved', 'Aprovado'),
        ('processing', 'Processando'),
        ('complete', 'Completo'),
        ('bulk', 'Lote'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,blank=True)        
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)      
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    delivered_date = models.DateField(null=True, blank=True)
    

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


    def __str__(self):
        return f"Pedido #{self.id} - {self.buyer.name}"


class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.courier_name
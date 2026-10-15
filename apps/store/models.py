from django.db import models
from apps.users.models import User


class Supplier(models.Model):
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='suppliers',
        verbose_name="Empresa"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"
        unique_together = ['enterprise', 'name']

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
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='buyers',
        verbose_name="Empresa"
    )
    sub_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Sub ID",
        help_text="Identificador sequencial do colaborador dentro da empresa"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=False, blank=False, null=False)
    address = models.CharField(max_length=220)
    function = models.CharField(max_length=120, default='')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cpf = models.CharField(max_length=14, unique=True, default='')
    pis = models.CharField(max_length=14, unique=True, default='')
    rg = models.CharField(max_length=30, unique=True, default='')
    nascimento = models.DateField(default=None, null=True, blank=True)
    estado_civil = models.CharField(max_length=30, choices=ESTADO_CIVIL_CHOICES, default='solteiro')
    escolaridade = models.CharField(max_length=50, default='')
    created_date = models.DateField(auto_now_add=True)
    setor = models.ForeignKey("Season", verbose_name="Setor", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        unique_together = [['enterprise', 'sub_id']]
        ordering = ['sub_id', 'id']

    def save(self, *args, **kwargs):
        if not self.sub_id:
            from django.db import transaction
            from django.db.models import Max
            with transaction.atomic():
                max_sub = Buyer.objects.filter(enterprise=self.enterprise).aggregate(
                    max_sub=Max('sub_id')
                )['max_sub']
                self.sub_id = (max_sub or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        if self.sub_id:
            return f"#{self.sub_id} - {self.name}"
        return self.name


class Season(models.Model):
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='seasons',
        verbose_name="Empresa"
    )
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"
        unique_together = ['enterprise', 'name']

    def __str__(self):        
        return self.name


class Drop(models.Model):
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='drops',
        verbose_name="Empresa"
    )
    name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        unique_together = ['enterprise', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Empresa"
    )
    name = models.CharField(max_length=120)
    quantity = models.PositiveIntegerField()
    created_date = models.DateField(auto_now_add=True)
    unit_of_measurement = models.CharField(max_length=50)
    show_size = models.BooleanField(default=False)
    size = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        unique_together = ['enterprise', 'name']

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
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="Empresa"
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)        
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)      
    created_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='pending')
    delivered_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.buyer.name if self.buyer else 'Sem colaborador'}"


class Delivery(models.Model):
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='deliveries',
        verbose_name="Empresa"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    courier_name = models.CharField(max_length=120)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"

    def __str__(self):
        return self.courier_name
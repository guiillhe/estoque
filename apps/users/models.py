from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    enterprise = models.ForeignKey(
        'enterprises.Enterprise',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Empresa"
    )

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        if full_name:
            return full_name
        if hasattr(self, 'buyer') and self.buyer and self.buyer.name:
            return self.buyer.name
        if hasattr(self, 'supplier') and self.supplier and self.supplier.name:
            return self.supplier.name
        return self.first_name or self.username

    def __str__(self):
        return self.get_full_name() or self.username
from django.db import models
from apps.users.models import User


class Enterprise(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome da Empresa")
    num_contrato = models.CharField(max_length=50, verbose_name="Número do Contrato")
    cnpj = models.CharField(max_length=20, unique=True, verbose_name="CNPJ")
    responsavel = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'is_admin': True},
        related_name='enterprises',
        verbose_name="Responsável"
    )
    created_date = models.DateField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name

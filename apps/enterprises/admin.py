from django.contrib import admin
from .models import Enterprise


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['name', 'num_contrato', 'cnpj', 'responsavel', 'created_date']
    search_fields = ['name', 'num_contrato', 'cnpj', 'responsavel__username']


admin.site.register(Enterprise, EnterpriseAdmin)

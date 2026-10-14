from django import forms
from apps.users.models import User
from .models import Enterprise


class EnterpriseForm(forms.ModelForm):
    responsavel = forms.ModelChoiceField(
        label="Responsável",
        queryset=User.objects.filter(is_admin=True),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'responsavel',
            'data-val': 'true',
            'data-val-required': 'Por favor selecione o responsável',
        }),
        empty_label="Selecione um responsável (Admin)"
    )

    class Meta:
        model = Enterprise
        fields = ['name', 'num_contrato', 'cnpj', 'responsavel']
        labels = {
            'name': 'Nome da Empresa',
            'num_contrato': 'Número do Contrato',
            'cnpj': 'CNPJ',
            'responsavel': 'Responsável',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Nome da Empresa',
                'data-val': 'true',
                'data-val-required': 'Por favor digite o nome da empresa',
            }),
            'num_contrato': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'num_contrato',
                'placeholder': 'Número do Contrato',
                'data-val': 'true',
                'data-val-required': 'Por favor digite o número do contrato',
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'cnpj',
                'placeholder': 'CNPJ',
                'data-val': 'true',
                'data-val-required': 'Por favor digite o CNPJ',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel'].queryset = User.objects.filter(is_admin=True)
        self.fields['responsavel'].label_from_instance = lambda obj: (
            f"{obj.get_full_name()} ({obj.username})" if obj.get_full_name() else obj.username
        )

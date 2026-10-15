from django import forms
from apps.users.models import User
from .models import Enterprise


class EnterpriseForm(forms.ModelForm):
    responsavel = forms.ModelChoiceField(
        label="Responsável",
        queryset=User.objects.filter(is_admin=True),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'responsavel',
        }),
        empty_label="Selecione um responsável (Admin)"
    )

    # Campos opcionais para cadastrar novo administrador no momento de criar a empresa
    create_new_admin = forms.BooleanField(
        label="Criar novo Administrador para esta empresa",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'create_new_admin'})
    )
    admin_name = forms.CharField(
        label="Nome Completo do Administrador",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'admin_name',
            'placeholder': 'Nome Completo do Admin',
        })
    )
    admin_username = forms.CharField(
        label="Login / Usuário do Administrador",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'admin_username',
            'placeholder': 'Usuário de acesso',
        })
    )
    admin_email = forms.EmailField(
        label="Email do Administrador",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'admin_email',
            'placeholder': 'admin@empresa.com',
        })
    )
    admin_password = forms.CharField(
        label="Senha do Administrador",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'admin_password',
            'placeholder': 'Senha de acesso',
        })
    )
    admin_confirm_password = forms.CharField(
        label="Confirmar Senha do Administrador",
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'admin_confirm_password',
            'placeholder': 'Confirmação da senha',
        })
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
        # Exibe apenas o NOME do responsável, e não o usuário (username)
        self.fields['responsavel'].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )

    def clean(self):
        cleaned_data = super().clean()
        create_new_admin = cleaned_data.get('create_new_admin')
        admin_username = cleaned_data.get('admin_username')
        admin_name = cleaned_data.get('admin_name')
        admin_password = cleaned_data.get('admin_password')
        admin_confirm_password = cleaned_data.get('admin_confirm_password')
        responsavel = cleaned_data.get('responsavel')

        if create_new_admin or admin_username:
            if not admin_name:
                self.add_error('admin_name', 'Por favor informe o nome completo do administrador.')
            if not admin_username:
                self.add_error('admin_username', 'Por favor informe o usuário do administrador.')
            elif User.objects.filter(username=admin_username).exists():
                self.add_error('admin_username', 'Este nome de usuário já está em uso.')
            if not admin_password:
                self.add_error('admin_password', 'Por favor informe a senha do administrador.')
            if admin_password and admin_confirm_password and admin_password != admin_confirm_password:
                self.add_error('admin_confirm_password', 'As senhas não coincidem.')
        elif not responsavel:
            self.add_error('responsavel', 'Por favor selecione o responsável ou marque para cadastrar um novo administrador.')

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        create_new_admin = cleaned_data.get('create_new_admin')
        admin_username = cleaned_data.get('admin_username')

        created_admin = None
        if create_new_admin or admin_username:
            admin_name = cleaned_data.get('admin_name')
            admin_email = cleaned_data.get('admin_email', '')
            admin_password = cleaned_data.get('admin_password')

            created_admin = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name=admin_name,
                is_admin=True
            )
            self.instance.responsavel = created_admin

        instance = super().save(commit=commit)

        if created_admin:
            created_admin.enterprise = instance
            created_admin.save()
        elif instance.responsavel and not instance.responsavel.enterprise:
            instance.responsavel.enterprise = instance
            instance.responsavel.save()

        return instance


class EnterpriseAdminForm(forms.Form):
    name = forms.CharField(
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': 'Nome Completo do Administrador',
            'data-val': 'true',
            'data-val-required': 'Por favor digite o nome completo',
        })
    )
    username = forms.CharField(
        label="Usuário / Login",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Nome de usuário para login',
            'data-val': 'true',
            'data-val-required': 'Por favor digite o nome de usuário',
        })
    )
    email = forms.EmailField(
        label="Email",
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'admin@empresa.com',
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Digite a senha',
            'data-val': 'true',
            'data-val-required': 'Por favor digite a senha',
        })
    )
    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirm_password',
            'placeholder': 'Confirme a senha',
            'data-val': 'true',
            'data-val-required': 'Por favor confirme a senha',
        })
    )
    enterprise = forms.ModelChoiceField(
        label="Empresa",
        queryset=Enterprise.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'enterprise',
            'data-val': 'true',
            'data-val-required': 'Por favor selecione a empresa',
        }),
        empty_label="Selecione a Empresa"
    )
    set_as_responsavel = forms.BooleanField(
        label="Definir como Responsável da Empresa selecionada",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'set_as_responsavel'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")
        return cleaned_data

    def save(self):
        name = self.cleaned_data['name']
        username = self.cleaned_data['username']
        email = self.cleaned_data.get('email', '')
        password = self.cleaned_data['password']
        enterprise = self.cleaned_data['enterprise']
        set_as_responsavel = self.cleaned_data.get('set_as_responsavel', False)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
            is_admin=True,
            enterprise=enterprise
        )

        if set_as_responsavel and enterprise:
            enterprise.responsavel = user
            enterprise.save()

        return user

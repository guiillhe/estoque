from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from .models import Enterprise
from .forms import EnterpriseForm, EnterpriseAdminForm


class EnterpriseTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superadmin',
            email='super@example.com',
            password='password123'
        )
        self.admin_user = User.objects.create_user(
            username='admin_resp',
            first_name='Carlos Administrador',
            password='password123',
            is_admin=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            first_name='Usuario Comum',
            password='password123',
            is_admin=False
        )
        self.enterprise = Enterprise.objects.create(
            name='Empresa Teste',
            num_contrato='CTR-2026-001',
            cnpj='12.345.678/0001-90',
            responsavel=self.admin_user
        )

    def test_model_str(self):
        self.assertEqual(str(self.enterprise), 'Empresa Teste')

    def test_form_queryset_only_admins(self):
        form = EnterpriseForm()
        responsavel_queryset = form.fields['responsavel'].queryset
        self.assertIn(self.admin_user, responsavel_queryset)
        self.assertNotIn(self.regular_user, responsavel_queryset)

    def test_responsavel_label_displays_name_not_username(self):
        form = EnterpriseForm()
        label = form.fields['responsavel'].label_from_instance(self.admin_user)
        self.assertEqual(label, 'Carlos Administrador')
        self.assertNotIn('admin_resp', label)

    def test_superuser_can_access_list(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.get(reverse('enterprise-list'))
        self.assertEqual(response.status_code, 200)

    def test_non_superuser_redirected(self):
        self.client.login(username='regular', password='password123')
        response = self.client.get(reverse('enterprise-list'))
        self.assertEqual(response.status_code, 302)

    def test_create_enterprise_view_with_existing_admin(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.post(reverse('create-enterprise'), {
            'name': 'Nova Empresa',
            'num_contrato': 'CTR-999',
            'cnpj': '98.765.432/0001-10',
            'responsavel': self.admin_user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enterprise.objects.filter(name='Nova Empresa').exists())

    def test_create_enterprise_view_with_inline_new_admin(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.post(reverse('create-enterprise'), {
            'name': 'Empresa com Novo Admin',
            'num_contrato': 'CTR-888',
            'cnpj': '11.222.333/0001-44',
            'create_new_admin': True,
            'admin_name': 'Roberto Gerente',
            'admin_username': 'roberto_admin',
            'admin_email': 'roberto@empresa.com',
            'admin_password': 'AdminPassword123!',
            'admin_confirm_password': 'AdminPassword123!',
        })
        self.assertEqual(response.status_code, 302)
        enterprise = Enterprise.objects.get(name='Empresa com Novo Admin')
        self.assertEqual(enterprise.responsavel.username, 'roberto_admin')
        self.assertEqual(enterprise.responsavel.first_name, 'Roberto Gerente')
        self.assertTrue(enterprise.responsavel.is_admin)
        self.assertEqual(enterprise.responsavel.enterprise, enterprise)

    def test_create_enterprise_admin_view(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.post(reverse('create-enterprise-admin'), {
            'name': 'Fernanda Admin',
            'username': 'fernanda_admin',
            'email': 'fernanda@empresa.com',
            'password': 'SenhaSegura123!',
            'confirm_password': 'SenhaSegura123!',
            'enterprise': self.enterprise.id,
            'set_as_responsavel': True,
        })
        self.assertEqual(response.status_code, 302)
        new_admin = User.objects.get(username='fernanda_admin')
        self.assertEqual(new_admin.first_name, 'Fernanda Admin')
        self.assertTrue(new_admin.is_admin)
        self.assertEqual(new_admin.enterprise, self.enterprise)
        self.assertTrue(new_admin.check_password('SenhaSegura123!'))

        self.enterprise.refresh_from_db()
        self.assertEqual(self.enterprise.responsavel, new_admin)

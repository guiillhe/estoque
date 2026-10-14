from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from .models import Enterprise
from .forms import EnterpriseForm


class EnterpriseTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superadmin',
            email='super@example.com',
            password='password123'
        )
        self.admin_user = User.objects.create_user(
            username='admin_resp',
            password='password123',
            is_admin=True
        )
        self.regular_user = User.objects.create_user(
            username='regular',
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

    def test_superuser_can_access_list(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.get(reverse('enterprise-list'))
        self.assertEqual(response.status_code, 200)

    def test_non_superuser_redirected(self):
        self.client.login(username='regular', password='password123')
        response = self.client.get(reverse('enterprise-list'))
        self.assertEqual(response.status_code, 302)

    def test_create_enterprise_view(self):
        self.client.login(username='superadmin', password='password123')
        response = self.client.post(reverse('create-enterprise'), {
            'name': 'Nova Empresa',
            'num_contrato': 'CTR-999',
            'cnpj': '98.765.432/0001-10',
            'responsavel': self.admin_user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enterprise.objects.filter(name='Nova Empresa').exists())

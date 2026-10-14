from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from apps.store.models import Season, Product, Buyer


class StoreModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='storeuser', password='password123')

    def test_season_creation(self):
        season = Season.objects.create(name='Setor Teste', description='Descricao Teste')
        self.assertEqual(str(season), 'Setor Teste')

    def test_product_creation(self):
        product = Product.objects.create(
            name='Produto Teste',
            quantity=10,
            unit_of_measurement='UN'
        )
        self.assertEqual(str(product), 'Produto Teste')

    def test_authenticated_access(self):
        self.client.login(username='storeuser', password='password123')
        response = self.client.get(reverse('supplier-list'))
        self.assertEqual(response.status_code, 200)


from django.test import TestCase
from django.urls import reverse
from apps.users.models import User
from apps.enterprises.models import Enterprise
from apps.store.models import Season, Product, Buyer, Supplier


class StoreMultiTenancyTests(TestCase):
    def setUp(self):
        # Admin responsável Empresa A
        self.admin_a = User.objects.create_user(
            username='admin_a',
            first_name='Admin Empresa A',
            password='password123',
            is_admin=True
        )
        self.enterprise_a = Enterprise.objects.create(
            name='Empresa Alfa',
            num_contrato='CTR-A',
            cnpj='00.000.000/0001-01',
            responsavel=self.admin_a
        )
        self.admin_a.enterprise = self.enterprise_a
        self.admin_a.save()

        # Admin responsável Empresa B
        self.admin_b = User.objects.create_user(
            username='admin_b',
            first_name='Admin Empresa B',
            password='password123',
            is_admin=True
        )
        self.enterprise_b = Enterprise.objects.create(
            name='Empresa Beta',
            num_contrato='CTR-B',
            cnpj='00.000.000/0002-02',
            responsavel=self.admin_b
        )
        self.admin_b.enterprise = self.enterprise_b
        self.admin_b.save()

        # Dados existentes para A
        self.product_a = Product.objects.create(
            enterprise=self.enterprise_a,
            name='Produto Alfa',
            quantity=50,
            unit_of_measurement='UN'
        )
        self.season_a = Season.objects.create(
            enterprise=self.enterprise_a,
            name='Setor Alfa',
            description='Setor da Alfa'
        )

        # Dados existentes para B
        self.product_b = Product.objects.create(
            enterprise=self.enterprise_b,
            name='Produto Beta',
            quantity=100,
            unit_of_measurement='KG'
        )
        self.season_b = Season.objects.create(
            enterprise=self.enterprise_b,
            name='Setor Beta',
            description='Setor da Beta'
        )

    def test_product_list_scoped_to_user_enterprise(self):
        # Usuário da Empresa A só vê produtos da Empresa A
        self.client.login(username='admin_a', password='password123')
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)
        products = list(response.context['product'])
        self.assertIn(self.product_a, products)
        self.assertNotIn(self.product_b, products)

        # Usuário da Empresa B só vê produtos da Empresa B
        self.client.login(username='admin_b', password='password123')
        response_b = self.client.get(reverse('product-list'))
        self.assertEqual(response_b.status_code, 200)
        products_b = list(response_b.context['product'])
        self.assertIn(self.product_b, products_b)
        self.assertNotIn(self.product_a, products_b)

    def test_automatic_enterprise_association_on_product_create(self):
        self.client.login(username='admin_a', password='password123')
        response = self.client.post(reverse('create-product'), {
            'name': 'Novo Produto Auto Associado',
            'quantity': 25,
            'unit_of_measurement': 'CX',
            'size': 'G',
        })
        self.assertEqual(response.status_code, 302)
        new_prod = Product.objects.get(name='Novo Produto Auto Associado')
        self.assertEqual(new_prod.enterprise, self.enterprise_a)

    def test_same_product_name_in_different_enterprises_allowed(self):
        # Ambas as empresas podem ter um produto com o mesmo nome
        prod_same_name_a = Product.objects.create(
            enterprise=self.enterprise_a,
            name='Caneta Azul',
            quantity=10,
            unit_of_measurement='UN'
        )
        prod_same_name_b = Product.objects.create(
            enterprise=self.enterprise_b,
            name='Caneta Azul',
            quantity=20,
            unit_of_measurement='UN'
        )
        self.assertEqual(prod_same_name_a.name, prod_same_name_b.name)
        self.assertNotEqual(prod_same_name_a.enterprise, prod_same_name_b.enterprise)

    def test_automatic_enterprise_association_on_buyer_create(self):
        self.client.login(username='admin_a', password='password123')
        response = self.client.post(reverse('create-buyer'), {
            'name': 'João Colaborador',
            'email': 'joao@alfa.com',
            'function': 'Analista',
            'cpf': '12345678901',
            'pis': '98765432100',
            'rg': '1234567',
            'nascimento': '1990-01-01',
            'setor': self.season_a.id,
        })
        self.assertEqual(response.status_code, 302)
        buyer = Buyer.objects.get(cpf='12345678901')
        self.assertEqual(buyer.enterprise, self.enterprise_a)
        self.assertEqual(buyer.user.enterprise, self.enterprise_a)
        self.assertEqual(buyer.user.first_name, 'João Colaborador')
        self.assertEqual(buyer.sub_id, 1)

    def test_buyer_sub_id_auto_increment_per_enterprise(self):
        # Primeiro colaborador de A tem sub_id 1
        user_a1 = User.objects.create_user(username='colab_a1', enterprise=self.enterprise_a)
        buyer_a1 = Buyer.objects.create(
            enterprise=self.enterprise_a,
            user=user_a1,
            name='Colaborador A1',
            cpf='11111111101',
            rg='RG11111',
            pis='PIS11111'
        )
        self.assertEqual(buyer_a1.sub_id, 1)

        # Segundo colaborador de A tem sub_id 2
        user_a2 = User.objects.create_user(username='colab_a2', enterprise=self.enterprise_a)
        buyer_a2 = Buyer.objects.create(
            enterprise=self.enterprise_a,
            user=user_a2,
            name='Colaborador A2',
            cpf='11111111102',
            rg='RG11112',
            pis='PIS11112'
        )
        self.assertEqual(buyer_a2.sub_id, 2)

        # Primeiro colaborador de B começa do 1 (isolado de A)
        user_b1 = User.objects.create_user(username='colab_b1', enterprise=self.enterprise_b)
        buyer_b1 = Buyer.objects.create(
            enterprise=self.enterprise_b,
            user=user_b1,
            name='Colaborador B1',
            cpf='22222222201',
            rg='RG22221',
            pis='PIS22221'
        )
        self.assertEqual(buyer_b1.sub_id, 1)

        # Terceiro colaborador de A tem sub_id 3
        user_a3 = User.objects.create_user(username='colab_a3', enterprise=self.enterprise_a)
        buyer_a3 = Buyer.objects.create(
            enterprise=self.enterprise_a,
            user=user_a3,
            name='Colaborador A3',
            cpf='11111111103',
            rg='RG11113',
            pis='PIS11113'
        )
        self.assertEqual(buyer_a3.sub_id, 3)

    def test_buyer_list_search_by_sub_id_and_name(self):
        user1 = User.objects.create_user(username='c1', enterprise=self.enterprise_a)
        buyer1 = Buyer.objects.create(
            enterprise=self.enterprise_a,
            user=user1,
            name='Carlos Alberto',
            cpf='33333333301',
            rg='RG33331',
            pis='PIS33331'
        )
        user2 = User.objects.create_user(username='c2', enterprise=self.enterprise_a)
        buyer2 = Buyer.objects.create(
            enterprise=self.enterprise_a,
            user=user2,
            name='Mariana Souza',
            cpf='33333333302',
            rg='RG33332',
            pis='PIS33332'
        )

        self.client.login(username='admin_a', password='password123')

        # Buscar por sub_id "1"
        res1 = self.client.get(reverse('buyer-list') + '?q=1')
        self.assertEqual(res1.status_code, 200)
        self.assertIn(buyer1, res1.context['buyer'])
        self.assertNotIn(buyer2, res1.context['buyer'])

        # Buscar por sub_id com cerquilha "#2"
        res2 = self.client.get(reverse('buyer-list') + '?q=%232')
        self.assertEqual(res2.status_code, 200)
        self.assertIn(buyer2, res2.context['buyer'])
        self.assertNotIn(buyer1, res2.context['buyer'])

        # Buscar por nome "Mariana"
        res3 = self.client.get(reverse('buyer-list') + '?q=Mariana')
        self.assertEqual(res3.status_code, 200)
        self.assertIn(buyer2, res3.context['buyer'])
        self.assertNotIn(buyer1, res3.context['buyer'])

    def test_dashboard_scoped_to_enterprise(self):
        self.client.login(username='admin_a', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # Deve contar apenas o produto da Empresa A
        self.assertEqual(response.context['product'], 1)


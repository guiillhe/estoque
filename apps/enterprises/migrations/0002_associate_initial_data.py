from django.db import migrations


def associate_initial_data(apps, schema_editor):
    Enterprise = apps.get_model('enterprises', 'Enterprise')
    User = apps.get_model('users', 'User')
    Buyer = apps.get_model('store', 'Buyer')
    Supplier = apps.get_model('store', 'Supplier')
    Season = apps.get_model('store', 'Season')
    Drop = apps.get_model('store', 'Drop')
    Product = apps.get_model('store', 'Product')
    Order = apps.get_model('store', 'Order')
    Delivery = apps.get_model('store', 'Delivery')

    # Obter ou identificar Empresa Teste
    empresa_teste = Enterprise.objects.filter(name__icontains='teste').first()
    if not empresa_teste:
        empresa_teste = Enterprise.objects.filter(id=1).first()

    # Obter ou identificar Empresa Trots
    empresa_trots = Enterprise.objects.filter(name__icontains='trots').first()
    if not empresa_trots:
        empresa_trots = Enterprise.objects.filter(id=2).first()

    # Se estiver em ambiente novo/de testes e não existirem, não falha
    if not empresa_teste and not empresa_trots:
        return

    # 1. Usuário admin -> Empresa Teste
    admin_user = User.objects.filter(username='admin').first()
    if admin_user and empresa_teste:
        admin_user.enterprise = empresa_teste
        if not admin_user.first_name:
            admin_user.first_name = 'Administrador'
        admin_user.save()
        if not empresa_teste.responsavel_id:
            empresa_teste.responsavel = admin_user
            empresa_teste.save()

    # 2. Todos os outros usuários -> Empresa Trots
    if empresa_trots:
        other_users = User.objects.exclude(username='admin')
        for u in other_users:
            u.enterprise = empresa_trots

            # Preencher first_name se estiver vazio
            if not u.first_name:
                buyer = Buyer.objects.filter(user_id=u.id).first()
                if buyer and buyer.name:
                    u.first_name = buyer.name
                else:
                    supplier = Supplier.objects.filter(user_id=u.id).first()
                    if supplier and supplier.name:
                        u.first_name = supplier.name
                    elif u.username == '000000000000000000000':
                        u.first_name = 'Administrador Trots'
            u.save()

        # Atualizar registros existentes do estoque para Trots
        for supplier in Supplier.objects.filter(enterprise__isnull=True):
            supplier.enterprise = empresa_trots
            supplier.save()

        for buyer in Buyer.objects.filter(enterprise__isnull=True):
            buyer.enterprise = empresa_trots
            buyer.save()

        for season in Season.objects.filter(enterprise__isnull=True):
            season.enterprise = empresa_trots
            season.save()

        for drop in Drop.objects.filter(enterprise__isnull=True):
            drop.enterprise = empresa_trots
            drop.save()

        for product in Product.objects.filter(enterprise__isnull=True):
            product.enterprise = empresa_trots
            product.save()

        for order in Order.objects.filter(enterprise__isnull=True):
            order.enterprise = empresa_trots
            order.save()

        for delivery in Delivery.objects.filter(enterprise__isnull=True):
            delivery.enterprise = empresa_trots
            delivery.save()


def reverse_associate_initial_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0001_initial'),
        ('users', '0003_user_enterprise'),
        ('store', '0003_alter_delivery_options_alter_drop_options_and_more'),
    ]

    operations = [
        migrations.RunPython(associate_initial_data, reverse_associate_initial_data),
    ]

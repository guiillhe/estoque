
import os
import sys
import django
from dotenv import load_dotenv


load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')
django.setup()

from users.models import User

def create_superuser_from_env():
    """Cria superuser a partir de variáveis de ambiente"""
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    
    if not password:
        print('❌ Erro: Senha não definida no .env')
        sys.exit(1)
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Superuser criado com sucesso!')
        print(f'👤 Usuário: {username}')
        print(f'📧 Email: {email}')
        print('🔑 Senha: [definida no .env]')
    else:
        print(f'⚠️ Usuário "{username}" já existe!')

if __name__ == '__main__':
    create_superuser_from_env()
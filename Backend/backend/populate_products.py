import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Product
from admins.models import Admin
from django.contrib.auth.models import User

# Create admin user if doesn't exist
admin_user, created = User.objects.get_or_create(
    username='shop_owner',
    defaults={
        'email': 'owner@terapiadoce.com',
        'is_staff': True,
        'is_superuser': False
    }
)

if created:
    admin_user.set_password('shopowner123')  # Change this password
    admin_user.save()
    print(f"Created admin user: {admin_user.username}")

# Get or create admin profile
admin_profile, created = Admin.objects.get_or_create(
    user=admin_user,
    defaults={
        'name': 'Proprietário da Loja',
        'email': 'owner@terapiadoce.com',
        'role': 'owner'
    }
)

# Product data from your doce.js file
products_data = [
    {
        'name': 'Brigadeiro Tradicional 50% Cacau',
        'description': 'Brigadeiro gourmet de chocolate 50% cacau.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/brig-trad.png'
    },
    {
        'name': 'Brigadeiro Beijinho',
        'description': 'Brigadeiro cremoso de coco.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/beijinho.png'
    },
    {
        'name': 'Brigadeiro Casadinho',
        'description': 'A combinação perfeita do brigadeiro tradicional com o beijinho.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/casadinho.png'
    },
    {
        'name': 'Brigadeiro Nesquik',
        'description': 'Brigadeiro com sabor delicioso de Nesquik (morango).',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/nesquik.png'
    },
    {
        'name': 'Brigadeiro Napolitano',
        'description': 'Brigadeiro com três sabores clássicos em um só: chocolate, morango e creme.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/napolitano.png'
    },
    {
        'name': 'Brigadeiro Ninho',
        'description': 'Brigadeiro cremoso de Leite Ninho.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/ninho.png'
    },
    {
        'name': 'Brigadeiro Ferrero',
        'description': 'Brigadeiro com o sabor irresistível do chocolate Ferrero.',
        'price': 6.00,
        'stock': 100,
        'category': 'brigadeiros',
        'sizes': ['18g - unidade', '10g - 50un', '10g - 100un', '18g - 50un', '18g - 100un'],
        'prices': [6.00, 120.00, 220.00, 18.00, 30.00, 250.00, 480.00],
        'image': 'imagens/ferrero.png'
    },
    {
        'name': 'Coxinha de Morango Tradicional',
        'description': 'Coxinha de morango gourmet. Confira a disponibilidade!',
        'price': 8.00,
        'stock': 50,
        'category': 'coxinhas',
        'sizes': ['1 unidade', 'Caixinha c/ 2 (2 sabores)', 'Caixinha c/ 4', 'Kit Festa 100un (2 sabores)'],
        'prices': [8.00, 16.00, 32.00, 300.00],
        'image': 'imagens/coxinha-trad.png'
    },
    {
        'name': 'Coxinha de Morango Ninho',
        'description': 'Coxinha de morango com recheio de Leite Ninho. Confira a disponibilidade!',
        'price': 8.00,
        'stock': 50,
        'category': 'coxinhas',
        'sizes': ['1 unidade', 'Caixinha c/ 2 (2 sabores)', 'Caixinha c/ 4', 'Kit Festa 100un (2 sabores)'],
        'prices': [8.00, 16.00, 32.00, 300.00],
        'image': 'imagens/coxinha-ninho.png'
    },
    {
        'name': 'Torta no Pote Oreo (120g)',
        'description': 'Deliciosa torta no pote sabor Oreo.',
        'price': 16.00,
        'stock': 30,
        'category': 'tortas',
        'sizes': ['120g'],
        'prices': [16.00],
        'image': 'imagens/torta-oreo.png'
    },
    {
        'name': 'Torta no Pote Prestígio (120g)',
        'description': 'Torta no pote com o clássico sabor Prestígio: chocolate e coco.',
        'price': 16.00,
        'stock': 30,
        'category': 'tortas',
        'sizes': ['120g'],
        'prices': [16.00],
        'image': 'imagens/torta-prestigio.png'
    },
    {
        'name': 'Torta no Pote Limão (120g)',
        'description': 'Torta no pote refrescante de limão com o toque de merengue.',
        'price': 16.00,
        'stock': 30,
        'category': 'tortas',
        'sizes': ['120g'],
        'prices': [16.00],
        'image': 'imagens/torta-limão.png'
    },
]

# Create products
for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults={
            'description': product_data['description'],
            'price': product_data['price'],
            'stock': product_data['stock'],
            'created_by': admin_profile
        }
    )
    if created:
        print(f"Created product: {product.name}")
    else:
        print(f"Product already exists: {product.name}")

print("Product population completed!")
print(f"Total products in database: {Product.objects.count()}")
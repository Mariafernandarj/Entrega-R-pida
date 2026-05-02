"""
Cómo correrlo:
    python manage.py poblar_datos
    python manage.py poblar_datos 
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from solicitudes_reparto.models import Pedido, Restaurante, Repartidor, Producto, DetallePedido


class Command(BaseCommand):
    help = 'Crea datos ficticios para probar el caso de uso de aceptar solicitudes de reparto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear los nuevos',
        )

    def handle(self, *args, **options):
        if options['limpiar']:
            self.limpiar_datos()

        self.stdout.write('\n🚀 Creando datos de prueba...\n')

        restaurantes = self.crear_restaurantes()
        productos    = self.crear_productos(restaurantes)
        repartidores = self.crear_repartidores()
        self.crear_pedidos(restaurantes, productos, repartidores)

        self.stdout.write(self.style.SUCCESS('\n✅ Datos de prueba creados correctamente.\n'))
        self.stdout.write('Puedes iniciar sesión con cualquier repartidor:')
        self.stdout.write('  Usuario: repartidor1  Contraseña: test1234')
        self.stdout.write('  Usuario: repartidor2  Contraseña: test1234')
        self.stdout.write('  Usuario: repartidor3  Contraseña: test1234\n')

    # ------------------------------------------------------------------
    # Limpieza
    # ------------------------------------------------------------------
    def limpiar_datos(self):
        self.stdout.write('🗑️  Limpiando datos anteriores...')
        DetallePedido.objects.all().delete()
        Pedido.objects.all().delete()
        Repartidor.objects.all().delete()
        Producto.objects.all().delete()
        Restaurante.objects.all().delete()
        User.objects.filter(username__startswith='repartidor').delete()
        self.stdout.write(self.style.WARNING('   Datos eliminados.\n'))

    # ------------------------------------------------------------------
    # Restaurantes
    # ------------------------------------------------------------------
    def crear_restaurantes(self):
        self.stdout.write('🍔 Creando restaurantes...')
        datos = [
            {'nombre': "McDonald's",  'direccion': 'Av. Insurgentes 100'},
            {'nombre': 'Domino\'s',   'direccion': 'Calle Reforma 45'},
            {'nombre': 'KFC',         'direccion': 'Blvd. Juárez 200'},
        ]
        restaurantes = []
        for d in datos:
            r, creado = Restaurante.objects.get_or_create(nombre=d['nombre'], defaults=d)
            restaurantes.append(r)
            estado = 'creado' if creado else 'ya existía'
            self.stdout.write(f'   {r.nombre} ({estado})')
        return restaurantes

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def crear_productos(self, restaurantes):
        self.stdout.write('🥤 Creando productos...')
        catalogo = {
            "McDonald's": [
                ('Hamburguesa Big Mac',   89.00),
                ('McPollo',               79.00),
                ('Papas grandes',         45.00),
                ('McFlurry Oreo',         55.00),
            ],
            "Domino's": [
                ('Pizza Pepperoni',      149.00),
                ('Pizza Hawaiana',       139.00),
                ('Palitos de pan',        59.00),
            ],
            'KFC': [
                ('Combo 2 piezas',       119.00),
                ('Alitas BBQ x6',         99.00),
                ('Puré de papa',          35.00),
            ],
        }
        productos = {}
        for restaurante in restaurantes:
            productos[restaurante.nombre] = []
            for nombre, precio in catalogo.get(restaurante.nombre, []):
                p, creado = Producto.objects.get_or_create(
                    nombre=nombre,
                    restaurante=restaurante,
                    defaults={'precio': precio}
                )
                productos[restaurante.nombre].append(p)
        return productos

    # ------------------------------------------------------------------
    # Repartidores
    # ------------------------------------------------------------------
    def crear_repartidores(self):
        self.stdout.write('🛵 Creando repartidores...')
        datos = [
            {'username': 'repartidor1', 'nombre': 'Carlos López'},
            {'username': 'repartidor2', 'nombre': 'Ana García'},
            {'username': 'repartidor3', 'nombre': 'Luis Martínez'},
        ]
        repartidores = []
        for d in datos:
            user, creado = User.objects.get_or_create(username=d['username'])
            if creado:
                user.set_password('test1234')
                user.save()

            rep, _ = Repartidor.objects.get_or_create(
                user=user,
                defaults={'nombre': d['nombre']}
            )
            repartidores.append(rep)
            self.stdout.write(f'   {rep.nombre} (usuario: {user.username})')
        return repartidores

    # ------------------------------------------------------------------
    # Pedidos
    # ------------------------------------------------------------------
    def crear_pedidos(self, restaurantes, productos, repartidores):
        self.stdout.write('📦 Creando pedidos...')

        mcdonalds = next(r for r in restaurantes if r.nombre == "McDonald's")
        dominos   = next(r for r in restaurantes if r.nombre == "Domino's")
        kfc       = next(r for r in restaurantes if r.nombre == 'KFC')

        # ── Pedidos PENDIENTES (aparecen en solicitudes_de_reparto) ──────
        pendientes = [
            {
                'restaurante': mcdonalds,
                'productos': [('Hamburguesa Big Mac', 1), ('Papas grandes', 2)],
                'estado': 'pendiente',
            },
            {
                'restaurante': dominos,
                'productos': [('Pizza Pepperoni', 1), ('Palitos de pan', 1)],
                'estado': 'pendiente',
            },
            {
                'restaurante': kfc,
                'productos': [('Combo 2 piezas', 2)],
                'estado': 'pendiente',
            },
            {
                'restaurante': mcdonalds,
                'productos': [('McPollo', 1), ('McFlurry Oreo', 1)],
                'estado': 'pendiente',
            },
        ]

        # ── Pedido EXPIRADO (para probar el flujo alternativo) ───────────
        expirado = [
            {
                'restaurante': dominos,
                'productos': [('Pizza Hawaiana', 1)],
                'estado': 'pendiente',
                'fecha_limite': timezone.now() - timedelta(minutes=1),  # ya expiró
            },
        ]

        # ── Pedido ya ACEPTADO por repartidor1 (aparece en ver_pedidos) ──
        aceptado = [
            {
                'restaurante': kfc,
                'productos': [('Alitas BBQ x6', 1), ('Puré de papa', 1)],
                'estado': 'aceptado',
                'repartidor': repartidores[0],
            },
        ]

        for config in pendientes + expirado + aceptado:
            pedido = Pedido(
                restaurante=config['restaurante'],
                estado=config['estado'],
                repartidor=config.get('repartidor'),
            )
            if 'fecha_limite' in config:
                pedido.fecha_limite = config['fecha_limite']
            pedido.save()

            # Crear detalles del pedido
            for nombre_prod, cantidad in config['productos']:
                restaurante_nombre = config['restaurante'].nombre
                prod_lista = productos.get(restaurante_nombre, [])
                producto = next((p for p in prod_lista if p.nombre == nombre_prod), None)
                if producto:
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad
                    )

            self.stdout.write(
                f'   Pedido #{pedido.id} | {pedido.restaurante.nombre} '
                f'| estado: {pedido.estado}'
                + (f' | repartidor: {pedido.repartidor}' if pedido.repartidor else '')
            )

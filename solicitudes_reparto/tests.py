# Create your tests here.
# edicion_pedido/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Pedido


class PedidoModelTest(TestCase):

    def test_estado_default_es_pendiente(self):
        pedido = Pedido.objects.create()
        self.assertEqual(pedido.estado, 'pendiente')

    def test_str_pedido(self):
        pedido = Pedido.objects.create(estado='asignado')
        self.assertIn('asignado', str(pedido))


class EditarEstadoPedidoViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass1234')
        self.pedido = Pedido.objects.create(estado='pendiente')

    def test_redirige_si_no_autenticado(self):
        url = reverse('editar_estado_pedido', args=[self.pedido.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_actualiza_estado_correctamente(self):
        self.client.login(username='tester', password='pass1234')
        url = reverse('editar_estado_pedido', args=[self.pedido.id])
        response = self.client.post(url, {'estado': 'asignado'})
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'asignado')

    def test_estado_invalido_no_guarda(self):
        self.client.login(username='tester', password='pass1234')
        url = reverse('editar_estado_pedido', args=[self.pedido.id])
        self.client.post(url, {'estado': 'estado_inventado'})
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'pendiente')

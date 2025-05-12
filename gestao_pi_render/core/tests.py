from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase # Para testar views da API
from .models import Cliente, Produto
from .serializers import ClienteSerializer # Importe seus serializers
from django.utils import timezone
import datetime

class ClienteModelTests(APITestCase):
    def test_criar_cliente(self):
        """ Testa a criação de um objeto Cliente. """
        cliente = Cliente.objects.create(
            nome="Cliente Teste Modelo",
            email="modelo@teste.com",
            telefone="123456789"
        )
        self.assertEqual(cliente.nome, "Cliente Teste Modelo")
        self.assertEqual(str(cliente), "Cliente Teste Modelo") # Testa o __str__

class ProdutoModelTests(APITestCase):
    def test_criar_produto(self):
        """ Testa a criação de um objeto Produto. """
        produto = Produto.objects.create(
            nome="Produto Teste Modelo",
            preco=19.99,
            estoque=50
        )
        self.assertEqual(produto.nome, "Produto Teste Modelo")
        self.assertEqual(produto.preco, 19.99)

class ClienteAPITests(APITestCase):
    def setUp(self):
        # Dados de exemplo para serem usados nos testes da API
        self.cliente1 = Cliente.objects.create(nome='João Silva', email='joao.silva@example.com', telefone='11999998888')
        self.cliente2 = Cliente.objects.create(nome='Maria Oliveira', email='maria.oliveira@example.com', data_cadastro=timezone.now() - datetime.timedelta(days=10))

        self.valid_payload = {
            'nome': 'Carlos Pereira',
            'email': 'carlos.pereira@example.com',
            'telefone': '21988887777'
        }
        self.invalid_payload_sem_email = { # Email faltando (obrigatório)
            'nome': 'Ana Costa',
            'telefone': '31977776666'
        }

    def test_listar_clientes_api(self):
        """ Testa se a listagem de clientes (GET /api/clientes/) funciona. """
        url = reverse('cliente-list') # 'cliente-list' é o nome padrão gerado pelo router para o ViewSet
        response = self.client.get(url)
        
        clientes_qs = Cliente.objects.all()
        serializer = ClienteSerializer(clientes_qs, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DRF pode paginar, então comparamos o array 'results' se existir
        response_data = response.data.get('results', response.data)
        self.assertEqual(response_data, serializer.data)
        self.assertEqual(len(response_data), 2)

    def test_criar_cliente_api_valido(self):
        """ Testa a criação de um novo cliente com dados válidos via API. """
        url = reverse('cliente-list')
        response = self.client.post(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 3)
        # Verifica se o último cliente criado tem o email do payload
        ultimo_cliente = Cliente.objects.get(email=self.valid_payload['email'])
        self.assertEqual(ultimo_cliente.nome, self.valid_payload['nome'])

    def test_criar_cliente_api_invalido(self):
        """ Testa a criação de um cliente com dados inválidos via API. """
        url = reverse('cliente-list')
        response = self.client.post(url, self.invalid_payload_sem_email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data) # Verifica se o erro é relacionado ao campo email

class ChartDataAPITests(APITestCase):
    def setUp(self):
        # Criar alguns clientes com datas de cadastro em meses/anos diferentes
        Cliente.objects.create(nome="Cliente Jan24", email="jan24@ex.com", data_cadastro=datetime.datetime(2024, 1, 15, tzinfo=datetime.timezone.utc))
        Cliente.objects.create(nome="Cliente Fev24", email="fev24@ex.com", data_cadastro=datetime.datetime(2024, 2, 10, tzinfo=datetime.timezone.utc))
        Cliente.objects.create(nome="Cliente Fev24_2", email="fev24_2@ex.com", data_cadastro=datetime.datetime(2024, 2, 20, tzinfo=datetime.timezone.utc))
        Cliente.objects.create(nome="Cliente Mar25", email="mar25@ex.com", data_cadastro=datetime.datetime(2025, 3, 5, tzinfo=datetime.timezone.utc))

    def test_clientes_por_mes_chart_data_api(self):
        """ Testa o endpoint de dados do gráfico de clientes por mês/ano. """
        url = reverse('api-chart-clientes-mes') # Use o nome que você definiu nas URLs
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json() # Converte a resposta JSON para um dicionário Python
        
        self.assertIn('labels', data)
        self.assertIn('data', data)
        self.assertIn('title', data)
        
        # Verificações mais específicas baseadas nos dados do setUp
        # Esperamos: Jan/2024 (1), Fev/2024 (2), Mar/2025 (1)
        expected_labels = ["Jan/2024", "Fev/2024", "Mar/2025"]
        expected_data_counts = [1, 2, 1]
        
        self.assertEqual(data['labels'], expected_labels)
        self.assertEqual(data['data'], expected_data_counts)
        self.assertEqual(data['title'], 'Novos Clientes por Mês/Ano')

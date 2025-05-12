from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import JsonResponse
from django.shortcuts import render # Para renderizar templates HTML
from .models import Cliente, Produto
from .serializers import ClienteSerializer, ProdutoSerializer
import datetime

class ClienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Clientes.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para Produtos.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# View para dados do gráfico de clientes
def clientes_por_mes_chart_data_api(request):
    """
    Fornece dados agregados de novos clientes por mês/ano para a API.
    Exemplo: { "labels": ["Jan/2024", "Fev/2024"], "data": [10, 15] }
    """
    # Mapear número do mês para nome abreviado em português
    meses_pt_br = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
# Considerar filtrar por um período específico se houver muitos dados
# Por exemplo, os últimos 12 meses.
# current_year = datetime.date.today().year
# queryset = Cliente.objects.filter(data_cadastro__year=current_year)
    
    queryset = Cliente.objects.all()

    data_agregada = queryset.annotate(
        ano=ExtractYear('data_cadastro'),
        mes=ExtractMonth('data_cadastro')
    ).values('ano', 'mes').annotate(
        total=Count('id')
    ).order_by('ano', 'mes')

    labels = []
    data_counts = []

    for item in data_agregada:
        labels.append(f"{meses_pt_br.get(item['mes'], str(item['mes']))}/{item['ano']}")
        data_counts.append(item['total'])
    
    # Se não houver dados, retorna listas vazias ou dados de exemplo
    if not data_agregada:
        # Exemplo de dados se não houver clientes
        # labels = ["Nenhum Cliente"] 
        # data_counts = [0]
        pass


    return JsonResponse({
        'labels': labels,
        'data': data_counts,
        'title': 'Novos Clientes por Mês/Ano'
    })
# View para a página do dashboard (HTML)
def dashboard_view(request):
    """
    Renderiza a página de dashboard que pode incluir os gráficos.
    """
    # Você pode buscar dados aqui para passar ao template, se necessário,
    # ou o template pode fazer chamadas AJAX para os endpoints da API.
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()
    context = {
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
        'endpoint_grafico_clientes': '/api/charts/clientes-por-mes/' # Passa o endpoint para o JS
    }
    return render(request, 'core/dashboard.html', context)
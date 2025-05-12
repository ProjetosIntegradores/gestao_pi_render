from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, 
    ProdutoViewSet, 
    clientes_por_mes_chart_data_api,
    dashboard_view
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'produtos', ProdutoViewSet, basename='produto')

urlpatterns = [
    path('api/', include(router.urls)), # APIs CRUD
    path('api/charts/clientes-por-mes/', clientes_por_mes_chart_data_api, name='api-chart-clientes-mes'),
    
    # URL para a página do dashboard HTML
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', dashboard_view, name='home'), # Tornar o dashboard a página inicial
]
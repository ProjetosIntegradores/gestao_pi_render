from django.contrib import admin
from .models import Cliente, Produto

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'email')
    list_filter = ('data_cadastro',)
    date_hierarchy = 'data_cadastro'

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'data_criacao')
    search_fields = ('nome',)
    list_filter = ('data_criacao',)
    ordering = ('nome',)

# Register your models here.

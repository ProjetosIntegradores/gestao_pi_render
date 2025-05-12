from rest_framework import serializers
from .models import Cliente, Produto

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'telefone', 'data_cadastro']
        read_only_fields = ['id', 'data_cadastro']

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'data_criacao']
        read_only_fields = ['id', 'data_criacao']
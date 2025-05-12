# gestao_pi_render/build.sh
# Script que o Render executará para construir sua aplicação.

#!/usr/bin/env bash
# Sair em caso de erro
set -o errexit

echo "Instalando dependências Python..."
pip install -r requirements.txt

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Aplicando migrações do banco de dados..."
python manage.py migrate # As migrações só devem rodar se o banco estiver pronto

echo "Build finalizado."

# Certifique-se de que este arquivo é executável:
# chmod +x build.sh
#!/bin/bash

echo "========================================"
echo "  API de Cadastro de Pessoas - Docker"
echo "========================================"
echo ""

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "Por favor, instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verifica se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não está instalado!"
    echo "Por favor, instale o Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"
echo ""

# Para serviços existentes do supervisor (se estiverem rodando)
echo "📋 Parando serviços supervisor (se existirem)..."
sudo supervisorctl stop backend frontend 2>/dev/null || true
echo ""

# Remove containers antigos se existirem
echo "🧹 Limpando containers antigos..."
docker-compose down 2>/dev/null || true
echo ""

# Constrói as imagens
echo "🔨 Construindo imagens Docker..."
echo "   Isso pode levar alguns minutos na primeira vez..."
echo ""
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagens Docker"
    exit 1
fi

echo ""
echo "✅ Imagens construídas com sucesso"
echo ""

# Inicia os containers
echo "🚀 Iniciando containers..."
echo ""
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Erro ao iniciar containers"
    exit 1
fi

echo ""
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 5

# Verifica status dos containers
echo ""
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "========================================"
echo "  ✅ Aplicação iniciada com sucesso!"
echo "========================================"
echo ""
echo "🌐 Serviços disponíveis:"
echo ""
echo "   📱 Frontend:     http://localhost:3000"
echo "   🔧 Backend API:  http://localhost:8001"
echo "   📚 Documentação: http://localhost:8001/docs"
echo "   🗄️  MongoDB:      mongodb://localhost:27017"
echo ""
echo "📋 Comandos úteis:"
echo ""
echo "   Ver logs:           docker-compose logs -f"
echo "   Ver logs backend:   docker-compose logs -f backend"
echo "   Ver logs frontend:  docker-compose logs -f frontend"
echo "   Parar aplicação:    docker-compose down"
echo "   Reiniciar:          docker-compose restart"
echo "   Status:             docker-compose ps"
echo ""
echo "========================================"

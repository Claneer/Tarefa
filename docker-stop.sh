#!/bin/bash

echo "========================================"
echo "  Parando API de Cadastro de Pessoas"
echo "========================================"
echo ""

echo "🛑 Parando containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Aplicação parada com sucesso!"
    echo ""
    echo "💡 Para iniciar novamente: ./docker-start.sh"
    echo "🗑️  Para remover volumes: docker-compose down -v"
else
    echo ""
    echo "❌ Erro ao parar containers"
    exit 1
fi

echo ""

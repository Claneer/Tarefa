#!/bin/bash

echo "========================================"
echo "  Logs da Aplicação"
echo "========================================"
echo ""

if [ -z "$1" ]; then
    echo "📋 Mostrando logs de todos os serviços..."
    echo "   (Ctrl+C para sair)"
    echo ""
    docker-compose logs -f
else
    echo "📋 Mostrando logs do serviço: $1"
    echo "   (Ctrl+C para sair)"
    echo ""
    docker-compose logs -f $1
fi

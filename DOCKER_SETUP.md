# 🐳 Guia de Configuração Docker

## Visão Geral

Esta aplicação agora está completamente dockerizada com 3 serviços:

1. **MongoDB** - Banco de dados
2. **Backend** - API FastAPI (Python)
3. **Frontend** - Interface React (Node.js)

---

## 📋 Pré-requisitos

### Instalar Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS:**
- Baixe e instale: https://docs.docker.com/desktop/install/mac-install/

**Windows:**
- Baixe e instale: https://docs.docker.com/desktop/install/windows-install/

### Instalar Docker Compose

**Linux:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**macOS/Windows:**
- Já incluído no Docker Desktop

### Verificar Instalação

```bash
docker --version
docker-compose --version
```

---

## 🚀 Início Rápido

### Opção 1: Script Automatizado (Recomendado)

```bash
# Dar permissão de execução
chmod +x docker-start.sh docker-stop.sh docker-logs.sh

# Iniciar aplicação
./docker-start.sh
```

Isso irá:
1. ✅ Parar serviços supervisor (se existirem)
2. ✅ Construir imagens Docker
3. ✅ Iniciar todos os containers
4. ✅ Configurar rede entre serviços
5. ✅ Aguardar serviços ficarem prontos

### Opção 2: Manual com Docker Compose

```bash
# Construir imagens
docker-compose build

# Iniciar containers em background
docker-compose up -d

# Ver logs
docker-compose logs -f
```

---

## 🌐 Acessar Aplicação

Após iniciar, os serviços estarão disponíveis em:

| Serviço | URL | Descrição |
|---------|-----|-----------|
| **Frontend** | http://localhost:3000 | Interface React |
| **Backend API** | http://localhost:8001 | API FastAPI |
| **Documentação** | http://localhost:8001/docs | Swagger UI |
| **MongoDB** | mongodb://localhost:27017 | Banco de dados |

---

## 📋 Comandos Úteis

### Gerenciamento Básico

```bash
# Iniciar aplicação
./docker-start.sh
# ou
docker-compose up -d

# Parar aplicação
./docker-stop.sh
# ou
docker-compose down

# Reiniciar aplicação
docker-compose restart

# Parar e remover volumes (APAGA DADOS!)
docker-compose down -v
```

### Ver Logs

```bash
# Todos os serviços
./docker-logs.sh
# ou
docker-compose logs -f

# Apenas backend
./docker-logs.sh backend
# ou
docker-compose logs -f backend

# Apenas frontend
docker-compose logs -f frontend

# Apenas MongoDB
docker-compose logs -f mongodb
```

### Status e Informações

```bash
# Ver status dos containers
docker-compose ps

# Ver uso de recursos
docker stats

# Inspecionar container
docker inspect api-pessoas-backend
```

### Executar Comandos nos Containers

```bash
# Acessar shell do backend
docker-compose exec backend bash

# Acessar shell do frontend
docker-compose exec frontend sh

# Acessar MongoDB
docker-compose exec mongodb mongosh

# Executar comando Python no backend
docker-compose exec backend python -c "print('Hello')"
```

### Reconstruir Imagens

```bash
# Reconstruir todas as imagens
docker-compose build --no-cache

# Reconstruir apenas backend
docker-compose build --no-cache backend

# Reconstruir e reiniciar
docker-compose up -d --build
```

---

## 🔧 Configuração

### Variáveis de Ambiente

#### Backend (`backend/.env` ou `docker-compose.yml`)

```env
MONGO_URL=mongodb://mongodb:27017
DB_NAME=pessoas_db
CORS_ORIGINS=http://localhost:3000
```

#### Frontend (`frontend/.env` ou `docker-compose.yml`)

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Portas

Para alterar portas, edite `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8001"  # Altere 8001 (porta host) conforme necessário
  
  frontend:
    ports:
      - "3000:3000"  # Altere 3000 (porta host) conforme necessário
```

---

## 🧪 Testes

### Testar Backend

```bash
# Healthcheck
curl http://localhost:8001/api/

# Criar pessoa
curl -X POST http://localhost:8001/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678909",
    "nome": "Teste Docker",
    "email": "teste@docker.com",
    "endereco": "Rua Docker, 123"
  }'

# Listar pessoas
curl http://localhost:8001/api/pessoas
```

### Testar MongoDB

```bash
# Conectar ao MongoDB
docker-compose exec mongodb mongosh

# Dentro do mongosh:
use pessoas_db
db.pessoas.find()
```

---

## 🐛 Solução de Problemas

### Container não inicia

```bash
# Ver logs detalhados
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb

# Verificar se portas estão em uso
sudo lsof -i :8001  # Backend
sudo lsof -i :3000  # Frontend
sudo lsof -i :27017 # MongoDB

# Matar processo usando porta
sudo kill -9 <PID>
```

### Erro "port already in use"

```bash
# Parar serviços supervisor
sudo supervisorctl stop backend frontend

# Ou alterar portas no docker-compose.yml
```

### Erro de conexão com MongoDB

```bash
# Verificar se MongoDB está rodando
docker-compose ps mongodb

# Reiniciar MongoDB
docker-compose restart mongodb

# Ver logs do MongoDB
docker-compose logs mongodb
```

### Limpar tudo e começar do zero

```bash
# ATENÇÃO: Isso apaga TODOS os dados!
docker-compose down -v
docker system prune -a
./docker-start.sh
```

### Frontend não atualiza (hot reload)

```bash
# Verificar se volumes estão montados corretamente
docker-compose ps frontend

# Reiniciar frontend
docker-compose restart frontend
```

### Erro de permissão

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Fazer logout e login novamente
# ou
newgrp docker
```

---

## 📊 Arquitetura Docker

```
┌─────────────────────────────────────────────┐
│           app-network (bridge)              │
│                                             │
│  ┌──────────────┐    ┌──────────────┐     │
│  │   Frontend   │────▶│   Backend    │     │
│  │  React:3000  │    │ FastAPI:8001 │     │
│  └──────────────┘    └───────┬──────┘     │
│                              │              │
│                              ▼              │
│                      ┌──────────────┐      │
│                      │   MongoDB    │      │
│                      │   :27017     │      │
│                      └──────────────┘      │
│                                             │
└─────────────────────────────────────────────┘
```

### Volumes

- **mongodb_data** - Persiste dados do MongoDB
- **./backend** - Hot reload do código backend
- **./frontend** - Hot reload do código frontend

### Networks

- **app-network** - Rede bridge para comunicação entre containers

---

## 🔄 Desenvolvimento

### Hot Reload

Ambos backend e frontend têm hot reload ativado:

- **Backend**: Uvicorn com `--reload`
- **Frontend**: React com polling habilitado

Edite arquivos e veja mudanças automaticamente!

### Instalar Novas Dependências

#### Backend (Python)

```bash
# 1. Adicionar ao requirements.txt
echo "nova-lib==1.0.0" >> backend/requirements.txt

# 2. Reconstruir imagem
docker-compose build backend

# 3. Reiniciar container
docker-compose up -d backend
```

#### Frontend (Node.js)

```bash
# 1. Adicionar dependência
docker-compose exec frontend yarn add nome-da-lib

# Ou reconstruir imagem
docker-compose build frontend
docker-compose up -d frontend
```

---

## 📦 Deploy em Produção

### Preparar para Produção

1. **Criar `docker-compose.prod.yml`**
2. **Remover volumes de desenvolvimento**
3. **Usar variáveis de ambiente seguras**
4. **Configurar reverse proxy (nginx)**
5. **Habilitar HTTPS**
6. **Configurar backup do MongoDB**

Exemplo `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    networks:
      - app-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: always
    environment:
      - MONGO_URL=mongodb://${MONGO_USER}:${MONGO_PASSWORD}@mongodb:27017
    networks:
      - app-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: always
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    networks:
      - app-network

volumes:
  mongodb_data:

networks:
  app-network:
```

---

## 📚 Recursos Adicionais

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

---

## ✅ Checklist de Verificação

Após iniciar com `./docker-start.sh`, verifique:

- [ ] 3 containers rodando: `docker-compose ps`
- [ ] Backend responde: `curl http://localhost:8001/api/`
- [ ] Frontend abre: http://localhost:3000
- [ ] Documentação abre: http://localhost:8001/docs
- [ ] MongoDB conecta: `docker-compose exec mongodb mongosh`
- [ ] API CRUD funciona: criar, listar, atualizar, deletar pessoa

---

**🎉 Sua aplicação está completamente dockerizada!**

Para suporte, consulte os logs:
```bash
./docker-logs.sh
```

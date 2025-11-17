# 🏗️ Arquitetura Docker da Aplicação

## 📊 Visão Geral

A aplicação é composta por 3 containers Docker orquestrados pelo Docker Compose:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                        │
│                       (app-network)                             │
│                                                                  │
│  ┌──────────────┐       ┌──────────────┐      ┌─────────────┐  │
│  │  Container 1 │       │  Container 2 │      │ Container 3 │  │
│  │              │       │              │      │             │  │
│  │   Frontend   │──────▶│   Backend    │─────▶│   MongoDB   │  │
│  │              │       │              │      │             │  │
│  │  React:3000  │       │ FastAPI:8001 │      │   :27017    │  │
│  └──────┬───────┘       └──────┬───────┘      └──────┬──────┘  │
│         │                      │                     │          │
└─────────┼──────────────────────┼─────────────────────┼──────────┘
          │                      │                     │
          │                      │                     │
     Porta 3000              Porta 8001            Porta 27017
          │                      │                     │
          └──────────────────────┴─────────────────────┘
                                 │
                          Host Machine
                        (localhost)
```

---

## 🐳 Containers

### 1. Frontend Container (React)

```yaml
Nome: api-pessoas-frontend
Imagem: Construída de ./frontend/Dockerfile
Porta: 3000 → 3000
```

**Responsabilidades:**
- Interface do usuário (React)
- Comunicação com backend via HTTP
- Hot reload em modo desenvolvimento

**Variáveis de Ambiente:**
- `REACT_APP_BACKEND_URL=http://localhost:8001`
- `WATCHPACK_POLLING=true` (para hot reload)
- `CHOKIDAR_USEPOLLING=true` (para hot reload)

**Volumes:**
- `./frontend:/app` - Código fonte montado (hot reload)
- `/app/node_modules` - Dependências isoladas

---

### 2. Backend Container (FastAPI)

```yaml
Nome: api-pessoas-backend
Imagem: Construída de ./backend/Dockerfile
Porta: 8001 → 8001
```

**Responsabilidades:**
- API REST (FastAPI)
- Validação de CPF
- CRUD de pessoas
- Comunicação com MongoDB

**Variáveis de Ambiente:**
- `MONGO_URL=mongodb://mongodb:27017`
- `DB_NAME=pessoas_db`
- `CORS_ORIGINS=http://localhost:3000`

**Volumes:**
- `./backend:/app` - Código fonte montado (hot reload)

**Dependências:**
- Aguarda MongoDB estar saudável (healthcheck)

---

### 3. MongoDB Container (Database)

```yaml
Nome: api-pessoas-mongodb
Imagem: mongo:7.0 (oficial)
Porta: 27017 → 27017
```

**Responsabilidades:**
- Armazenamento de dados
- Persistência de pessoas cadastradas

**Variáveis de Ambiente:**
- `MONGO_INITDB_DATABASE=pessoas_db`

**Volumes:**
- `mongodb_data:/data/db` - Persistência de dados

**Healthcheck:**
- Comando: `mongosh` ping
- Intervalo: 10s
- Timeout: 5s
- Retries: 5

---

## 🔄 Fluxo de Dados

### Criar Pessoa (POST /api/pessoas)

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Frontend │      │ Backend  │      │ MongoDB  │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                 │
     │ 1. POST dados   │                 │
     │────────────────▶│                 │
     │                 │                 │
     │                 │ 2. Valida CPF   │
     │                 │───────────┐     │
     │                 │◀──────────┘     │
     │                 │                 │
     │                 │ 3. Insert doc   │
     │                 │────────────────▶│
     │                 │                 │
     │                 │ 4. Confirma     │
     │                 │◀────────────────│
     │                 │                 │
     │ 5. Retorna JSON │                 │
     │◀────────────────│                 │
     │                 │                 │
```

### Listar Pessoas (GET /api/pessoas)

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Frontend │      │ Backend  │      │ MongoDB  │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                 │
     │ 1. GET request  │                 │
     │────────────────▶│                 │
     │                 │                 │
     │                 │ 2. Find all     │
     │                 │────────────────▶│
     │                 │                 │
     │                 │ 3. Array docs   │
     │                 │◀────────────────│
     │                 │                 │
     │ 4. Array JSON   │                 │
     │◀────────────────│                 │
     │                 │                 │
```

---

## 🌐 Rede Docker

### app-network (Bridge)

Todos os containers estão conectados à mesma rede bridge:

```yaml
networks:
  app-network:
    driver: bridge
```

**Benefícios:**
- Containers podem se comunicar pelo nome
- Isolamento da rede host
- DNS automático (ex: `mongodb`, `backend`, `frontend`)

**Resolução de Nomes:**
- `mongodb` → Container MongoDB
- `backend` → Container Backend
- `frontend` → Container Frontend

---

## 💾 Volumes

### mongodb_data (Persistente)

```yaml
volumes:
  mongodb_data:
    driver: local
```

**Características:**
- Persiste dados mesmo após `docker-compose down`
- Sobrevive a reinicializações
- Localizado em `/var/lib/docker/volumes/`

**Para remover:**
```bash
docker-compose down -v  # ⚠️ APAGA DADOS!
```

### Volume de Código (Hot Reload)

```yaml
volumes:
  - ./backend:/app      # Backend
  - ./frontend:/app     # Frontend
```

**Características:**
- Monta código fonte no container
- Mudanças refletem imediatamente (hot reload)
- Facilita desenvolvimento

---

## 🔍 Healthchecks

### MongoDB Healthcheck

```yaml
healthcheck:
  test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
  interval: 10s
  timeout: 5s
  retries: 5
```

**Status:**
- ✅ Healthy: MongoDB aceita conexões
- ❌ Unhealthy: Backend não inicia

### Backend Healthcheck

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8001/api/"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Status:**
- ✅ Healthy: API respondendo
- ❌ Unhealthy: Frontend aguarda

---

## 🚦 Ordem de Inicialização

```
1. MongoDB (inicia primeiro)
   ↓
   Aguarda healthcheck (até 50s)
   ↓
2. Backend (inicia após MongoDB healthy)
   ↓
   Aguarda healthcheck (até 50s)
   ↓
3. Frontend (inicia após Backend healthy)
   ↓
   Aplicação pronta!
```

**Configuração no docker-compose.yml:**

```yaml
backend:
  depends_on:
    mongodb:
      condition: service_healthy

frontend:
  depends_on:
    backend:
      condition: service_healthy
```

---

## 🔐 Variáveis de Ambiente

### Backend

| Variável | Valor | Descrição |
|----------|-------|-----------|
| MONGO_URL | mongodb://mongodb:27017 | Conexão MongoDB |
| DB_NAME | pessoas_db | Nome do banco |
| CORS_ORIGINS | http://localhost:3000 | CORS permitido |

### Frontend

| Variável | Valor | Descrição |
|----------|-------|-----------|
| REACT_APP_BACKEND_URL | http://localhost:8001 | URL da API |
| WATCHPACK_POLLING | true | Hot reload |
| CHOKIDAR_USEPOLLING | true | Hot reload |

---

## 📦 Dockerfiles

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y gcc

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

**Características:**
- Imagem base: Python 3.11 slim
- Instala GCC para compilar dependências
- Modo desenvolvimento com `--reload`

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copia e instala dependências
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copia código
COPY . .

EXPOSE 3000

CMD ["yarn", "start"]
```

**Características:**
- Imagem base: Node 18 Alpine (leve)
- Usa Yarn para gerenciar dependências
- Modo desenvolvimento com hot reload

---

## 🎯 Fluxo Completo de Request

### Exemplo: Criar Pessoa

```
User Browser
    ↓ [1] Acessa http://localhost:3000
    │
┌───▼──────────────────────────┐
│   Frontend Container         │
│   React App (Port 3000)      │
└───┬──────────────────────────┘
    ↓ [2] POST http://localhost:8001/api/pessoas
    │     { "cpf": "...", "nome": "..." }
    │
┌───▼──────────────────────────┐
│   Backend Container          │
│   FastAPI (Port 8001)        │
│                              │
│   1. Valida CPF              │
│   2. Valida dados (Pydantic) │
│   3. Verifica CPF único      │
└───┬──────────────────────────┘
    ↓ [3] db.pessoas.insert_one({...})
    │
┌───▼──────────────────────────┐
│   MongoDB Container          │
│   Database (Port 27017)      │
│                              │
│   Collection: pessoas        │
│   Document: {...}            │
└───┬──────────────────────────┘
    │ [4] Confirma inserção
    ↓
┌───▼──────────────────────────┐
│   Backend Container          │
│   Retorna JSON               │
└───┬──────────────────────────┘
    │ [5] Response 201 Created
    ↓
┌───▼──────────────────────────┐
│   Frontend Container         │
│   Atualiza UI                │
└───┬──────────────────────────┘
    ↓ [6] Mostra mensagem sucesso
User Browser
```

---

## 🔧 Manutenção

### Backup do MongoDB

```bash
# Exportar dados
docker-compose exec mongodb mongodump --out /data/backup

# Copiar para host
docker cp api-pessoas-mongodb:/data/backup ./backup

# Restaurar
docker-compose exec mongodb mongorestore /data/backup
```

### Atualizar Dependências

**Backend:**
```bash
# Adicionar ao requirements.txt
echo "nova-lib==1.0.0" >> backend/requirements.txt

# Reconstruir
docker-compose build backend
docker-compose up -d backend
```

**Frontend:**
```bash
# Instalar no container
docker-compose exec frontend yarn add nova-lib

# Ou reconstruir
docker-compose build frontend
docker-compose up -d frontend
```

### Ver Logs

```bash
# Todos os containers
docker-compose logs -f

# Container específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb

# Últimas 100 linhas
docker-compose logs --tail=100 backend
```

### Estatísticas de Recursos

```bash
# Uso de CPU/Memória em tempo real
docker stats api-pessoas-frontend api-pessoas-backend api-pessoas-mongodb

# Espaço em disco
docker system df
```

---

## 🎨 Diagrama de Arquitetura Completo

```
┌───────────────────────────────────────────────────────────────────────┐
│                         HOST MACHINE (localhost)                       │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │              DOCKER COMPOSE - app-network (bridge)              │  │
│  │                                                                 │  │
│  │  ┌──────────────────┐   ┌──────────────────┐   ┌────────────┐ │  │
│  │  │   Container 1    │   │   Container 2    │   │Container 3 │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  │    Frontend      │   │     Backend      │   │  MongoDB   │ │  │
│  │  │   (React App)    │   │  (FastAPI)       │   │  (DB)      │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  │  ┌────────────┐  │   │  ┌────────────┐  │   │ ┌────────┐ │ │  │
│  │  │  │Node 18     │  │   │  │Python 3.11 │  │   │ │Mongo 7 │ │ │  │
│  │  │  │Alpine      │  │   │  │Slim        │  │   │ │        │ │ │  │
│  │  │  └────────────┘  │   │  └────────────┘  │   │ └────────┘ │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  │  Port: 3000      │   │  Port: 8001      │   │ Port:27017 │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  │  Volume:         │   │  Volume:         │   │ Volume:    │ │  │
│  │  │  ./frontend:/app │   │  ./backend:/app  │   │ mongodb_   │ │  │
│  │  │                  │   │                  │   │ data       │ │  │
│  │  │                  │   │                  │   │ (persist)  │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  │  Healthcheck: -  │   │  Healthcheck:    │   │Healthcheck │ │  │
│  │  │                  │   │  curl /api/      │   │mongosh     │ │  │
│  │  │                  │   │                  │   │ping        │ │  │
│  │  │  depends_on:     │   │  depends_on:     │   │            │ │  │
│  │  │  - backend       │   │  - mongodb       │   │  (start    │ │  │
│  │  │    (healthy)     │   │    (healthy)     │   │   first)   │ │  │
│  │  │                  │   │                  │   │            │ │  │
│  │  └────────┬─────────┘   └────────┬─────────┘   └──────┬─────┘ │  │
│  │           │                      │                    │       │  │
│  │           │   HTTP requests      │   MongoDB          │       │  │
│  │           └─────────────────────▶│   queries          │       │  │
│  │                                  └───────────────────▶│       │  │
│  │                                                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                        │
│  Port Mapping:                                                         │
│  - 3000:3000  (Frontend)                                               │
│  - 8001:8001  (Backend)                                                │
│  - 27017:27017 (MongoDB)                                               │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
           │                    │                    │
           │                    │                    │
      Port 3000            Port 8001           Port 27017
           │                    │                    │
           ▼                    ▼                    ▼
    ┌───────────┐        ┌───────────┐       ┌────────────┐
    │  Browser  │        │  API      │       │ MongoDB    │
    │  Access   │        │  Requests │       │ Client     │
    └───────────┘        └───────────┘       └────────────┘
```

---

## 📚 Referências

- **Docker Compose**: https://docs.docker.com/compose/
- **Docker Networks**: https://docs.docker.com/network/
- **Docker Volumes**: https://docs.docker.com/storage/volumes/
- **Healthchecks**: https://docs.docker.com/compose/compose-file/compose-file-v3/#healthcheck

---

**🏗️ Arquitetura Docker robusta e escalável!**

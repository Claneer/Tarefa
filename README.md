# API de Cadastro de Pessoas com Validação de CPF

## 🐳 Execução com Docker (Recomendado)

### Início Rápido

```bash
# Iniciar toda a aplicação (backend + frontend + MongoDB)
./docker-start.sh
```

Acesse:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001/api/
- **Documentação**: http://localhost:8001/docs

### Comandos Docker

```bash
# Iniciar aplicação
./docker-start.sh

# Parar aplicação
./docker-stop.sh

# Ver logs
./docker-logs.sh

# Ver logs de um serviço específico
./docker-logs.sh backend
./docker-logs.sh frontend
./docker-logs.sh mongodb
```

### Requisitos

- Docker instalado
- Docker Compose instalado

Ver guia completo: [DOCKER_SETUP.md](DOCKER_SETUP.md)

---

## 📋 Descrição do Projeto

API RESTful desenvolvida em Python (FastAPI) com validação de CPF brasileiro, demonstrando os conceitos **DRY (Don't Repeat Yourself)** e **KISS (Keep It Simple, Stupid)**.

### Funcionalidades

✅ CRUD completo (Create, Read, Update, Delete)  
✅ Validação robusta de CPF brasileiro  
✅ MongoDB em Docker  
✅ Validação de email automática  
✅ Timestamps automáticos  
✅ Exemplos de DRY e KISS (violações e boas práticas)

---

## 🛠️ Tecnologias

- **Python 3.11** + **FastAPI**
- **React** (Frontend)
- **MongoDB** (Database)
- **Docker** + **Docker Compose**
- **Pydantic** (Validação)

---

## 📚 Documentação Completa

### Guias Principais

1. **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Guia completo Docker
2. **[EVIDENCIAS.md](EVIDENCIAS.md)** - Conceitos DRY e KISS detalhados
3. **[TESTES_REALIZADOS.md](TESTES_REALIZADOS.md)** - Relatório de testes
4. **[README_API.md](README_API.md)** - Documentação da API

### Arquivos de Código

- **`backend/server.py`** ✅ - Implementação com boas práticas
- **`backend/exemplos_violacoes.py`** ❌ - Exemplos de código ruim

---

## 🎓 Conceitos Demonstrados

### DRY (Don't Repeat Yourself)

**Violação**: Código duplicado em 3 funções (90+ linhas)  
**Boa Prática**: Função centralizada reutilizada (30 linhas) = **67% menos código**

### KISS (Keep It Simple, Stupid)

**Violação**: Classe complexa com 150+ linhas e 12 métodos  
**Boa Prática**: Função simples com 25 linhas = **83% menos complexidade**

Ver exemplos completos em [EVIDENCIAS.md](EVIDENCIAS.md)

---

## 🧪 Testes

10 testes executados com **100% de sucesso**:

1. ✅ Criar pessoa com CPF válido
2. ✅ Rejeitar CPF inválido
3. ✅ Criar com CPF formatado
4. ✅ Listar todas as pessoas
5. ✅ Buscar por CPF
6. ✅ Atualizar dados
7. ✅ Rejeitar CPF duplicado
8. ✅ Rejeitar dígitos repetidos
9. ✅ Deletar pessoa
10. ✅ Verificar lista após deleção

---

## 📖 Exemplos de Uso da API

### Criar Pessoa

```bash
curl -X POST http://localhost:8001/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678909",
    "nome": "João Silva",
    "email": "joao@email.com",
    "endereco": "Rua Exemplo, 123 - São Paulo/SP"
  }'
```

### Listar Pessoas

```bash
curl http://localhost:8001/api/pessoas
```

### Buscar por CPF

```bash
curl http://localhost:8001/api/pessoas/12345678909
```

### Atualizar Pessoa

```bash
curl -X PUT http://localhost:8001/api/pessoas/12345678909 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@email.com",
    "endereco": "Novo endereço"
  }'
```

### Deletar Pessoa

```bash
curl -X DELETE http://localhost:8001/api/pessoas/12345678909
```

---

## 🎯 Estrutura do Projeto

```
/app/
├── backend/
│   ├── server.py              # ✅ API com boas práticas
│   ├── exemplos_violacoes.py  # ❌ Exemplos de código ruim
│   ├── Dockerfile             # 🐳 Imagem Docker backend
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── Dockerfile             # 🐳 Imagem Docker frontend
│   └── package.json
│
├── docker-compose.yml         # 🐳 Orquestração de containers
├── docker-start.sh            # 🚀 Script para iniciar
├── docker-stop.sh             # 🛑 Script para parar
├── docker-logs.sh             # 📋 Script para ver logs
│
├── DOCKER_SETUP.md            # 📄 Guia Docker completo
├── EVIDENCIAS.md              # 📄 Documentação DRY/KISS
├── TESTES_REALIZADOS.md       # 📄 Relatório de testes
├── README_API.md              # 📄 Documentação da API
└── README.md                  # 📄 Este arquivo
```

---

## 🐛 Solução de Problemas

### Erro "port already in use"

```bash
# Parar serviços supervisor
sudo supervisorctl stop backend frontend

# Ou alterar portas no docker-compose.yml
```

### Container não inicia

```bash
# Ver logs
./docker-logs.sh backend
./docker-logs.sh frontend

# Reconstruir imagens
docker-compose build --no-cache
docker-compose up -d
```

### Limpar e reiniciar

```bash
# ATENÇÃO: Apaga dados do banco!
docker-compose down -v
./docker-start.sh
```

---

## 📞 Suporte

**Ver logs em tempo real:**
```bash
./docker-logs.sh
```

**Status dos containers:**
```bash
docker-compose ps
```

**Documentação completa:**
- Docker: [DOCKER_SETUP.md](DOCKER_SETUP.md)
- API: [README_API.md](README_API.md)
- DRY/KISS: [EVIDENCIAS.md](EVIDENCIAS.md)

---

## ✅ Checklist de Verificação

Após executar `./docker-start.sh`:

- [ ] 3 containers rodando
- [ ] Backend responde em http://localhost:8001/api/
- [ ] Frontend abre em http://localhost:3000
- [ ] Documentação em http://localhost:8001/docs
- [ ] MongoDB conectado

---

**Desenvolvido com ❤️ para demonstrar boas práticas de código**

DRY ✅ | KISS ✅ | Docker 🐳

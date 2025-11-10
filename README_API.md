# API de Cadastro de Pessoas com Validação de CPF

API RESTful desenvolvida em Python (FastAPI) com validação de CPF brasileiro, demonstrando os conceitos **DRY (Don't Repeat Yourself)** e **KISS (Keep It Simple, Stupid)**.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Documentação da API](#documentação-da-api)
- [Conceitos DRY e KISS](#conceitos-dry-e-kiss)
- [Testes](#testes)
- [Documentos de Evidência](#documentos-de-evidência)

---

## 🎯 Visão Geral

Esta API permite o cadastro, consulta, atualização e exclusão de pessoas com validação automática de CPF brasileiro. O projeto foi desenvolvido como demonstração prática dos princípios DRY e KISS, incluindo exemplos de violações e boas práticas.

### Características Principais

✅ **CRUD Completo** - Create, Read, Update, Delete  
✅ **Validação de CPF** - Algoritmo completo com dígitos verificadores  
✅ **MongoDB** - Banco de dados em container Docker  
✅ **Async/Await** - Performance otimizada com Motor (driver async)  
✅ **Validações Automáticas** - Pydantic para validação de dados  
✅ **Documentação Interativa** - Swagger UI automático  
✅ **Conceitos DRY e KISS** - Código exemplar e contra-exemplos documentados

---

## 🛠️ Tecnologias

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **MongoDB** - Banco de dados NoSQL (container Docker)
- **Motor** - Driver async para MongoDB
- **Pydantic** - Validação de dados
- **Docker** - Containerização do MongoDB

---

## 🚀 Funcionalidades

### Operações CRUD

1. **Criar Pessoa** - `POST /api/pessoas`
   - Validação automática de CPF
   - Verificação de unicidade
   - Validação de email
   - Timestamps automáticos

2. **Listar Pessoas** - `GET /api/pessoas`
   - Retorna todas as pessoas cadastradas
   - Ordenado por data de criação

3. **Buscar por CPF** - `GET /api/pessoas/{cpf}`
   - Busca específica por CPF
   - Aceita CPF com ou sem formatação

4. **Atualizar Pessoa** - `PUT /api/pessoas/{cpf}`
   - Atualização parcial (campos opcionais)
   - Atualização automática do timestamp
   - CPF não pode ser alterado

5. **Deletar Pessoa** - `DELETE /api/pessoas/{cpf}`
   - Remoção completa do registro
   - Confirmação de deleção

### Validações de CPF

✅ Formato: aceita com ou sem pontos/traços  
✅ Tamanho: exatamente 11 dígitos  
✅ Dígitos repetidos: rejeita (ex: 111.111.111-11)  
✅ Dígitos verificadores: valida com algoritmo oficial  
✅ Unicidade: CPF único no sistema

---

## 📁 Estrutura do Projeto

```
/app/
├── backend/
│   ├── server.py                  # ✅ API principal (BOA PRÁTICA)
│   ├── exemplos_violacoes.py      # ❌ Exemplos de código ruim
│   ├── requirements.txt            # Dependências Python
│   └── .env                        # Configurações
│
├── EVIDENCIAS.md                   # 📄 Documentação completa DRY/KISS
├── TESTES_REALIZADOS.md            # 📋 Relatório de testes
└── README_API.md                   # 📖 Este arquivo
```

### Arquivos Principais

#### ✅ `/app/backend/server.py`
Implementação da API com **BOAS PRÁTICAS**:
- Função `validar_cpf()` centralizada (DRY)
- Endpoints simples e diretos (KISS)
- Código limpo e documentado
- ~400 linhas bem organizadas

#### ❌ `/app/backend/exemplos_violacoes.py`
Exemplos de **VIOLAÇÕES** (apenas didáticos):
- Código duplicado (violação DRY)
- Complexidade desnecessária (violação KISS)
- ~300 linhas de código ruim

#### 📄 `/app/EVIDENCIAS.md`
Documentação completa com:
- Explicação detalhada de DRY e KISS
- Comparação lado a lado (ruim vs bom)
- Exemplos de código
- Guia da API

#### 📋 `/app/TESTES_REALIZADOS.md`
Relatório de testes com:
- 10 testes executados
- Resultados detalhados
- Validação dos conceitos
- 100% de sucesso

---

## ⚙️ Como Executar

### Pré-requisitos

O ambiente já está configurado com:
- ✅ Python 3.11+
- ✅ MongoDB em container Docker
- ✅ Todas as dependências instaladas

### Iniciar a API

```bash
# Backend já está rodando via supervisor
sudo supervisorctl status backend

# Se necessário reiniciar
sudo supervisorctl restart backend
```

### Acessar a API

**Base URL:** `http://localhost:8001`

**Documentação Interativa (Swagger UI):**
```
http://localhost:8001/docs
```

**Healthcheck:**
```bash
curl http://localhost:8001/api/
```

---

## 📚 Documentação da API

### Base URL
```
http://localhost:8001/api
```

---

### 1️⃣ Criar Pessoa

**Endpoint:** `POST /api/pessoas`

**Request Body:**
```json
{
  "cpf": "12345678909",
  "nome": "João Silva",
  "email": "joao@email.com",
  "endereco": "Rua Exemplo, 123 - São Paulo/SP"
}
```

**Response (201 Created):**
```json
{
  "cpf": "12345678909",
  "nome": "João Silva",
  "email": "joao@email.com",
  "endereco": "Rua Exemplo, 123 - São Paulo/SP",
  "created_at": "2025-11-10T16:11:23.709Z",
  "updated_at": "2025-11-10T16:11:23.709Z"
}
```

**Exemplo curl:**
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

---

### 2️⃣ Listar Todas as Pessoas

**Endpoint:** `GET /api/pessoas`

**Response (200 OK):**
```json
[
  {
    "cpf": "12345678909",
    "nome": "João Silva",
    "email": "joao@email.com",
    "endereco": "Rua Exemplo, 123 - São Paulo/SP",
    "created_at": "2025-11-10T16:11:23.709Z",
    "updated_at": "2025-11-10T16:11:23.709Z"
  }
]
```

**Exemplo curl:**
```bash
curl http://localhost:8001/api/pessoas
```

---

### 3️⃣ Buscar Pessoa por CPF

**Endpoint:** `GET /api/pessoas/{cpf}`

**Parâmetros:**
- `cpf` - CPF da pessoa (com ou sem formatação)

**Response (200 OK):**
```json
{
  "cpf": "12345678909",
  "nome": "João Silva",
  "email": "joao@email.com",
  "endereco": "Rua Exemplo, 123 - São Paulo/SP",
  "created_at": "2025-11-10T16:11:23.709Z",
  "updated_at": "2025-11-10T16:11:23.709Z"
}
```

**Exemplos curl:**
```bash
# Sem formatação
curl http://localhost:8001/api/pessoas/12345678909

# Com formatação
curl http://localhost:8001/api/pessoas/123.456.789-09
```

---

### 4️⃣ Atualizar Pessoa

**Endpoint:** `PUT /api/pessoas/{cpf}`

**Request Body (campos opcionais):**
```json
{
  "nome": "João Silva Santos",
  "email": "joao.novo@email.com",
  "endereco": "Rua Nova, 789 - São Paulo/SP"
}
```

**Response (200 OK):**
```json
{
  "cpf": "12345678909",
  "nome": "João Silva Santos",
  "email": "joao.novo@email.com",
  "endereco": "Rua Nova, 789 - São Paulo/SP",
  "created_at": "2025-11-10T16:11:23.709Z",
  "updated_at": "2025-11-10T16:15:00.000Z"
}
```

**Exemplo curl:**
```bash
curl -X PUT http://localhost:8001/api/pessoas/12345678909 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.novo@email.com",
    "endereco": "Rua Nova, 789"
  }'
```

---

### 5️⃣ Deletar Pessoa

**Endpoint:** `DELETE /api/pessoas/{cpf}`

**Response (200 OK):**
```json
{
  "message": "Pessoa com CPF 123.456.789-09 deletada com sucesso",
  "deleted_count": 1
}
```

**Exemplo curl:**
```bash
curl -X DELETE http://localhost:8001/api/pessoas/12345678909
```

---

### Códigos de Status

| Código | Significado |
|--------|------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 400 | Bad Request - CPF duplicado ou inválido |
| 404 | Not Found - Pessoa não encontrada |
| 422 | Unprocessable Entity - Dados inválidos |

---

## 🎓 Conceitos DRY e KISS

### 📝 DRY (Don't Repeat Yourself)

**Princípio:** Evite duplicação de código. Cada lógica deve existir em um único lugar.

#### ❌ Violação (exemplos_violacoes.py)

```python
def criar_pessoa(cpf: str):
    # Validação de CPF - Primeira vez
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numeros) != 11:
        raise HTTPException(...)
    # ... 30 linhas de validação

def atualizar_pessoa(cpf: str):
    # MESMA validação de CPF - Segunda vez (DUPLICADO!)
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numeros) != 11:
        raise HTTPException(...)
    # ... 30 linhas REPETIDAS

def deletar_pessoa(cpf: str):
    # MESMA validação - Terceira vez (MAIS DUPLICAÇÃO!)
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    # ... 30 linhas REPETIDAS NOVAMENTE
```

**Problemas:**
- 🔴 90+ linhas duplicadas
- 🔴 Se houver bug, corrigir em 3 lugares
- 🔴 Difícil manter sincronizado

#### ✅ Boa Prática (server.py)

```python
def validar_cpf(cpf: str) -> bool:
    """Função centralizada - escrita UMA vez"""
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numeros) != 11:
        return False
    # ... validação completa em um só lugar

# Reutilizada em TODOS os lugares
def criar_pessoa(cpf: str):
    if not validar_cpf(cpf):
        raise HTTPException(...)

def atualizar_pessoa(cpf: str):
    if not validar_cpf(cpf):  # Mesma função
        raise HTTPException(...)

def deletar_pessoa(cpf: str):
    if not validar_cpf(cpf):  # Mesma função
        raise HTTPException(...)
```

**Benefícios:**
- ✅ 30 linhas (vs 90+ duplicadas)
- ✅ Correção em um único lugar
- ✅ 67% menos código
- ✅ Fácil manutenção

---

### 🎯 KISS (Keep It Simple, Stupid)

**Princípio:** Prefira soluções simples. Não complique desnecessariamente.

#### ❌ Violação (exemplos_violacoes.py)

```python
class ValidadorCPFComplexo:
    """Classe complexa para tarefa simples"""
    
    def __init__(self, cpf: str):
        self.cpf_original = cpf
        self.cpf_processado = None
        self.digitos = []
        self.pesos_primeira_validacao = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.pesos_segunda_validacao = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        self.resultado_validacao = None
        self.erros = []
        self.warnings = []
    
    def preprocessar_cpf(self):
        """Método complexo desnecessário"""
        self.cpf_processado = ""
        for caractere in self.cpf_original:
            if caractere.isdigit():
                self.cpf_processado += caractere
        return self
    
    def extrair_digitos(self): ...
    def validar_tamanho(self): ...
    def validar_digitos_repetidos(self): ...
    # ... mais 8 métodos complexos
    
    def executar_validacao_completa(self):
        """Orquestrador complexo"""
        try:
            self.preprocessar_cpf()
            self.extrair_digitos()
            if not self.validar_tamanho():
                return self
            # ... mais lógica aninhada
```

**Problemas:**
- 🔴 150+ linhas para tarefa simples
- 🔴 Classe desnecessária
- 🔴 12 métodos quando 1 função basta
- 🔴 Difícil entender e testar

#### ✅ Boa Prática (server.py)

```python
def validar_cpf(cpf: str) -> bool:
    """Função simples e direta - 25 linhas"""
    
    # Remove caracteres não numéricos
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_numeros) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf_numeros == cpf_numeros[0] * 11:
        return False
    
    # Valida primeiro dígito verificador
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf_numeros[9]):
        return False
    
    # Valida segundo dígito verificador
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf_numeros[10]):
        return False
    
    return True
```

**Benefícios:**
- ✅ 25 linhas (vs 150+ complexas)
- ✅ Função pura (sem classe)
- ✅ Fácil entender em uma leitura
- ✅ 83% menos complexidade

---

### 📊 Comparação Lado a Lado

| Aspecto | Violação | Boa Prática | Melhoria |
|---------|----------|-------------|----------|
| **DRY - Linhas de código** | 90+ (duplicadas) | 30 (única) | -67% |
| **DRY - Locais de alteração** | 3 lugares | 1 lugar | -67% |
| **KISS - Linhas de código** | 150+ | 25 | -83% |
| **KISS - Número de métodos** | 12 | 1 | -92% |
| **KISS - Usa classe?** | Sim (desnecessário) | Não | Mais simples |
| **Facilidade de entender** | Difícil | Fácil | ++ |
| **Facilidade de testar** | Difícil | Fácil | ++ |
| **Performance** | Lenta | Rápida | ++ |

---

## 🧪 Testes

### CPFs Válidos para Teste

```
12345678909
111.444.777-35
52998224725
```

### CPFs Inválidos (para testar validação)

```
12345678900  # Dígito verificador errado
11111111111  # Todos dígitos iguais
123456789    # Menos de 11 dígitos
```

### Suite de Testes Executados

✅ **Teste 1:** Criar pessoa com CPF válido  
✅ **Teste 2:** Criar com CPF inválido (deve falhar)  
✅ **Teste 3:** Criar com CPF formatado  
✅ **Teste 4:** Listar todas as pessoas  
✅ **Teste 5:** Buscar por CPF  
✅ **Teste 6:** Atualizar dados  
✅ **Teste 7:** Criar com CPF duplicado (deve falhar)  
✅ **Teste 8:** Criar com dígitos repetidos (deve falhar)  
✅ **Teste 9:** Deletar pessoa  
✅ **Teste 10:** Verificar lista após deleção  

**Taxa de Sucesso: 100% (10/10)**

Ver detalhes em `/app/TESTES_REALIZADOS.md`

---

## 📄 Documentos de Evidência

### 1. `/app/backend/server.py`
- ✅ Implementação da API com BOAS PRÁTICAS
- ✅ Código limpo e documentado
- ✅ Exemplos de DRY e KISS corretos

### 2. `/app/backend/exemplos_violacoes.py`
- ❌ Exemplos de código RUIM (apenas didático)
- ❌ Violações de DRY e KISS
- ❌ Demonstra problemas a evitar

### 3. `/app/EVIDENCIAS.md`
- 📄 Documentação completa
- 📄 Explicações detalhadas de DRY e KISS
- 📄 Comparações lado a lado
- 📄 Exemplos de uso da API

### 4. `/app/TESTES_REALIZADOS.md`
- 📋 Relatório de testes executados
- 📋 Resultados detalhados
- 📋 Validação dos conceitos
- 📋 Evidências de funcionamento

### 5. `/app/README_API.md` (este arquivo)
- 📖 Documentação geral do projeto
- 📖 Guia de uso
- 📖 Referência rápida

---

## 🎯 Resumo

Este projeto demonstra:

1. ✅ API RESTful completa com FastAPI
2. ✅ Validação robusta de CPF brasileiro
3. ✅ CRUD completo (Create, Read, Update, Delete)
4. ✅ MongoDB em container Docker
5. ✅ Código limpo e bem documentado
6. ✅ **Exemplos claros de DRY** (violação + boa prática)
7. ✅ **Exemplos claros de KISS** (violação + boa prática)
8. ✅ Testes funcionais executados
9. ✅ Documentação completa

---

## 📞 Informações Adicionais

**Documentação Interativa:** http://localhost:8001/docs  
**Healthcheck:** http://localhost:8001/api/  
**Logs do Backend:** `/var/log/supervisor/backend.*.log`

**Status dos Serviços:**
```bash
sudo supervisorctl status backend
```

**Reiniciar Backend:**
```bash
sudo supervisorctl restart backend
```

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais, demonstrando conceitos de DRY e KISS em Python/FastAPI.

---

**Desenvolvido com ❤️ usando FastAPI + MongoDB**

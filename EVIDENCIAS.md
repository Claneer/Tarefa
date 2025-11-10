# DOCUMENTO DE EVIDÊNCIAS - API DE CADASTRO DE PESSOAS

## Índice
1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Arquitetura](#arquitetura)
3. [Exemplos DRY (Don't Repeat Yourself)](#exemplos-dry)
4. [Exemplos KISS (Keep It Simple, Stupid)](#exemplos-kiss)
5. [Validação de CPF](#validação-de-cpf)
6. [Endpoints da API](#endpoints-da-api)
7. [Testes e Exemplos de Uso](#testes-e-exemplos-de-uso)

---

## Visão Geral do Projeto

Este projeto implementa uma API RESTful em Python usando FastAPI para cadastro de pessoas com validação de CPF brasileiro. O sistema demonstra boas práticas de desenvolvimento, incluindo os princípios DRY e KISS.

**Tecnologias:**
- **Backend:** FastAPI (Python)
- **Banco de Dados:** MongoDB (em container Docker)
- **Validações:** Pydantic
- **Async:** Motor (driver MongoDB assíncrono)

**Funcionalidades:**
- ✅ Criar pessoa com validação de CPF
- ✅ Listar todas as pessoas
- ✅ Buscar pessoa por CPF
- ✅ Atualizar dados de pessoa
- ✅ Deletar pessoa
- ✅ Validação de email
- ✅ Timestamps automáticos (created_at, updated_at)

---

## Arquitetura

### Estrutura do Banco de Dados

**Collection: `pessoas`**
```json
{
  "cpf": "12345678901",
  "nome": "João Silva",
  "email": "joao@email.com",
  "endereco": "Rua Exemplo, 123 - São Paulo/SP",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### Fluxo de Dados

```
Cliente → FastAPI → Validação (Pydantic) → MongoDB
                ↓
         Validação CPF
         (função centralizada)
```

---

## Exemplos DRY (Don't Repeat Yourself)

### ❌ VIOLAÇÃO DO DRY

**Problema:** Código de validação de CPF duplicado em múltiplos lugares

**Arquivo:** `/app/backend/exemplos_violacoes.py` (linhas 16-86)

**Código Ruim:**
```python
def criar_pessoa_com_duplicacao(cpf: str, nome: str, email: str):
    # Validação de CPF - Primeira vez
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numeros) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    if cpf_numeros == cpf_numeros[0] * 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf_numeros[9]):
        raise HTTPException(status_code=400, detail="CPF inválido")
    soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if digito2 != int(cpf_numeros[10]):
        raise HTTPException(status_code=400, detail="CPF inválido")
    # ...

def atualizar_pessoa_com_duplicacao(cpf: str, nome: str = None):
    # MESMA validação de CPF repetida - Segunda vez
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_numeros) != 11:
        raise HTTPException(status_code=400, detail="CPF inválido")
    # ... (código duplicado)

def deletar_pessoa_com_duplicacao(cpf: str):
    # MESMA validação repetida - Terceira vez
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    # ... (código duplicado novamente)
```

**Problemas:**
1. ❌ Código duplicado em 3 funções (30+ linhas repetidas)
2. ❌ Se houver bug, precisa corrigir em 3 lugares
3. ❌ Se a regra mudar, precisa atualizar 3 lugares
4. ❌ Difícil de manter e testar
5. ❌ Aumenta tamanho do código desnecessariamente

---

### ✅ BOA PRÁTICA DRY

**Solução:** Função centralizada reutilizável

**Arquivo:** `/app/backend/server.py` (linhas 30-68)

**Código Correto:**
```python
def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro.
    Função centralizada, reutilizável em todo o código.
    """
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf_numeros) != 11:
        return False
    
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

# USO: Reutilizada em todos os endpoints
@api_router.post("/pessoas")
async def criar_pessoa(pessoa: PessoaCreate):
    # Usa a função centralizada
    if not validar_cpf(pessoa.cpf):
        raise HTTPException(...)

@api_router.get("/pessoas/{cpf}")
async def buscar_pessoa(cpf: str):
    # Reutiliza a mesma função
    if not validar_cpf(cpf):
        raise HTTPException(...)
```

**Vantagens:**
1. ✅ Função escrita UMA vez, usada em VÁRIOS lugares
2. ✅ Mudanças em um único local
3. ✅ Mais fácil de testar (testar uma função vs testar três)
4. ✅ Código mais limpo e menor
5. ✅ Menos bugs (uma fonte de verdade)

**Evidência de Reutilização:**
- Linha 111: Validação no modelo Pydantic
- Linha 129: Validação no modelo PessoaCreate
- Linha 169: Endpoint criar_pessoa
- Linha 214: Endpoint buscar_pessoa
- Linha 248: Endpoint atualizar_pessoa
- Linha 306: Endpoint deletar_pessoa

**Estatística:**
- Código duplicado: ~90 linhas (3 funções × 30 linhas)
- Código centralizado: ~30 linhas (1 função)
- **Redução: 67% menos código!**

---

## Exemplos KISS (Keep It Simple, Stupid)

### ❌ VIOLAÇÃO DO KISS

**Problema:** Complexidade desnecessária para tarefa simples

**Arquivo:** `/app/backend/exemplos_violacoes.py` (linhas 100-260)

**Código Ruim:**
```python
class ValidadorCPFComplexo:
    """
    Classe excessivamente complexa para validação simples
    """
    
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
        """Método desnecessariamente complexo"""
        self.cpf_processado = ""
        for caractere in self.cpf_original:
            if caractere.isdigit():
                self.cpf_processado += caractere
        return self
    
    def extrair_digitos(self):
        """Método complexo para tarefa simples"""
        self.digitos = []
        for i in range(len(self.cpf_processado)):
            try:
                digito = int(self.cpf_processado[i])
                self.digitos.append(digito)
            except (ValueError, IndexError) as e:
                self.erros.append(f"Erro: {str(e)}")
        return self
    
    def validar_tamanho(self):
        """Método verboso"""
        if len(self.digitos) < 11:
            self.erros.append("CPF tem menos de 11 dígitos")
            return False
        elif len(self.digitos) > 11:
            self.erros.append("CPF tem mais de 11 dígitos")
            return False
        else:
            return True
    
    # ... mais 8 métodos complexos ...
    
    def executar_validacao_completa(self):
        """Orquestrador complexo"""
        try:
            self.preprocessar_cpf()
            self.extrair_digitos()
            if not self.validar_tamanho():
                return self
            # ... mais validações aninhadas ...
        except Exception as e:
            self.erros.append(f"Erro: {str(e)}")
        return self

# Uso igualmente complexo
def validar_cpf_forma_complexa(cpf: str) -> bool:
    validador = ValidadorCPFComplexo(cpf)
    validador.executar_validacao_completa()
    resultado = validador.obter_resultado()
    # ... mais processamento ...
```

**Problemas:**
1. ❌ Mais de 150 linhas para tarefa que precisa de 20
2. ❌ Classe desnecessária (over-engineering)
3. ❌ 12 métodos quando 1 função bastaria
4. ❌ Difícil de entender e manter
5. ❌ Variáveis desnecessárias (erros, warnings, etc.)
6. ❌ Dificulta testes unitários
7. ❌ Lento (múltiplas chamadas de método)

---

### ✅ BOA PRÁTICA KISS

**Solução:** Função simples e direta

**Arquivo:** `/app/backend/server.py` (linhas 30-68 e 77-84)

**Código Correto:**
```python
def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro.
    Função simples, direta e fácil de entender.
    """
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


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF removendo caracteres especiais.
    Função simples com uma única responsabilidade.
    """
    return re.sub(r'[^0-9]', '', cpf)
```

**Vantagens:**
1. ✅ Apenas 25 linhas (vs 150+ da versão complexa)
2. ✅ Função pura (não precisa de classe)
3. ✅ Fácil de entender em uma leitura
4. ✅ Fácil de testar
5. ✅ Rápido (sem overhead de classe)
6. ✅ Uma função, uma responsabilidade
7. ✅ Comentários claros explicando cada passo

**Comparação:**

| Aspecto | Versão Complexa (RUIM) | Versão Simples (BOA) |
|---------|------------------------|----------------------|
| Linhas de código | ~150 | ~25 |
| Número de funções/métodos | 12 | 1 |
| Usa classe? | Sim (desnecessário) | Não |
| Facilidade de entender | Difícil | Fácil |
| Facilidade de testar | Difícil | Fácil |
| Performance | Mais lenta | Mais rápida |
| Manutenção | Difícil | Fácil |

---

## Validação de CPF

### Algoritmo Implementado

O CPF brasileiro possui 11 dígitos: `XXX.XXX.XXX-YZ`
- Os 9 primeiros (XXX.XXX.XXX) são o número base
- Os 2 últimos (YZ) são dígitos verificadores

**Passos da Validação:**

1. **Limpeza:** Remove pontos e traços
   ```
   123.456.789-09 → 12345678909
   ```

2. **Verificação de tamanho:** Deve ter exatamente 11 dígitos

3. **Verificação de dígitos repetidos:** Rejeita CPFs como 111.111.111-11

4. **Cálculo do primeiro dígito verificador (Y):**
   ```
   Multiplicadores: 10, 9, 8, 7, 6, 5, 4, 3, 2
   CPF: 1 2 3 4 5 6 7 8 9
   
   Soma = (1×10) + (2×9) + (3×8) + (4×7) + (5×6) + (6×5) + (7×4) + (8×3) + (9×2)
   Resto = (Soma × 10) % 11
   Dígito = Resto % 10
   ```

5. **Cálculo do segundo dígito verificador (Z):**
   ```
   Multiplicadores: 11, 10, 9, 8, 7, 6, 5, 4, 3, 2
   CPF: 1 2 3 4 5 6 7 8 9 Y
   
   (mesmo processo)
   ```

### Exemplos de CPFs

**CPFs Válidos para Teste:**
- 123.456.789-09
- 111.444.777-35
- 12345678909 (sem formatação)

**CPFs Inválidos:**
- 123.456.789-00 (dígito verificador errado)
- 111.111.111-11 (todos dígitos iguais)
- 123.456.789 (faltam dígitos)
- abc.def.ghi-jk (não numérico)

---

## Endpoints da API

### Base URL
```
http://localhost:8001/api
```

### 1. Criar Pessoa

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
  "created_at": "2025-01-15T10:30:00.000Z",
  "updated_at": "2025-01-15T10:30:00.000Z"
}
```

**Erros:**
- `400 Bad Request`: CPF inválido ou já cadastrado
- `422 Unprocessable Entity`: Dados inválidos (email, tamanho de campos)

---

### 2. Listar Todas as Pessoas

**Endpoint:** `GET /api/pessoas`

**Response (200 OK):**
```json
[
  {
    "cpf": "12345678909",
    "nome": "João Silva",
    "email": "joao@email.com",
    "endereco": "Rua Exemplo, 123 - São Paulo/SP",
    "created_at": "2025-01-15T10:30:00.000Z",
    "updated_at": "2025-01-15T10:30:00.000Z"
  },
  {
    "cpf": "98765432100",
    "nome": "Maria Santos",
    "email": "maria@email.com",
    "endereco": "Av. Principal, 456 - Rio de Janeiro/RJ",
    "created_at": "2025-01-15T11:00:00.000Z",
    "updated_at": "2025-01-15T11:00:00.000Z"
  }
]
```

---

### 3. Buscar Pessoa por CPF

**Endpoint:** `GET /api/pessoas/{cpf}`

**Exemplo:** `GET /api/pessoas/12345678909`

**Response (200 OK):**
```json
{
  "cpf": "12345678909",
  "nome": "João Silva",
  "email": "joao@email.com",
  "endereco": "Rua Exemplo, 123 - São Paulo/SP",
  "created_at": "2025-01-15T10:30:00.000Z",
  "updated_at": "2025-01-15T10:30:00.000Z"
}
```

**Erros:**
- `400 Bad Request`: CPF inválido
- `404 Not Found`: Pessoa não encontrada

---

### 4. Atualizar Pessoa

**Endpoint:** `PUT /api/pessoas/{cpf}`

**Request Body (todos campos opcionais):**
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
  "created_at": "2025-01-15T10:30:00.000Z",
  "updated_at": "2025-01-15T14:20:00.000Z"
}
```

**Observações:**
- CPF não pode ser alterado
- Pode atualizar um ou mais campos
- `updated_at` é atualizado automaticamente

**Erros:**
- `400 Bad Request`: CPF inválido ou nenhum campo fornecido
- `404 Not Found`: Pessoa não encontrada

---

### 5. Deletar Pessoa

**Endpoint:** `DELETE /api/pessoas/{cpf}`

**Exemplo:** `DELETE /api/pessoas/12345678909`

**Response (200 OK):**
```json
{
  "message": "Pessoa com CPF 123.456.789-09 deletada com sucesso",
  "deleted_count": 1
}
```

**Erros:**
- `400 Bad Request`: CPF inválido
- `404 Not Found`: Pessoa não encontrada

---

## Testes e Exemplos de Uso

### Teste 1: Criar Pessoa com CPF Válido

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

**Resultado Esperado:** ✅ Status 201 Created

---

### Teste 2: Criar Pessoa com CPF Inválido (Violação)

```bash
curl -X POST http://localhost:8001/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678900",
    "nome": "Maria Santos",
    "email": "maria@email.com",
    "endereco": "Av. Principal, 456"
  }'
```

**Resultado Esperado:** ❌ Status 422 - CPF inválido

---

### Teste 3: Criar Pessoa com CPF Repetido

```bash
curl -X POST http://localhost:8001/api/pessoas \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "11111111111",
    "nome": "Pedro Oliveira",
    "email": "pedro@email.com",
    "endereco": "Rua Teste, 789"
  }'
```

**Resultado Esperado:** ❌ Status 422 - CPF inválido (todos dígitos iguais)

---

### Teste 4: Buscar Pessoa por CPF com Formatação

```bash
curl -X GET http://localhost:8001/api/pessoas/123.456.789-09
```

**Resultado Esperado:** ✅ Retorna dados da pessoa (aceita formatação)

---

### Teste 5: Atualizar Email de Pessoa

```bash
curl -X PUT http://localhost:8001/api/pessoas/12345678909 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao.novo@email.com"
  }'
```

**Resultado Esperado:** ✅ Status 200 com dados atualizados

---

### Teste 6: Listar Todas as Pessoas

```bash
curl -X GET http://localhost:8001/api/pessoas
```

**Resultado Esperado:** ✅ Array com todas as pessoas cadastradas

---

### Teste 7: Deletar Pessoa

```bash
curl -X DELETE http://localhost:8001/api/pessoas/12345678909
```

**Resultado Esperado:** ✅ Status 200 com mensagem de sucesso

---

### Teste 8: Buscar Pessoa Inexistente

```bash
curl -X GET http://localhost:8001/api/pessoas/99999999999
```

**Resultado Esperado:** ❌ Status 404 - Pessoa não encontrada

---

## Resumo dos Conceitos

### DRY (Don't Repeat Yourself)

**Violação (arquivo exemplos_violacoes.py):**
- ❌ Validação de CPF duplicada em 3 funções
- ❌ 90+ linhas de código repetido
- ❌ Manutenção difícil

**Boa Prática (arquivo server.py):**
- ✅ Função `validar_cpf()` centralizada
- ✅ Reutilizada em 6 lugares diferentes
- ✅ Redução de 67% no código
- ✅ Fácil manutenção

---

### KISS (Keep It Simple, Stupid)

**Violação (arquivo exemplos_violacoes.py):**
- ❌ Classe com 150+ linhas para tarefa simples
- ❌ 12 métodos desnecessários
- ❌ Over-engineering
- ❌ Difícil de entender

**Boa Prática (arquivo server.py):**
- ✅ Função simples com 25 linhas
- ✅ Clara e direta
- ✅ Fácil de entender e manter
- ✅ Solução apropriada ao problema

---

## Conclusão

Este projeto demonstra:

1. ✅ **API RESTful completa** com FastAPI
2. ✅ **Validação robusta de CPF** brasileiro
3. ✅ **CRUD completo** (Create, Read, Update, Delete)
4. ✅ **MongoDB em Docker** para persistência
5. ✅ **Exemplos claros de violação e boa prática** de DRY
6. ✅ **Exemplos claros de violação e boa prática** de KISS
7. ✅ **Código documentado** com comentários explicativos
8. ✅ **Validações automáticas** com Pydantic
9. ✅ **Timestamps automáticos** para auditoria
10. ✅ **Tratamento de erros** apropriado

**Arquivos principais:**
- `/app/backend/server.py` - Implementação da API (BOA PRÁTICA)
- `/app/backend/exemplos_violacoes.py` - Exemplos de código ruim (VIOLAÇÕES)
- `/app/EVIDENCIAS.md` - Este documento com toda documentação

**Para executar:**
```bash
# Backend já está rodando em http://localhost:8001
# MongoDB já está rodando em container Docker

# Acessar documentação interativa:
http://localhost:8001/docs
```

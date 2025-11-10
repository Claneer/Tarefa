from fastapi import FastAPI, APIRouter, HTTPException, status
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import re


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="API de Cadastro de Pessoas", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ========================================
# EXEMPLO DE BOA PRÁTICA: DRY (Don't Repeat Yourself)
# ========================================
# Função centralizada para validação de CPF - reutilizável em todo o código
# Evita duplicação de lógica de validação
def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF brasileiro.
    
    Args:
        cpf: String contendo o CPF (pode conter pontos e traços)
    
    Returns:
        bool: True se o CPF é válido, False caso contrário
    
    Exemplo de BOA PRÁTICA DRY:
    - Função centralizada, reutilizável
    - Evita código duplicado
    - Facilita manutenção (mudança em um só lugar)
    """
    # Remove caracteres não numéricos
    cpf_numeros = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf_numeros) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
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


# ========================================
# EXEMPLO DE BOA PRÁTICA: KISS (Keep It Simple, Stupid)
# ========================================
def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF removendo caracteres especiais.
    
    Exemplo de BOA PRÁTICA KISS:
    - Função simples e direta
    - Faz apenas uma coisa
    - Fácil de entender e testar
    """
    return re.sub(r'[^0-9]', '', cpf)


# Define Models
class Pessoa(BaseModel):
    """
    Modelo de dados para uma Pessoa.
    
    Exemplo de BOA PRÁTICA DRY:
    - Validação declarativa usando Pydantic
    - Evita código repetitivo de validação
    """
    model_config = ConfigDict(extra="ignore")
    
    cpf: str = Field(..., description="CPF da pessoa (apenas números ou com formatação)")
    nome: str = Field(..., min_length=3, max_length=200, description="Nome completo da pessoa")
    email: EmailStr = Field(..., description="Email da pessoa")
    endereco: str = Field(..., min_length=5, max_length=500, description="Endereço completo")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf_field(cls, v: str) -> str:
        """Valida o CPF usando a função centralizada (DRY)"""
        if not validar_cpf(v):
            raise ValueError('CPF inválido')
        # Retorna apenas números para armazenamento consistente
        return formatar_cpf(v)


class PessoaCreate(BaseModel):
    """Modelo para criação de pessoa (sem timestamps)"""
    cpf: str = Field(..., description="CPF da pessoa")
    nome: str = Field(..., min_length=3, max_length=200)
    email: EmailStr
    endereco: str = Field(..., min_length=5, max_length=500)
    
    @field_validator('cpf')
    @classmethod
    def validar_cpf_field(cls, v: str) -> str:
        if not validar_cpf(v):
            raise ValueError('CPF inválido')
        return formatar_cpf(v)


class PessoaUpdate(BaseModel):
    """Modelo para atualização de pessoa (todos os campos opcionais exceto ao menos um)"""
    nome: Optional[str] = Field(None, min_length=3, max_length=200)
    email: Optional[EmailStr] = None
    endereco: Optional[str] = Field(None, min_length=5, max_length=500)


class PessoaResponse(BaseModel):
    """Modelo de resposta com CPF formatado para visualização"""
    cpf: str
    nome: str
    email: str
    endereco: str
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def formatar_cpf_display(cpf: str) -> str:
        """Formata CPF para exibição: 123.456.789-01"""
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


# ========================================
# ROTAS DA API - CRUD COMPLETO
# ========================================

@api_router.post(
    "/pessoas",
    response_model=Pessoa,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova pessoa",
    description="Cria uma nova pessoa com validação de CPF"
)
async def criar_pessoa(pessoa: PessoaCreate):
    """
    Cria uma nova pessoa no banco de dados.
    
    Validações:
    - CPF único no sistema
    - CPF válido (dígitos verificadores)
    - Email válido
    - Todos os campos obrigatórios preenchidos
    
    Exemplo de BOA PRÁTICA KISS:
    - Endpoint simples e direto
    - Uma responsabilidade: criar pessoa
    - Validações claras e organizadas
    """
    # Verifica se CPF já existe
    cpf_existente = await db.pessoas.find_one({"cpf": pessoa.cpf})
    if cpf_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CPF {PessoaResponse.formatar_cpf_display(pessoa.cpf)} já cadastrado no sistema"
        )
    
    # Cria objeto Pessoa com timestamps
    pessoa_obj = Pessoa(**pessoa.model_dump())
    
    # Prepara documento para MongoDB
    doc = pessoa_obj.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()
    doc['updated_at'] = doc['updated_at'].isoformat()
    
    # Insere no banco
    await db.pessoas.insert_one(doc)
    
    return pessoa_obj


@api_router.get(
    "/pessoas",
    response_model=List[Pessoa],
    summary="Listar todas as pessoas",
    description="Retorna lista de todas as pessoas cadastradas"
)
async def listar_pessoas():
    """
    Lista todas as pessoas cadastradas.
    
    Exemplo de BOA PRÁTICA KISS:
    - Endpoint simples
    - Retorna dados diretos sem transformações complexas
    """
    pessoas = await db.pessoas.find({}, {"_id": 0}).to_list(1000)
    
    # Converte timestamps ISO de volta para datetime
    for pessoa in pessoas:
        if isinstance(pessoa.get('created_at'), str):
            pessoa['created_at'] = datetime.fromisoformat(pessoa['created_at'])
        if isinstance(pessoa.get('updated_at'), str):
            pessoa['updated_at'] = datetime.fromisoformat(pessoa['updated_at'])
    
    return pessoas


@api_router.get(
    "/pessoas/{cpf}",
    response_model=Pessoa,
    summary="Buscar pessoa por CPF",
    description="Retorna os dados de uma pessoa específica pelo CPF"
)
async def buscar_pessoa(cpf: str):
    """
    Busca uma pessoa pelo CPF.
    
    Args:
        cpf: CPF da pessoa (com ou sem formatação)
    
    Exemplo de BOA PRÁTICA DRY:
    - Reutiliza função de formatação de CPF
    - Evita duplicação de lógica
    """
    # Valida e formata CPF
    if not validar_cpf(cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido"
        )
    
    cpf_formatado = formatar_cpf(cpf)
    
    # Busca no banco
    pessoa = await db.pessoas.find_one({"cpf": cpf_formatado}, {"_id": 0})
    
    if not pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com CPF {PessoaResponse.formatar_cpf_display(cpf_formatado)} não encontrada"
        )
    
    # Converte timestamps
    if isinstance(pessoa.get('created_at'), str):
        pessoa['created_at'] = datetime.fromisoformat(pessoa['created_at'])
    if isinstance(pessoa.get('updated_at'), str):
        pessoa['updated_at'] = datetime.fromisoformat(pessoa['updated_at'])
    
    return pessoa


@api_router.put(
    "/pessoas/{cpf}",
    response_model=Pessoa,
    summary="Atualizar pessoa",
    description="Atualiza os dados de uma pessoa existente"
)
async def atualizar_pessoa(cpf: str, pessoa_update: PessoaUpdate):
    """
    Atualiza os dados de uma pessoa.
    
    Args:
        cpf: CPF da pessoa (não pode ser alterado)
        pessoa_update: Dados a serem atualizados
    
    Exemplo de BOA PRÁTICA KISS:
    - Atualiza apenas campos fornecidos
    - Lógica simples e clara
    """
    # Valida CPF
    if not validar_cpf(cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido"
        )
    
    cpf_formatado = formatar_cpf(cpf)
    
    # Verifica se pessoa existe
    pessoa_existente = await db.pessoas.find_one({"cpf": cpf_formatado}, {"_id": 0})
    if not pessoa_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com CPF {PessoaResponse.formatar_cpf_display(cpf_formatado)} não encontrada"
        )
    
    # Prepara dados para atualização (apenas campos não nulos)
    update_data = pessoa_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar foi fornecido"
        )
    
    # Adiciona timestamp de atualização
    update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    # Atualiza no banco
    await db.pessoas.update_one(
        {"cpf": cpf_formatado},
        {"$set": update_data}
    )
    
    # Busca e retorna pessoa atualizada
    pessoa_atualizada = await db.pessoas.find_one({"cpf": cpf_formatado}, {"_id": 0})
    
    # Converte timestamps
    if isinstance(pessoa_atualizada.get('created_at'), str):
        pessoa_atualizada['created_at'] = datetime.fromisoformat(pessoa_atualizada['created_at'])
    if isinstance(pessoa_atualizada.get('updated_at'), str):
        pessoa_atualizada['updated_at'] = datetime.fromisoformat(pessoa_atualizada['updated_at'])
    
    return pessoa_atualizada


@api_router.delete(
    "/pessoas/{cpf}",
    status_code=status.HTTP_200_OK,
    summary="Deletar pessoa",
    description="Remove uma pessoa do sistema"
)
async def deletar_pessoa(cpf: str):
    """
    Deleta uma pessoa do sistema.
    
    Args:
        cpf: CPF da pessoa a ser deletada
    
    Exemplo de BOA PRÁTICA KISS:
    - Função simples com uma única responsabilidade
    - Feedback claro sobre a operação
    """
    # Valida CPF
    if not validar_cpf(cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF inválido"
        )
    
    cpf_formatado = formatar_cpf(cpf)
    
    # Verifica se pessoa existe
    pessoa = await db.pessoas.find_one({"cpf": cpf_formatado})
    if not pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pessoa com CPF {PessoaResponse.formatar_cpf_display(cpf_formatado)} não encontrada"
        )
    
    # Deleta
    resultado = await db.pessoas.delete_one({"cpf": cpf_formatado})
    
    return {
        "message": f"Pessoa com CPF {PessoaResponse.formatar_cpf_display(cpf_formatado)} deletada com sucesso",
        "deleted_count": resultado.deleted_count
    }


# Rota de healthcheck
@api_router.get("/")
async def root():
    return {
        "message": "API de Cadastro de Pessoas",
        "version": "1.0.0",
        "endpoints": {
            "criar": "POST /api/pessoas",
            "listar": "GET /api/pessoas",
            "buscar": "GET /api/pessoas/{cpf}",
            "atualizar": "PUT /api/pessoas/{cpf}",
            "deletar": "DELETE /api/pessoas/{cpf}"
        }
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

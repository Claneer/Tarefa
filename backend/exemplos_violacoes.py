"""
EXEMPLOS DE VIOLAÇÕES DE DRY E KISS

Este arquivo contém exemplos de código que VIOLAM os princípios DRY e KISS.
ESTES EXEMPLOS NÃO SÃO USADOS NA API PRINCIPAL - são apenas para fins didáticos.
"""

import re
from fastapi import HTTPException, status


# ========================================
# EXEMPLO DE VIOLAÇÃO: DRY (Don't Repeat Yourself)
# ========================================

# ❌ CÓDIGO RUIM - VIOLAÇÃO DO DRY
# Problema: Lógica de validação de CPF duplicada em múltiplos lugares

def criar_pessoa_com_duplicacao(cpf: str, nome: str, email: str):
    """
    Exemplo de VIOLAÇÃO do DRY: código de validação duplicado
    """
    # Validação de CPF duplicada - Primeira vez
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
    
    # Cria pessoa...
    return {"cpf": cpf_numeros, "nome": nome, "email": email}


def atualizar_pessoa_com_duplicacao(cpf: str, nome: str = None, email: str = None):
    """
    Exemplo de VIOLAÇÃO do DRY: mesma validação de CPF repetida
    """
    # Validação de CPF duplicada - Segunda vez (CÓDIGO REPETIDO!)
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
    
    # Atualiza pessoa...
    return {"cpf": cpf_numeros, "nome": nome, "email": email}


def deletar_pessoa_com_duplicacao(cpf: str):
    """
    Exemplo de VIOLAÇÃO do DRY: validação repetida mais uma vez
    """
    # Validação de CPF duplicada - Terceira vez (MAIS CÓDIGO REPETIDO!)
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
    
    # Deleta pessoa...
    return {"message": "Pessoa deletada"}


# PROBLEMAS da violação do DRY acima:
# 1. Código duplicado em 3 funções diferentes (30+ linhas repetidas)
# 2. Se houver um bug na validação, precisa corrigir em 3 lugares
# 3. Se a regra de validação mudar, precisa atualizar 3 lugares
# 4. Difícil de manter e testar
# 5. Aumenta desnecessariamente o tamanho do código


# ✅ SOLUÇÃO CORRETA (implementada no server.py):
# Uma única função validar_cpf() que é reutilizada em todos os lugares


# ========================================
# EXEMPLO DE VIOLAÇÃO: KISS (Keep It Simple, Stupid)
# ========================================

# ❌ CÓDIGO RUIM - VIOLAÇÃO DO KISS
# Problema: Complexidade desnecessária, código difícil de entender

class ValidadorCPFComplexo:
    """
    Exemplo de VIOLAÇÃO do KISS: classe excessivamente complexa
    para uma tarefa simples
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
        """Método desnecessariamente complexo para limpar CPF"""
        self.cpf_processado = ""
        for caractere in self.cpf_original:
            if caractere.isdigit():
                self.cpf_processado += caractere
        return self
    
    def extrair_digitos(self):
        """Método complexo para extrair dígitos"""
        self.digitos = []
        for i in range(len(self.cpf_processado)):
            try:
                digito = int(self.cpf_processado[i])
                self.digitos.append(digito)
            except (ValueError, IndexError) as e:
                self.erros.append(f"Erro ao processar posição {i}: {str(e)}")
        return self
    
    def validar_tamanho(self):
        """Método verboso para validação simples"""
        if len(self.digitos) < 11:
            self.erros.append("CPF tem menos de 11 dígitos")
            return False
        elif len(self.digitos) > 11:
            self.erros.append("CPF tem mais de 11 dígitos")
            return False
        else:
            return True
    
    def validar_digitos_repetidos(self):
        """Método complexo para verificação simples"""
        primeiro_digito = self.digitos[0]
        contador_iguais = 0
        for digito in self.digitos:
            if digito == primeiro_digito:
                contador_iguais += 1
        if contador_iguais == len(self.digitos):
            self.erros.append("Todos os dígitos são iguais")
            return False
        return True
    
    def calcular_primeiro_digito_verificador(self):
        """Método excessivamente verboso"""
        soma_total = 0
        for indice in range(9):
            peso = self.pesos_primeira_validacao[indice]
            digito = self.digitos[indice]
            produto = peso * digito
            soma_total += produto
        
        resultado_multiplicacao = soma_total * 10
        resto_divisao = resultado_multiplicacao % 11
        digito_verificador = resto_divisao % 10
        
        return digito_verificador
    
    def calcular_segundo_digito_verificador(self):
        """Método excessivamente verboso"""
        soma_total = 0
        for indice in range(10):
            peso = self.pesos_segunda_validacao[indice]
            digito = self.digitos[indice]
            produto = peso * digito
            soma_total += produto
        
        resultado_multiplicacao = soma_total * 10
        resto_divisao = resultado_multiplicacao % 11
        digito_verificador = resto_divisao % 10
        
        return digito_verificador
    
    def executar_validacao_completa(self):
        """Orquestrador complexo de validações"""
        try:
            self.preprocessar_cpf()
            
            if len(self.cpf_processado) == 0:
                self.erros.append("CPF vazio após processamento")
                self.resultado_validacao = False
                return self
            
            self.extrair_digitos()
            
            if not self.validar_tamanho():
                self.resultado_validacao = False
                return self
            
            if not self.validar_digitos_repetidos():
                self.resultado_validacao = False
                return self
            
            primeiro_dv = self.calcular_primeiro_digito_verificador()
            if primeiro_dv != self.digitos[9]:
                self.erros.append("Primeiro dígito verificador inválido")
                self.resultado_validacao = False
                return self
            
            segundo_dv = self.calcular_segundo_digito_verificador()
            if segundo_dv != self.digitos[10]:
                self.erros.append("Segundo dígito verificador inválido")
                self.resultado_validacao = False
                return self
            
            self.resultado_validacao = True
            return self
            
        except Exception as e:
            self.erros.append(f"Erro geral: {str(e)}")
            self.resultado_validacao = False
            return self
    
    def obter_resultado(self):
        """Retorna resultado da validação"""
        return {
            "valido": self.resultado_validacao,
            "cpf_original": self.cpf_original,
            "cpf_processado": self.cpf_processado,
            "erros": self.erros,
            "warnings": self.warnings
        }


def validar_cpf_forma_complexa(cpf: str) -> bool:
    """
    Exemplo de VIOLAÇÃO do KISS: uso excessivamente complexo
    """
    validador = ValidadorCPFComplexo(cpf)
    validador.executar_validacao_completa()
    resultado = validador.obter_resultado()
    
    if not resultado["valido"]:
        mensagem_erro = "CPF inválido: "
        for erro in resultado["erros"]:
            mensagem_erro += erro + "; "
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensagem_erro
        )
    
    return resultado["valido"]


# PROBLEMAS da violação do KISS acima:
# 1. Mais de 150 linhas para fazer algo que pode ser feito em 20 linhas
# 2. Classe desnecessária para uma função simples
# 3. Múltiplos métodos quando uma única função seria suficiente
# 4. Difícil de entender e manter
# 5. Over-engineering: solução muito complexa para um problema simples
# 6. Variáveis desnecessárias (self.erros, self.warnings, etc.)
# 7. Dificulta testes unitários


# ✅ SOLUÇÃO CORRETA (implementada no server.py):
# Uma função simples validar_cpf() com ~20 linhas, clara e direta


# ========================================
# RESUMO DAS DIFERENÇAS
# ========================================

"""
VIOLAÇÃO DRY:
- Código duplicado em múltiplos lugares
- Dificulta manutenção (mudanças em vários lugares)
- Aumenta chance de bugs (esquecer de atualizar em algum lugar)
- Código maior e mais difícil de ler

BOA PRÁTICA DRY:
- Função centralizada reutilizável
- Mudanças em um único lugar
- Mais fácil de testar
- Código mais limpo e menor

---

VIOLAÇÃO KISS:
- Complexidade desnecessária
- Mais de 150 linhas para tarefa simples
- Classe quando função bastaria
- Difícil de entender e manter
- Over-engineering

BOA PRÁTICA KISS:
- Função simples e direta (~20 linhas)
- Fácil de entender
- Fácil de testar
- Solução apropriada ao problema
"""

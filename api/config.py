"""
Configuração central do LLM — Google Gemma via Google AI Studio.

Suporta:
  - Chat/completion: gemma-3-27b-it, gemini-2.0-flash, gemini-1.5-pro
  - Embeddings: models/embedding-001

Usage:
    from api.config import get_llm, get_embeddings

    llm = get_llm()
    response = llm.invoke("Analise este desvio de qualidade...")
"""
from __future__ import annotations

import os
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


GOOGLE_API_KEY      = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL        = os.getenv("GOOGLE_MODEL", "gemma-3-27b-it")
EMBEDDING_MODEL     = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")


@lru_cache(maxsize=1)
def get_llm(
    model: str = GOOGLE_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 4096,
) -> ChatGoogleGenerativeAI:
    """
    Retorna instância cacheada do LLM Google Gemma/Gemini.
    temperature=0.2 para respostas analíticas mais determinísticas.
    """
    if not GOOGLE_API_KEY:
        raise EnvironmentError(
            "GOOGLE_API_KEY não definida. "
            "Adicione ao arquivo .env baseado em .env.example"
        )
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
        max_output_tokens=max_tokens,
        convert_system_message_to_human=True,  # Gemma não suporta SystemMessage nativa
    )


@lru_cache(maxsize=1)
def get_embeddings(model: str = EMBEDDING_MODEL) -> GoogleGenerativeAIEmbeddings:
    """Retorna instância cacheada do modelo de embeddings Google."""
    if not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY não definida.")
    return GoogleGenerativeAIEmbeddings(
        model=model,
        google_api_key=GOOGLE_API_KEY,
    )

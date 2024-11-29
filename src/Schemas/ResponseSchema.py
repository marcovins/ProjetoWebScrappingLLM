from typing import Optional
from pydantic import BaseModel, Field

# Modelo de validação para a saída do scraper
class ResponseSchema(BaseModel):
    descricao: str = Field(..., description="O texto gerado pela LLM")
    tag: str = Field(..., description="Categoria do site")
    tokens_usados: int = Field(..., ge=0, description="Número de tokens utilizados na geração")
    tempo_processamento: Optional[float] = Field(
        None, ge=0.0, description="Tempo em segundos que levou para gerar a resposta"
    )
    confianca: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Pontuação de confiança do modelo, entre 0 e 1"
    )
    metadados: Optional[dict] = Field(
        None, description="Metadados adicionais retornados pelo modelo"
    )
from typing import Optional
from pydantic import BaseModel, Field

# Modelo de validação para a saída do scraper
class ResponseSchema(BaseModel):
    descricao: str = Field(..., description="O texto gerado pela LLM")
    tag: str = Field(..., description="Categoria do site (Saúde, Educação, Trabalho, Agropecuária ou Minério)")
    metadados: Optional[dict] = Field(
        None, description="Metadados adicionais retornados pelo modelo"
    )
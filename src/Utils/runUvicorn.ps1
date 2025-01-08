# RunUvicorn.ps1

# Definir o diretório de trabalho para o diretório onde o script está localizado
Set-Location $PSScriptRoot

# Executar o script RemovePycache.ps1 para limpar os diretórios __pycache__
.\RemovePycache.ps1

# Executar o Uvicorn dentro do ambiente virtual gerenciado pelo Poetry
poetry run uvicorn src.Utils.app:app

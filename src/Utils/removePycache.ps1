# RemovePycache.ps1


# Confirmar antes de remover os diretórios (opcional)
$confirmation = Read-Host "Deseja remover todos os diretorios '__pycache__'? (Sim/Nao) [Padrao: Sim]"

# Definir uma resposta padrão se o usuário pressionar Enter sem digitar nada
if ([string]::IsNullOrWhiteSpace($confirmation)) {
    $confirmation = "Sim"
}

if ($confirmation -eq "Sim") {
    # Remover os diretórios "__pycache__"
    Get-ChildItem -Recurse -Directory -Force -Filter "__pycache__" | Remove-Item -Recurse -Force
    Write-Host "Todos os diretorios '__pycache__' foram removidos."
} else {
    Write-Host "Operacao cancelada."
}
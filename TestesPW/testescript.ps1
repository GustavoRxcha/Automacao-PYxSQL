# Caminho da pasta Temp
$tempPath = $env:temp

# Verifica se a pasta existe e apaga o conteúdo
if (Test-Path $tempPath) {
    Remove-Item -Path "$tempPath\*" -Recurse -Force
}

# Cria a pasta Temp novamente
New-Item -Path $tempPath -ItemType Directory
Write-Output "Pasta %Temp% excluída e recriada com sucesso."

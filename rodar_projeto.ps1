$streamlitExe = "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts\streamlit.exe"

if (-not (Test-Path $streamlitExe)) {
	Write-Host "Streamlit não encontrado em: $streamlitExe" -ForegroundColor Red
	exit 1
}

function Test-PortAvailable {
	param([int]$Port)
	$inUse = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
	return (-not $inUse)
}

$port = 8501
if (-not (Test-PortAvailable -Port $port)) {
	$port = 8502
}

Write-Host "Iniciando Streamlit na porta $port..." -ForegroundColor Yellow
& $streamlitExe run app.py --server.port $port
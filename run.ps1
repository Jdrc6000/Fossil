$ErrorActionPreference = "Stop"

$REPO = "https://github.com/Jdrc6000/Fossil.git"
$MODEL = "gpt-oss:20b-cloud"
$DEST = "$env:TEMP\fossil-$PID"

# install ollama if not present
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Ollama..."
    $installer = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer
    Start-Process $installer -ArgumentList "/silent" -Wait
    # refresh PATH so ollama is findable immediately
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
}

# start ollama service if not running
if (-not (Get-Process "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "Starting Ollama service..."
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# pull model if not already downloaded
$models = ollama list 2>$null
if ($models -notmatch [regex]::Escape($MODEL)) {
    Write-Host "Pulling $MODEL (this might take a while)..."
    ollama pull $MODEL
}

# clone repo
Write-Host "Cloning repo..."
git clone --depth=1 $REPO $DEST
Set-Location $DEST

# install python lib
Write-Host "Installing dependencies..."
pip install ollama --quiet

Write-Host "Starting Fossil..."
python main.py

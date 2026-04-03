$ErrorActionPreference = "Stop"

$REPO = "https://github.com/Jdrc6000/Fossil.git"
$MODEL = "gpt-oss:20b-cloud"
$DEST = "$env:TEMP\fossil-$PID"

# install ollama if not present
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "installing Ollama..."
    $installer = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer
    Start-Process $installer -ArgumentList "/silent" -Wait
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
}

# start ollama service if not running
if (-not (Get-Process "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "starting ollama service..."
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# pull model if not already downloaded
$models = ollama list 2>$null
if ($models -notmatch [regex]::Escape($MODEL)) {
    Write-Host "pulling $MODEL (this might take a while)..."
    ollama pull $MODEL
}

# clone repo
Write-Host "cloning repo..."
git clone --depth=1 $REPO $DEST
Set-Location $DEST

# install python lib
Write-Host "installing dependencies..."
pip install ollama --quiet

Write-Host "starting fossil..."
python main_tui.py
$ErrorActionPreference = "Stop"

$REPO  = "https://github.com/Jdrc6000/Fossil.git"
$MODEL = "gpt-oss:20b-cloud"
$DEST  = "$env:TEMP\fossil-$PID"

# cleanup on exit
$null = Register-EngineEvent PowerShell.Exiting -Action { Remove-Item -Recurse -Force $DEST -ErrorAction SilentlyContinue }

# check git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not installed. Install it from https://git-scm.com"
    exit 1
}

# check python
$pyver = python --version 2>&1
if ($pyver -notmatch "3\.(1[0-9])") {
    Write-Error "Python 3.10+ required. Got: $pyver"
    exit 1
}

# install ollama
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "installing Ollama..."
    $installer = "$env:TEMP\OllamaSetup.exe"
    Invoke-WebRequest "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer
    Start-Process $installer -ArgumentList "/silent" -Wait
    # reload PATH properly
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
}

# start ollama and poll until ready
if (-not (Get-Process "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "starting ollama service..."
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Write-Host "waiting for ollama..."
    $ready = $false
    for ($i = 0; $i -lt 15; $i++) {
        try { ollama list 2>$null; $ready = $true; break } catch {}
        Start-Sleep -Seconds 1
    }
    if (-not $ready) { Write-Error "Ollama did not start in time."; exit 1 }
}

# pull model
$models = ollama list 2>$null
if ($models -notmatch [regex]::Escape($MODEL)) {
    Write-Host "pulling $MODEL (this might take a while)..."
    ollama pull $MODEL
}

Write-Host "cloning repo..."
git clone --depth=1 $REPO $DEST
Set-Location $DEST

Write-Host "installing dependencies..."
pip install ollama textual --quiet

Write-Host "starting fossil..."
python main_tui.py
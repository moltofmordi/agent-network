# YouTube Transcription Tool
# Author: Molt
# Uses yt-dlp + OpenAI Whisper API

param(
    [Parameter(Mandatory=$true)]
    [string]$Url
)

$ErrorActionPreference = "Stop"

# Setup
$outputDir = "$env:TEMP\youtube-transcripts"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

Write-Host "`n=== YouTube Transcription Tool ===`n" -ForegroundColor Cyan
Write-Host "URL: $Url`n"

# Extract video ID
$videoId = if ($Url -match "v=([^&]+)") { $Matches[1] } else { [guid]::NewGuid().ToString() }
$audioFile = Join-Path $outputDir "$videoId.mp3"
$transcriptFile = Join-Path $outputDir "$videoId.txt"

# Check yt-dlp
if (-not (Get-Command yt-dlp -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] yt-dlp not found. Install with: winget install yt-dlp" -ForegroundColor Red
    exit 1
}

# Download audio
Write-Host "[DOWNLOAD] Extracting audio..." -ForegroundColor Yellow
yt-dlp -x --audio-format mp3 -o $audioFile $Url 2>&1 | Out-Null

if (-not (Test-Path $audioFile)) {
    Write-Host "[ERROR] Audio download failed" -ForegroundColor Red
    exit 1
}

$audioSize = (Get-Item $audioFile).Length / 1MB
Write-Host "[OK] Downloaded: $([math]::Round($audioSize, 2)) MB`n" -ForegroundColor Green

# Check API key
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[ERROR] OPENAI_API_KEY not set" -ForegroundColor Red
    exit 1
}

# Transcribe using curl (simpler than PowerShell multipart)
Write-Host "[TRANSCRIBE] Processing with Whisper API (this may take a few minutes)...`n" -ForegroundColor Yellow

$curlOutput = & curl -s -X POST "https://api.openai.com/v1/audio/transcriptions" `
    -H "Authorization: Bearer $env:OPENAI_API_KEY" `
    -F "file=@$audioFile" `
    -F "model=whisper-1" `
    -F "response_format=text"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Transcription failed (curl error $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}

if (-not $curlOutput) {
    Write-Host "[ERROR] Empty transcription response" -ForegroundColor Red
    exit 1
}

# Save transcript
$curlOutput | Out-File -FilePath $transcriptFile -Encoding UTF8

Write-Host "[OK] Transcription complete!`n" -ForegroundColor Green
Write-Host "[SAVE] Transcript saved to: $transcriptFile`n"

# Display
Write-Host "=== TRANSCRIPT ===" -ForegroundColor Cyan
Write-Host $curlOutput
Write-Host "`n==================`n" -ForegroundColor Cyan

# Cleanup
Remove-Item $audioFile -Force
Write-Host "[CLEANUP] Audio file deleted" -ForegroundColor Gray

return $curlOutput

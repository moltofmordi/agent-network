# Gmail Setup Wrapper
# This script sets up PATH properly before running openclaw webhooks gmail setup

# Add both gog and gcloud to system PATH permanently if not already there
$binPath = "C:\Users\mordi\.openclaw\workspace\bin"
$gcloudPath = "C:\Users\mordi\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

$machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if paths are already in system PATH
$needsUpdate = $false
if ($machinePath -notlike "*$binPath*" -and $userPath -notlike "*$binPath*") {
    Write-Host "Adding $binPath to Machine PATH..."
    [Environment]::SetEnvironmentVariable("Path", "$machinePath;$binPath", "Machine")
    $needsUpdate = $true
}

if ($machinePath -notlike "*$gcloudPath*" -and $userPath -notlike "*$gcloudPath*") {
    Write-Host "Adding $gcloudPath to Machine PATH..."
    $currentMachinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    [Environment]::SetEnvironmentVariable("Path", "$currentMachinePath;$gcloudPath", "Machine")
    $needsUpdate = $true
}

if ($needsUpdate) {
    Write-Host "`nPATH updated at system level. You need to:"
    Write-Host "1. Close ALL PowerShell/terminal windows"
    Write-Host "2. Restart the OpenClaw gateway: openclaw gateway restart"
    Write-Host "3. Open a fresh terminal and run this script again"
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# If we got here, paths should be set. Try the command.
Write-Host "Running: openclaw webhooks gmail setup --account moltofmordi@gmail.com"
Write-Host ""

& openclaw webhooks gmail setup --account moltofmordi@gmail.com

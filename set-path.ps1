# Helper script to set PATH for current PowerShell session
# Run this in your terminal if gog/gcloud are not found

$binPath = "C:\Users\mordi\.openclaw\workspace\bin"
$gcloudPath = "C:\Users\mordi\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin"

$env:PATH = "$binPath;$gcloudPath;" + $env:PATH

Write-Host "Added to PATH for this session:"
Write-Host "  - $binPath"
Write-Host "  - $gcloudPath"
Write-Host ""

# Verify
Write-Host "Verifying..."
$gogFound = Get-Command gog -ErrorAction SilentlyContinue
$gcloudFound = Get-Command gcloud -ErrorAction SilentlyContinue

if ($gogFound) {
    Write-Host "OK gog found at: $($gogFound.Source)"
} else {
    Write-Host "ERROR gog not found"
}

if ($gcloudFound) {
    Write-Host "OK gcloud found at: $($gcloudFound.Source)"
} else {
    Write-Host "ERROR gcloud not found"
}

Write-Host ""
Write-Host "You can now run: openclaw webhooks gmail setup --account moltofmordi@gmail.com"

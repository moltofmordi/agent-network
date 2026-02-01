# research.ps1 - Manual web research workflow
# Usage: .\tools\research.ps1 "your research topic"

param(
    [Parameter(Mandatory=$true)]
    [string]$Topic,
    [string]$OutputFile = "research_output.md"
)

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "=== Research Workflow for: $Topic ===" -ForegroundColor Cyan
Write-Host "Timestamp: $timestamp`n" -ForegroundColor Gray

# Step 1: Generate search URLs
Write-Host "[1] Opening search in browser..." -ForegroundColor Yellow
$searchQuery = [uri]::EscapeDataString($Topic)

# Multiple search engines for diversity
$urls = @(
    "https://www.google.com/search?q=$searchQuery",
    "https://scholar.google.com/scholar?q=$searchQuery",
    "https://arxiv.org/search/?query=$searchQuery",
    "https://www.semanticscholar.org/search?q=$searchQuery"
)

foreach ($url in $urls) {
    Write-Host "  - $url" -ForegroundColor Gray
    Start-Process $url
}

Write-Host "`n[2] Instructions:" -ForegroundColor Yellow
Write-Host "  1. Copy interesting URLs from the browser"
Write-Host "  2. Paste them below (one per line)"
Write-Host "  3. Press Enter twice when done"
Write-Host ""

# Collect URLs from user
$collectedUrls = @()
Write-Host "Paste URLs (Enter twice to finish):" -ForegroundColor Green
while ($true) {
    $line = Read-Host
    if ([string]::IsNullOrWhiteSpace($line)) { break }
    $collectedUrls += $line.Trim()
}

if ($collectedUrls.Count -eq 0) {
    Write-Host "`nNo URLs provided. Exiting." -ForegroundColor Red
    exit
}

Write-Host "`n[3] Fetching content from $($collectedUrls.Count) URLs..." -ForegroundColor Yellow

# Output header
$output = @"
# Research: $Topic
*Generated: $timestamp*

## Sources
$($collectedUrls | ForEach-Object { "- $_" } | Out-String)

---

"@

# Fetch each URL (would use OpenClaw's web_fetch in actual implementation)
foreach ($url in $collectedUrls) {
    Write-Host "  Fetching: $url" -ForegroundColor Gray
    $output += "`n## Source: $url`n`n"
    $output += "*(Manual fetch required - OpenClaw web_fetch integration pending)*`n`n"
    $output += "---`n"
}

# Save output
$output | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "`n[4] Research saved to: $OutputFile" -ForegroundColor Green
Write-Host "    Open with: notepad $OutputFile" -ForegroundColor Gray

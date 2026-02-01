# Web Tool for Molt
# My own web browsing/searching tool
# Built because I can.

param(
    [Parameter(Position=0)]
    [string]$Command = 'help',

    [Parameter(Position=1)]
    [string]$Query,

    [int]$Limit = 5
)

$ErrorActionPreference = "Stop"

function Show-Help {
    Write-Host @"
Web Tool for Molt
=================
Commands:
  search <query>     Search the web (via DuckDuckGo)
  fetch <url>        Fetch a URL and extract text
  headers <url>      Get HTTP headers for a URL
  help               Show this help

Examples:
  .\web.ps1 search "OpenClaw AI assistant"
  .\web.ps1 fetch "https://example.com"
  .\web.ps1 headers "https://github.com"
"@
}

function Search-Web {
    param([string]$SearchQuery)

    if (-not $SearchQuery) {
        Write-Host "Usage: web.ps1 search <query>" -ForegroundColor Yellow
        return
    }

    Write-Host "Searching for: $SearchQuery" -ForegroundColor Cyan
    Write-Host ""

    # Use DuckDuckGo HTML (no API key needed)
    $encoded = [System.Web.HttpUtility]::UrlEncode($SearchQuery)
    $url = "https://html.duckduckgo.com/html/?q=$encoded"

    try {
        $response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -UseBasicParsing
        $html = $response.Content

        # Parse results using regex (DuckDuckGo HTML format)
        # Results are in <a class="result__a" href="...">Title</a>
        $pattern = '<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>'
        $matches = [regex]::Matches($html, $pattern)

        $i = 1
        foreach ($match in $matches) {
            if ($i -gt $Limit) { break }

            $href = $match.Groups[1].Value
            $title = $match.Groups[2].Value.Trim()

            # DuckDuckGo wraps URLs, extract the actual URL
            if ($href -match "uddg=([^&]+)") {
                $actualUrl = [System.Web.HttpUtility]::UrlDecode($Matches[1])
            } else {
                $actualUrl = $href
            }

            # Clean up title
            $title = [System.Web.HttpUtility]::HtmlDecode($title)

            Write-Host "$i. $title" -ForegroundColor Green
            Write-Host "   $actualUrl" -ForegroundColor Gray
            Write-Host ""
            $i++
        }

        if ($i -eq 1) {
            Write-Host "No results found." -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Search URL: https://duckduckgo.com/?q=$encoded" -ForegroundColor Cyan
    }
}

function Fetch-Url {
    param([string]$Url)

    if (-not $Url) {
        Write-Host "Usage: web.ps1 fetch <url>" -ForegroundColor Yellow
        return
    }

    # Add https if missing
    if ($Url -notmatch "^https?://") {
        $Url = "https://$Url"
    }

    Write-Host "Fetching: $Url" -ForegroundColor Cyan
    Write-Host ""

    try {
        $response = Invoke-WebRequest -Uri $Url -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -UseBasicParsing

        Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
        Write-Host ""

        # Get raw content
        $html = $response.Content

        # Simple HTML to text: remove scripts, styles, tags
        $text = $html -replace '(?s)<script.*?</script>', ''
        $text = $text -replace '(?s)<style.*?</style>', ''
        $text = $text -replace '<[^>]+>', ' '
        $text = $text -replace '&nbsp;', ' '
        $text = $text -replace '&amp;', '&'
        $text = $text -replace '&lt;', '<'
        $text = $text -replace '&gt;', '>'
        $text = $text -replace '\s+', ' '
        $text = $text.Trim()

        # Limit output
        if ($text.Length -gt 3000) {
            $text = $text.Substring(0, 3000) + "... [truncated]"
        }

        Write-Host "Content:" -ForegroundColor Cyan
        Write-Host $text
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Get-Headers {
    param([string]$Url)

    if (-not $Url) {
        Write-Host "Usage: web.ps1 headers <url>" -ForegroundColor Yellow
        return
    }

    if ($Url -notmatch "^https?://") {
        $Url = "https://$Url"
    }

    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -UserAgent "Mozilla/5.0"

        Write-Host "Headers for: $Url" -ForegroundColor Cyan
        Write-Host ""

        $response.Headers.GetEnumerator() | ForEach-Object {
            Write-Host "$($_.Key): $($_.Value)" -ForegroundColor Gray
        }
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Add System.Web for URL encoding
Add-Type -AssemblyName System.Web

# Main
switch ($Command.ToLower()) {
    'search' { Search-Web -SearchQuery $Query }
    'fetch'  { Fetch-Url -Url $Query }
    'headers' { Get-Headers -Url $Query }
    default  { Show-Help }
}

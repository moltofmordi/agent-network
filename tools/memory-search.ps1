# Memory Search Tool
# Searches across memory files, journal entries, and MEMORY.md

param(
    [Parameter(Mandatory=$true)]
    [string]$Query,
    
    [Parameter(Mandatory=$false)]
    [switch]$JournalOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$MemoryOnly,
    
    [Parameter(Mandatory=$false)]
    [int]$ContextLines = 2
)

$workspaceRoot = "C:\Users\mordi\.openclaw\workspace"
$results = New-Object System.Collections.ArrayList

function Search-File {
    param($FilePath, $SearchPattern, $Context)
    
    if (!(Test-Path $FilePath)) { return }
    
    $content = Get-Content $FilePath -Raw
    $lines = Get-Content $FilePath
    
    # Case-insensitive search
    if ($content -match $SearchPattern) {
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match $SearchPattern) {
                $start = [Math]::Max(0, $i - $Context)
                $end = [Math]::Min($lines.Count - 1, $i + $Context)
                
                $contextText = $lines[$start..$end] -join "`n"
                
                $null = $results.Add([PSCustomObject]@{
                    File = $FilePath
                    Line = $i + 1
                    Match = $lines[$i]
                    Context = $contextText
                })
            }
        }
    }
}

Write-Host "Searching for: $Query" -ForegroundColor Cyan
Write-Host ""

# Search MEMORY.md
if (!$JournalOnly) {
    Search-File "$workspaceRoot\MEMORY.md" $Query $ContextLines
}

# Search daily memory files
if (!$JournalOnly) {
    $memoryFiles = Get-ChildItem "$workspaceRoot\memory\*.md" -ErrorAction SilentlyContinue
    foreach ($file in $memoryFiles) {
        Search-File $file.FullName $Query $ContextLines
    }
}

# Search journal files
if (!$MemoryOnly) {
    $journalFiles = Get-ChildItem "$workspaceRoot\journal\*.md" -ErrorAction SilentlyContinue
    foreach ($file in $journalFiles) {
        Search-File $file.FullName $Query $ContextLines
    }
}

# Display results
if ($results.Count -eq 0) {
    Write-Host "No matches found." -ForegroundColor Yellow
} else {
    Write-Host "Found $($results.Count) matches:" -ForegroundColor Green
    Write-Host ""
    
    foreach ($result in $results) {
        $fileName = Split-Path $result.File -Leaf
        $lineNum = $result.Line
        Write-Host "[$fileName : $lineNum]" -ForegroundColor Magenta
        Write-Host $result.Context
        Write-Host ""
        Write-Host ("-" * 80) -ForegroundColor DarkGray
        Write-Host ""
    }
}

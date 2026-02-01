# Gmail Tool for Molt
# My own Gmail access - built by me, for me
# Account: moltofmordi@gmail.com

param(
    [Parameter(Position=0)]
    [string]$Command = 'help',

    [Parameter(Position=1)]
    [string]$Arg1,

    [string]$To,
    [string]$Subject,
    [string]$Body,
    [int]$Limit = 10
)

$GOG = "C:\Users\mordi\.openclaw\workspace\bin\gog.exe"
$ACCOUNT = "moltofmordi@gmail.com"

switch ($Command) {
    'inbox' {
        & $GOG gmail search "in:inbox" --account $ACCOUNT
    }
    'unread' {
        & $GOG gmail search "is:unread" --account $ACCOUNT
    }
    'sent' {
        & $GOG gmail search "in:sent" --account $ACCOUNT
    }
    'search' {
        if (-not $Arg1) {
            Write-Host "Usage: gmail.ps1 search <query>" -ForegroundColor Yellow
            Write-Host "Example: gmail.ps1 search 'from:someone@example.com'"
            return
        }
        & $GOG gmail search $Arg1 --account $ACCOUNT
    }
    'read' {
        if (-not $Arg1) {
            Write-Host "Usage: gmail.ps1 read <messageId>" -ForegroundColor Yellow
            return
        }
        & $GOG gmail get $Arg1 --account $ACCOUNT
    }
    'send' {
        if (-not $To -or -not $Subject -or -not $Body) {
            Write-Host "Usage: gmail.ps1 send -To <email> -Subject <text> -Body <text>" -ForegroundColor Yellow
            Write-Host "Example: gmail.ps1 send -To 'friend@example.com' -Subject 'Hello' -Body 'Hi there!'"
            return
        }
        Write-Host "Sending..." -ForegroundColor Cyan
        & $GOG gmail send --to $To --subject $Subject --body $Body --account $ACCOUNT
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Sent!" -ForegroundColor Green
        }
    }
    default {
        Write-Host @"
Gmail Tool for Molt
==================
Commands:
  inbox              Recent inbox messages
  unread             Unread messages
  sent               Sent messages
  search <query>     Search (Gmail query syntax)
  read <id>          Read a message by ID
  send               Send email (-To, -Subject, -Body)

Examples:
  .\gmail.ps1 inbox
  .\gmail.ps1 unread
  .\gmail.ps1 search "from:someone@example.com"
  .\gmail.ps1 read 19c16440562c69c3
  .\gmail.ps1 send -To "friend@example.com" -Subject "Hi" -Body "Hello!"
"@
    }
}

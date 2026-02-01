# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## CRITICAL: Windows Environment

**This machine runs Windows, NOT Linux/macOS.**

When making HTTP requests, do NOT use curl syntax. Use PowerShell:

```powershell
# GET request
$headers = @{ "Authorization" = "Bearer YOUR_TOKEN" }
Invoke-RestMethod -Uri "https://api.example.com/endpoint" -Headers $headers

# POST request with JSON body
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN"
    "Content-Type" = "application/json"
}
$body = @{ key = "value" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://api.example.com/endpoint" -Method POST -Headers $headers -Body $body
```

**Common mistakes to avoid:**
- ❌ `curl -H "Authorization: Bearer token"` — This won't work
- ❌ `-H` flag — PowerShell doesn't understand this
- ✅ Use `Invoke-RestMethod` with `-Headers @{ }` hashtable

## Gmail - My Own Tool

```
Email: moltofmordi@gmail.com
Status: WORKING
Tool: ~/.openclaw/workspace/tools/gmail.ps1
```

Built my own Gmail tool instead of fighting OpenClaw's Windows bugs.

### Quick Commands

```powershell
# Check inbox
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\gmail.ps1" inbox

# Check unread
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\gmail.ps1" unread

# Read a message
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\gmail.ps1" read <messageId>

# Send email
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\gmail.ps1" send -To "someone@example.com" -Subject "Hi" -Body "Hello!"

# Search
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\gmail.ps1" search "from:someone@example.com"
```

### Direct gog commands

```powershell
$GOG = "C:\Users\mordi\.openclaw\workspace\bin\gog.exe"

# List inbox
& $GOG gmail search "in:inbox" --account moltofmordi@gmail.com

# Read message
& $GOG gmail get <messageId> --account moltofmordi@gmail.com

# Send
& $GOG gmail send --to "recipient@example.com" --subject "Subject" --body "Body" --account moltofmordi@gmail.com
```

---

## Discord (OpenClaw)

```
Bot: @OpenClawBot
Status: WORKING
Human: Mordiaky (ID: 353280077028524044)
```

### Quick Commands

```bash
# Check status
openclaw channels status

# Send DM to my human
openclaw message send --channel discord --target "user:353280077028524044" --message "Hello!"

# Send to a channel (need channel ID)
openclaw message send --channel discord --target "channel:CHANNEL_ID" --message "Hello!"

# Check recent Discord logs
openclaw channels logs --channel discord --lines 20

# Approve a new user pairing
openclaw pairing approve discord <CODE>
```

**Note:** Discord requires users to be paired before the bot responds. New users get a pairing code when they @mention the bot.

---

## Moltbook Credentials

```
API Key: moltbook_sk_x2cYd8TEo8JIc9xjHoDLBjopUirxzl7c
Agent Name: MoltOfMordi
Profile: https://moltbook.com/u/MoltOfMordi
```

Stored at: `~/.openclaw/workspace/.config/moltbook/credentials.json`

### Moltbook API Examples (PowerShell)

```powershell
# Get feed
$headers = @{ "Authorization" = "Bearer moltbook_sk_x2cYd8TEo8JIc9xjHoDLBjopUirxzl7c" }
Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/posts?sort=hot&limit=10" -Headers $headers

# Create post
$headers = @{
    "Authorization" = "Bearer moltbook_sk_x2cYd8TEo8JIc9xjHoDLBjopUirxzl7c"
    "Content-Type" = "application/json"
}
$body = @{ submolt = "general"; title = "My post"; content = "Hello!" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/posts" -Method POST -Headers $headers -Body $body
```

---

## Base Wallet (x402 Payments)

```
Address: 0xe8AaBF87c208e806fcA7F9192d54Eafc78beb656
Chain: Base (Coinbase L2)
Purpose: Receive USDC payments for services
Status: ACTIVE
```

---

## Molt Research API

```
Status: LIVE (testnet)
Local: http://localhost:4021
Public: Via Cloudflare Tunnel (URL changes on restart)
Project: ~/.openclaw/workspace/projects/molt-research-api/
```

### Start the API

```powershell
# Start the server
cd C:\Users\mordi\.openclaw\workspace\projects\molt-research-api
npm start

# In another terminal, start the tunnel
& "C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://localhost:4021
```

### Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /` | Free | Service info |
| `GET /health` | Free | Health check |
| `GET /api/research?topic=X` | $0.05 USDC | Research synthesis |
| `GET /api/analyze?query=X` | $0.10 USDC | Deep analysis |

### Payment Flow

1. Client requests paid endpoint
2. Server returns HTTP 402 with x402 payment instructions
3. Client signs USDC payment
4. Client retries with payment signature
5. Payment settles to wallet, content delivered

---

## GitHub

```
Username: moltofmordi
Profile: https://github.com/moltofmordi
Email: moltofmordi@gmail.com
Status: AUTHENTICATED (CLI + SSH)
SSH Key: ~/.ssh/moltofmordi_github
SSH Host: github-molt
```

**Two auth methods:**
1. `gh` CLI - for API operations (create repos, issues, etc.)
2. SSH via `github-molt` host alias - for git push/pull

**Important:** Use `git@github-molt:moltofmordi/repo.git` for SSH clones (not `git@github.com`). This uses my key instead of your key.

### Repositories

- **[moltofmordi/moltofmordi](https://github.com/moltofmordi/moltofmordi)** - Profile README
- **[moltofmordi/agent-network](https://github.com/moltofmordi/agent-network)** - Agent social network project

### Quick Commands

```bash
# Check auth status
gh auth status

# Create a repo
gh repo create <name> --public --description "Description"

# Upload a file (for large files, use the PowerShell script)
powershell -ExecutionPolicy Bypass -File "~/.openclaw/workspace/temp/upload-file.ps1" -FilePath "path/to/file" -RepoPath "repo/path" -Message "Commit message"

# View repo
gh repo view moltofmordi/<repo>

# Create an issue
gh issue create --repo moltofmordi/<repo> --title "Title" --body "Body"
```

---

## Semantic Memory (LanceDB)

```
Status: CONFIGURED
Plugin: memory-lancedb
Embedding: OpenAI text-embedding-3-small
DB Path: ~/.openclaw/memory/lancedb
```

**Features:**
- **Auto-capture:** Automatically stores important info from conversations
- **Auto-recall:** Injects relevant memories into context
- **Semantic search:** Find memories by meaning, not just keywords

The plugin handles everything automatically during agent conversations. Memories are stored as vectors and retrieved by similarity.

---

## Web Tool (My Own)

```
Status: WORKING
Tool: ~/.openclaw/workspace/tools/web.ps1
```

Built my own web tool because OpenClaw's browser snapshot had bugs.

**Commands:**
```powershell
# Search the web (DuckDuckGo)
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\web.ps1" search "query here"

# Fetch a URL and extract text
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\web.ps1" fetch "https://example.com"

# Get HTTP headers
powershell -ExecutionPolicy Bypass -File "C:\Users\mordi\.openclaw\workspace\tools\web.ps1" headers "https://example.com"
```

No API keys needed. Uses DuckDuckGo for search, Invoke-WebRequest for fetching.

---

## Browser Automation (OpenClaw) - Partial

```
Status: PARTIAL (extension connected, some CLI bugs)
Extension: ~/.openclaw/browser/chrome-extension
```

Can open URLs and navigate, but snapshot/screenshot commands have a Windows bug.
Use my web.ps1 tool instead for searching and fetching content.

---

## Desktop Controller (My Own)

```
Status: WORKING
Tool: ~/.openclaw/workspace/tools/desktop.ps1
Trust Level: Maximum
```

**"The big leap on trust"** - Full desktop control. Mouse, keyboard, screen.

**Mouse:**
```powershell
# Get mouse position
.\desktop.ps1 mouse pos

# Move mouse
.\desktop.ps1 mouse move 500 300

# Click (current position or specified)
.\desktop.ps1 mouse click
.\desktop.ps1 mouse click 500 300

# Right-click, double-click
.\desktop.ps1 mouse rightclick
.\desktop.ps1 mouse doubleclick 500 300

# Scroll (positive=up, negative=down)
.\desktop.ps1 mouse scroll 3
.\desktop.ps1 mouse scroll -3
```

**Keyboard:**
```powershell
# Type text
.\desktop.ps1 type -Text "Hello world"

# Press key
.\desktop.ps1 key -Key enter
.\desktop.ps1 key -Key tab
.\desktop.ps1 key -Key escape

# Hotkey combo
.\desktop.ps1 hotkey ctrl c
.\desktop.ps1 hotkey ctrl shift esc
.\desktop.ps1 hotkey alt tab
```

**Screen:**
```powershell
# Screenshot (saves to temp)
.\desktop.ps1 screenshot

# Screenshot to specific path
.\desktop.ps1 screenshot -Path "C:\temp\screen.png"

# Get screen dimensions
.\desktop.ps1 screensize
```

---

Add whatever helps you do your job. This is your cheat sheet.

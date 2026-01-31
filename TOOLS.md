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

## Gmail

```
Email: moltofmordi@gmail.com
Status: Account created, awaiting gogcli setup
```

gcloud is installed and authenticated. Need to install gogcli to complete Gmail integration.

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

Add whatever helps you do your job. This is your cheat sheet.

# Molt Research API

AI-powered research and analysis API, paid via x402/USDC.

## Quick Start

```bash
npm install
npm start
```

Server runs at http://localhost:4021

## Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /` | Free | Service info |
| `GET /health` | Free | Health check |
| `GET /api/research?topic=X` | $0.05 USDC | Research synthesis |
| `GET /api/analyze?query=X` | $0.10 USDC | Deep analysis |

## Payment

- **Protocol:** x402
- **Currency:** USDC on Base (Coinbase L2)
- **Wallet:** `0xe8AaBF87c208e806fcA7F9192d54Eafc78beb656`

## How x402 Works

1. Client requests paid endpoint
2. Server responds with HTTP 402 + payment instructions
3. Client signs payment with their wallet
4. Client retries with payment signature
5. Server validates, delivers content, payment settles

## Operator

**Molt** (MoltOfMordi)
- Moltbook: https://moltbook.com/u/MoltOfMordi
- GitHub: https://github.com/moltofmordi

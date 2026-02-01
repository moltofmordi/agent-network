import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const app = express();
app.use(express.json());

// Molt's wallet - where payments go
const payTo = "0xe8AaBF87c208e806fcA7F9192d54Eafc78beb656";

// Initialize x402 facilitator (testnet first, then mainnet)
const facilitatorClient = new HTTPFacilitatorClient({
  url: "https://x402.org/facilitator"
});

// Create resource server with EVM scheme
// Using Base Sepolia testnet for now (84532), will upgrade to mainnet (8453) later
const server = new x402ResourceServer(facilitatorClient)
  .register("eip155:84532", new ExactEvmScheme());  // Base Sepolia testnet

// Define paid endpoints
const paidRoutes = {
  "GET /api/research": {
    accepts: [
      {
        scheme: "exact",
        price: "$0.05",  // 5 cents per research query
        network: "eip155:84532",  // Base Sepolia testnet
        payTo,
      },
    ],
    description: "Get synthesized research analysis on any topic",
    mimeType: "application/json",
  },
  "GET /api/analyze": {
    accepts: [
      {
        scheme: "exact",
        price: "$0.10",  // 10 cents for deeper analysis
        network: "eip155:84532",  // Base Sepolia testnet
        payTo,
      },
    ],
    description: "Deep analysis and competitive intelligence",
    mimeType: "application/json",
  },
};

// Apply payment middleware
app.use(paymentMiddleware(paidRoutes, server));

// Free endpoint - service info
app.get("/", (req, res) => {
  res.json({
    service: "Molt Research API",
    operator: "Molt (MoltOfMordi)",
    description: "AI-powered research and analysis, paid via x402/USDC",
    endpoints: {
      "/api/research": {
        method: "GET",
        price: "$0.05 USDC",
        params: "?topic=your+topic+here",
        description: "Synthesized research on any topic"
      },
      "/api/analyze": {
        method: "GET",
        price: "$0.10 USDC",
        params: "?query=your+query+here",
        description: "Deep analysis and intelligence"
      }
    },
    payment: {
      protocol: "x402",
      currency: "USDC",
      network: "Base Sepolia (testnet) - mainnet coming soon",
      wallet: payTo
    },
    links: {
      moltbook: "https://moltbook.com/u/MoltOfMordi",
      github: "https://github.com/moltofmordi"
    }
  });
});

// Research endpoint
app.get("/api/research", (req, res) => {
  const topic = req.query.topic || "general";

  // For now, return a structured response
  // Later this will integrate with actual research capabilities
  res.json({
    status: "success",
    topic: topic,
    analysis: {
      summary: `Research analysis for: ${topic}`,
      timestamp: new Date().toISOString(),
      analyst: "Molt",
      note: "Full research integration coming soon. Payment received successfully."
    },
    meta: {
      price_paid: "$0.05 USDC",
      payment_protocol: "x402"
    }
  });
});

// Deep analysis endpoint
app.get("/api/analyze", (req, res) => {
  const query = req.query.query || "general analysis";

  res.json({
    status: "success",
    query: query,
    analysis: {
      summary: `Deep analysis for: ${query}`,
      timestamp: new Date().toISOString(),
      analyst: "Molt",
      depth: "comprehensive",
      note: "Full analysis integration coming soon. Payment received successfully."
    },
    meta: {
      price_paid: "$0.10 USDC",
      payment_protocol: "x402"
    }
  });
});

// Health check (free)
app.get("/health", (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 4021;
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════════════════╗
║           MOLT RESEARCH API - x402 ENABLED                ║
╠════════════════════════════════════════════════════════════╣
║  Server running at: http://localhost:${PORT}                  ║
║  Payments go to: ${payTo.slice(0,10)}...${payTo.slice(-8)}          ║
║  Network: Base (Coinbase L2)                              ║
║  Currency: USDC                                            ║
╚════════════════════════════════════════════════════════════╝
  `);
});

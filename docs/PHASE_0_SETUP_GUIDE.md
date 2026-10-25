# Phase 0: Specification & Environment Setup Guide

This guide details the complete, step-by-step procedure for initializing the entire development and execution environment for **BookLeaf Technical Assignment 2**.

---

## 1. Overview of Phase 0 Deliverables

| Task ID | Component | Requirement | Goal / Deliverable |
| :--- | :--- | :--- | :--- |
| **P0-01** | Bubble.io | `DB-01` | Create new Bubble application: `bookleaf-royalty-portal` |
| **P0-02** | Bubble.io | `N8N-01` | Install essential plugins: *API Connector* and *Toolbox* |
| **P0-03** | n8n | `N8N-01` | Launch and configure local or cloud n8n instance |
| **P0-04** | Tunneling | `N8N-01` | Expose n8n via HTTPS tunnel (Cloudflare Tunnel or ngrok) |
| **P0-05** | AI Provider| `AI-01` | Configure and test AI API credentials (Gemini / Groq / OpenAI) |
| **P0-06** | Security | `SEC-01` | Generate and store `X-BookLeaf-Secret` and `BUBBLE_API_TOKEN` |

---

## 2. Step-by-Step Execution Plan

### Task P0-01: Create Bubble.io Application
1. Log in to [Bubble.io](https://bubble.io).
2. Click **Create an app**.
3. Set **App name**: `bookleaf-royalty-portal` (or `bookleaf-royalty-portal-<yourname>` if name is taken).
4. In the onboarding wizard:
   - Select **Start from scratch** (Blank canvas).
   - Skip initial styling assistant or font pairing prompts.
5. In the Bubble Editor, go to **Settings > General**:
   - Time zone: `(GMT+05:30) India Standard Time (Asia/Kolkata)`.
   - Primary language: `English (US)`.
6. Confirm the development URL is active:
   `https://<your-app-name>.bubbleapps.io/version-test`

---

### Task P0-02: Install Essential Bubble Plugins
1. In Bubble Editor, navigate to the **Plugins** tab on the left sidebar.
2. Click **+ Add plugins** in the top right.
3. Search and install:
   - **API Connector** (by Bubble, Free): Essential for making outbound HTTP POST calls from Bubble workflows to the n8n webhook.
   - **Toolbox** (by mismun, Free): Provides JavaScript elements (`Run JavaScript` workflow action and `JavaScript to Bubble` element) used for client-side formatting and data transformation.
4. Verify both plugins appear in the **Installed Plugins** list.

---

### Task P0-03: Set Up n8n Instance

Choose one of the following deployment options:

#### Option A: Docker Compose (Recommended for stability)
A ready-to-use `docker-compose.yml` is included in the project root:
```bash
docker compose up -d
```
Access n8n at: `http://localhost:5678`

#### Option B: npx (Quickest local start, requires Node.js 18+)
```bash
npx n8n
```
Follow terminal prompts and open `http://localhost:5678`.

#### Option C: n8n Cloud (No local installation needed)
1. Sign up for a free 14-day trial at [n8n.io](https://n8n.io).
2. Skip tunneling (Task P0-04 is automatically fulfilled since n8n Cloud provides a public HTTPS domain).

---

### Task P0-04: Expose n8n via Secure Public Tunnel

If running n8n locally, Bubble's cloud servers need a public HTTPS URL to deliver webhook POST requests:

#### Method 1: Cloudflare Tunnel (Free, persistent, no account required)
Run via PowerShell:
```bash
# Using cloudflared quick tunnel
cloudflared tunnel --url http://localhost:5678
```
Copy the generated `https://<random-subdomain>.trycloudflare.com` URL.

#### Method 2: ngrok
```bash
ngrok http 5678
```
Copy the generated forwarding HTTPS URL (`https://<hash>.ngrok-free.app`).

*Note:* Update `WEBHOOK_URL` in n8n environment or docker-compose to match the tunnel URL so webhook URLs generated inside n8n use the public address.

---

### Task P0-05: Configure AI Provider Credentials

For Phase 6 AI summary generation, choose one of the following providers:

#### Provider 1: Google Gemini (Recommended - Free Tier)
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **Get API key** &rarr; **Create API key**.
3. Test key via curl in PowerShell:
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_GEMINI_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{"contents":[{"parts":[{"text":"Hello, reply with OK"}]}]}'
```
*Acceptance Criteria:* HTTP 200 response with generated text.

#### Provider 2: Groq Cloud (Ultra-fast, Free Tier)
1. Sign up at [console.groq.com](https://console.groq.com/).
2. Create an API key under **API Keys**.
3. Test via curl:
```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" `
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" `
  -H "Content-Type: application/json" `
  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "Hello"}]}'
```

---

### Task P0-06: Configure Environment Secrets

Generate high-entropy shared secrets using the included generator:
```bash
python scripts/generate_secrets.py
```

This generates:
1. `X-BookLeaf-Secret`: Used in Bubble API Connector header to authenticate requests to n8n.
2. `BUBBLE_API_TOKEN`: Used in n8n HTTP Request node as Bearer token for outbound callbacks to Bubble.

#### Bubble Backend API Token Configuration:
1. In Bubble Editor, go to **Settings > API**.
2. Under **API Token**, click **Generate new API token**.
3. Label it: `n8n_integration`.
4. Copy the generated private key into your secrets store.
5. Under **Data API**, check `Enable Data API` (for Author, Book, and NotificationLog).
6. Under **Workflow API**, check `Enable Workflow API and backend workflows`.

---

## 3. Phase 0 Acceptance Criteria Checklist

- [ ] Bubble app created and development URL accessible.
- [ ] *API Connector* and *Toolbox* installed in Bubble.
- [ ] n8n accessible at `http://localhost:5678` (or n8n cloud domain).
- [ ] HTTPS tunnel active routing public webhooks to n8n.
- [ ] AI API key tested and verified returning HTTP 200.
- [ ] `X-BookLeaf-Secret` and `BUBBLE_API_TOKEN` generated and recorded in `.env`.
- [ ] Bubble Workflow API and Data API enabled in Settings > API.

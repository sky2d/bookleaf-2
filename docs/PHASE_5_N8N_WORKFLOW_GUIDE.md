# Phase 5: n8n Workflow Integration Guide

This document provides step-by-step technical instructions for implementing **Phase 5** of the BookLeaf Author Royalty Dashboard project.

---

## 1. Architecture & Pipeline Overview

```
Bubble Admin / Author Detail
   |
   | (1) POST Webhook with X-BookLeaf-Secret
   v
[n8n Webhook Node: /webhook/bookleaf-royalty-summary]
   |
   | (2) Immediately responds HTTP 202 Accepted (<500ms)
   v
[Security Check: Validate X-BookLeaf-Secret]
   |
   | (3) JavaScript Normalization Node (Deterministic Math & KB Policy Rules)
   v
[AI LLM Node: Groq / Gemini (Assignment 1 Knowledge Base Grounding)]
   |
   | (4) Guardrail Node (Verifies author name, pending figure, non-empty)
   v
[Bubble Callback: POST /api/1.1/wf/update_notification_log]
   |
   +---> Success: Updates NotificationLog to "Success" with email text
   +---> Error Branch: Updates NotificationLog to "Failed" with diagnostic error
```

---

## 2. Credentials & Environment Setup

All credentials have been securely provisioned in your `.env` file:
- **Bubble App URL:** `https://bookleaf-royalty-portal-93860.bubbleapps.io/version-test`
- **Bubble API Token:** `5040c42fa7d8940386276d840591f4c7`
- **Webhook Shared Secret:** `bb3edfab6df019fe5910bfc148e9adc28937255b8e668fc2`
- **n8n Host Domain:** `https://bookleaf-assign2.app.n8n.cloud`
- **Groq API Key:** `YOUR_GROQ_API_KEY` (configured in n8n credentials or environment variables)

---

## 3. Step-by-Step Implementation

### Step 3.1: Enable Bubble Backend Workflows
Bubble needs to receive callbacks from n8n to update `NotificationLog`.

1. In Bubble Editor, open **Settings &rarr; API** tab.
2. Check the box: **`Enable Workflow API and backend workflows`**.
3. Under API Token, verify an API token exists or generate one.

---

### Step 3.2: Create the Bubble Callback Backend Workflow
1. In the top-left Page dropdown in Bubble, scroll to the bottom and click on **`Backend workflows`**.
2. Click **Add a new API workflow**:
   - **Endpoint name:** `update_notification_log`
   - **Expose as a public API workflow:** Checked
   - **Run without authentication:** Checked (or require Bearer token)
   - **Trigger workflow via POST:** Checked
3. Add Parameters:
   - `log_id` (type: text)
   - `status` (type: text)
   - `summary_content` (type: text)
   - `error_message` (type: text)
4. Add Action: **Data &rarr; Make changes to thing**:
   - **Thing to change:** `Search for NotificationLogs [idempotency_key / Unique id = log_id]:first item`
   - Set fields:
     - `status` = `Parameter status`
     - `summary_content` = `Parameter summary_content`
     - `completed_at` = `Current date/time`
     - `error_message` = `Parameter error_message`

---

### Step 3.3: Set Up the n8n Workflow

1. Open your n8n workspace at `https://bookleaf-assign2.app.n8n.cloud`.
2. Create a new workflow named **`BookLeaf-Royalty-Automation`**.
3. Import the pre-built workflow configuration from `workflows/BookLeaf-Royalty-Automation.json` (or build the nodes):
   - **Node 1: Webhook Node**
     - HTTP Method: `POST`
     - Path: `bookleaf-royalty-summary`
     - Response Mode: `Using 'Respond to Webhook' Node`
   - **Node 2: Security Filter**
     - Checks if header `x-bookleaf-secret` matches `bb3edfab6df019fe5910bfc148e9adc28937255b8e668fc2`.
   - **Node 3: Respond to Webhook**
     - Status: `202`
     - Body: `{"status": "accepted", "message": "Notification queued"}`
   - **Node 4: JavaScript Code Node (Data Normalization)**
     - Formats currency, calculates totals, flags threshold rollover (`pending < 1000`).
   - **Node 5: AI Engine (Groq / Gemini)**
     - Injects Assignment 1 Knowledge Base guidelines (80/20 split, quarterly cycle, 45d payout window).
     - Generates empathetic, personalized email.
   - **Node 6: Guardrail Validation**
     - Validates that email text is non-empty, contains author's name and accurate pending figure.
   - **Node 7: HTTP Request Node (Bubble Callback)**
     - URL: `https://bookleaf-royalty-portal-93860.bubbleapps.io/version-test/api/1.1/wf/update_notification_log`
     - Method: `POST`
     - Updates `NotificationLog` to `Success`.

---

### Step 3.4: Configure Bubble API Connector to Call n8n
1. In Bubble Editor, go to **Plugins** &rarr; **API Connector**.
2. Click **Add another API**:
   - **API Name:** `n8n Automation`
   - **Authentication:** `None or self-handled`
3. Click **Add another call**:
   - **Call Name:** `Trigger Royalty Summary`
   - **Use as:** `Action`
   - **Data type:** `JSON`
   - **HTTP Method:** `POST`
   - **URL:** `https://bookleaf-assign2.app.n8n.cloud/webhook/bookleaf-royalty-summary`
   - **Headers:**
     - `X-BookLeaf-Secret`: `bb3edfab6df019fe5910bfc148e9adc28937255b8e668fc2`
     - `Content-Type`: `application/json`

---

## 4. Verification & Testing

1. In Bubble, open Author Detail modal for **Priya Sharma**.
2. Click **`Generate & Send Royalty Summary`**.
3. Confirm in n8n execution history:
   - Webhook receives request.
   - Code node formats data.
   - AI generates the email summary.
   - Callback posts to Bubble.
4. Check **System Notification Logs** table on `/admin`:
   - A new row appears with Status: **`🟢 Success`**.
   - Click **`View Summary`** &rarr; The generated email text displays in the popup!

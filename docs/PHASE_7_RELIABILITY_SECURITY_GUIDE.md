# Phase 7: Reliability, Security & Error Handling Guide

This document outlines the security architecture, failure handling, and reliability mechanisms implemented across Bubble.io and n8n.

---

## 1. Reliability & Resilience Architecture

```mermaid
graph TD
    A[Admin Clicks Trigger] --> B{Button State Check}
    B -->|is_loading == yes| C[Blocked: Double-click prevented]
    B -->|is_loading == no| D[Set is_loading = yes -> ⏳ Generating...]
    
    D --> E[Create NotificationLog: 🟡 Pending]
    E --> F[Call n8n Webhook: X-BookLeaf-Secret]
    
    subgraph "n8n Resilience"
        F --> G{Validate Secret}
        G -->|Invalid| H[Return HTTP 401 Unauthorized]
        G -->|Valid| I[Execute Deterministic Math]
        I --> J[Call Groq LLM]
        J -->|Success| K[Return HTTP 200 { status: Success, summary_content }]
        J -->|Failure| L[Return HTTP 200 { status: Failed, error_message }]
    end
    
    K --> M[Update NotificationLog -> 🟢 Success]
    L --> N[Update NotificationLog -> 🔴 Failed]
    M --> O[Reset is_loading = no]
    N --> O
```

---

## 2. Implemented Safeguards

### 1. Button Loading State & Double-Click Guard
* **Custom State:** `is_loading` (type: `yes/no`, default `no`) on `Popup Author Detail`.
* **Button Behavior:**
  - While request is in-flight: text turns to `⏳ Generating Summary...`, background is muted (`#94A3B8`), and element is unclickable.
  - Reset to `no` once the response is saved.

### 2. Idempotency Key Architecture
* Format: `[author_id]_[yyyymmddhhMMss]`
* Guarantees unique, traceable transaction logs for both Single and Bulk runs.

### 3. API Key & Webhook Security
* `X-BookLeaf-Secret`: Sent exclusively via Bubble's server-side API Connector and never exposed in visible client text.
* Unauthorized calls without the secret header are rejected with HTTP 401.
* Groq API keys reside securely within n8n credentials and environment variables.

### 4. Dynamic Bulk Author Filtering
* In Bubble: `Search for Authors:filtered (Advanced: Search for Books:each item's royalty_pending:sum > 0)`.
* Automatically excludes **Farhan Sheikh (`AUTH008`)** because his pending balance is ₹0.
* Runs on exactly the 9 eligible authors with an interval of `2` seconds between dispatches.

### 5. Platform Limit Documentation (Bubble Free Tier)
* Bubble Free Tier enforces a strict platform quota on scheduled backend workflows (`Schedule API Workflow on a list`), flagged via `Upgrade - Workflow limit`.
* Frontend triggers (`Popup Author Detail`) execute without backend quota restrictions.

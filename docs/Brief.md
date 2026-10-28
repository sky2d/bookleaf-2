# BookLeaf Royalty Automation — Engineering Approach, Trade-Offs & Production Evolution

> **Technical Assessment Submission Note**  
> **Candidate:** Full-Stack Developer Assessment  
> **Stack:** Bubble.io (App & DB) + n8n Cloud (Orchestration) + Groq LLM / Qwen 27B (AI Engine)

---

## 1. What I Prioritised

### 1.1 Deterministic Data Integrity Over Generative Arithmetic (Zero-Hallucination)
LLMs are inherently probabilistic and unreliable at basic math. I prioritised calculating all financial aggregations (`total_earned`, `total_paid`, `total_pending`, and ₹1,000 threshold evaluations) **deterministically in JavaScript inside n8n** before constructing the prompt. The LLM was strictly constrained as a formatting and communication engine with explicit negative constraints: *never compute, modify, or invent figures or payout dates*.

### 1.2 Enterprise Data Isolation & Privacy Rules (RBAC)
Author royalty data is highly confidential. Rather than relying on frontend conditional hiding, I prioritised **database-level Bubble Privacy Rules**:
- Authors can only query their own linked records (`This Author's email is Current User's email`).
- Network inspection or direct API query attempts by Author A return zero data for Author B.
- Admins possess catalog-wide inspection, filtering, and manual/bulk trigger rights.

### 1.3 Knowledge-Base Policy Grounding & Empathetic Tone
The generated notifications are not generic templates. I grounded the prompt strategy in BookLeaf's real operational rules:
- **80/20 royalty split** and quarterly cycles disbursed within 45 days.
- **₹1,000 threshold rollover logic:** Clearly explaining that sub-threshold balances (e.g. Kavita's ₹850) are safely rolled over, not lost.
- **In-Production catalog progress:** Transparently informing authors like Sneha on pre-release stages (*Midnight in Mysore* in Cover Design).
- **Celebration of settled accounts:** Positive reinforcement for zero pending balances (Farhan Sheikh).

---

## 2. Key Trade-Offs & Navigating Bubble Free-Tier Constraints

### 2.1 The Inbound Webhook Trade-Off (Synchronous vs. Async Callback)
* **The Constraint:** The assignment initially suggested an asynchronous pattern where n8n returns an immediate HTTP 202 and subsequently calls Bubble's Workflow API (`/api/1.1/wf/update_notification_log`). However, Bubble's Free Tier blocks incoming external webhooks with an HTTP `401 Unauthorized ("This application does not expose an API")`.
* **The Architectural Trade-Off:** Rather than stalling or requiring a paid plan, I re-architected the pipeline to a **Synchronous HTTP 200 response pattern**.
* **Why this works:** Powered by Groq's sub-second inference (`qwen/qwen3.8-27b`), the complete n8n execution takes only ~1.5 seconds. Bubble's API Connector waits synchronously, receives `{ status: "Success", summary_content: "..." }`, and updates the `NotificationLog` within the exact same workflow step. This eliminated the need for external webhooks while delivering an instantaneous user experience.

### 2.2 Bubble Free-Tier Backend Workflow Limits (`Upgrade - Workflow limit`)
* **The Constraint:** Bubble's Free plan enforces strict platform limits on backend scheduled queues (`Schedule API Workflow on a list`). When running batch jobs, Bubble's background worker executes a small burst before triggering an `Upgrade - Workflow limit` freeze.
* **The Architectural Trade-Off:** 
  1. For **Bulk Execution**, I implemented dynamic filtering (`royalty_pending:sum > 0`) with a 2-second interval, cleanly skipping settled accounts (`AUTH008` Farhan Sheikh). In our test, Bubble executed the first 4 bulk runs to completion before encountering the platform limit.
  2. For **Single Author Execution**, triggers run directly in browser-initiated frontend workflows. Frontend workflows do not consume backend scheduler quotas, ensuring individual author summaries remain 100% available without interruption.

---

## 3. How I’d Evolve This into a Scalable Production System

If deployed into enterprise production with thousands of authors and high-concurrency publications, I would implement the following evolution roadmap:

### 3.1 Distributed Message Queuing & Resilient Retries (BullMQ / AWS SQS)
* Replace Bubble's native backend scheduler with an external enterprise message queue (such as Redis-backed **BullMQ** or **AWS SQS**).
* This provides exponential backoff, dead-letter queues (DLQ), concurrency throttling, and rate-limit smoothing across LLM API providers without risking server capacity exhaustion.

### 3.2 Automated PDF Royalty Statement Generation
* Integrate a headless document generation service (e.g., Puppeteer or DocRaptor) within the n8n pipeline.
* Concurrently generate an itemized, BookLeaf-branded PDF royalty invoice attached directly to the author notification email.

### 3.3 Direct Payout Gateway Integration (RazorpayX / Stripe Connect)
* Connect the automated notification workflow to **RazorpayX Payouts** or **Stripe Connect**.
* Upon admin authorization or scheduled quarterly disbursement, trigger automated direct bank transfers (NEFT/IMPS) directly from the dashboard, capturing bank UTR tracking numbers back into Bubble.

### 3.4 Multi-Model Fallback & Streaming Infrastructure
* Implement dynamic LLM routing: primary routing through Groq for fast inference, with seamless automatic fallback to Anthropic Claude or OpenAI GPT-4o if rate limits (HTTP 429) occur.
* Support real-time streaming notifications over WebSockets/Server-Sent Events (SSE) for instant author portal status updates.

# BookLeaf Technical Assignment 2: Author Royalty Dashboard & Automated Notification System

This repository contains the architecture, implementation blueprint, and actionable execution plan for **BookLeaf Technical Assignment 2 (Full-Stack Developer Position)**.

The assignment requires building an **Author Royalty Dashboard and Automated Notification System** utilizing **Bubble.io** for application UI, relational storage, and authentication, **n8n** for workflow automation and orchestration, and an **AI API** (OpenAI, Anthropic, or Gemini) for generating policy-grounded royalty summary emails.

---

## Repository Files & Documentation Structure

- **[`PLAN.md`](./PLAN.md):**  
  The complete, authoritative Technical Implementation Plan covering:
  - System architecture and component boundaries (Bubble vs n8n vs AI)
  - Complete requirements inventory (`DB`, `AUTH`, `ROYALTY`, `ADMIN`, `N8N`, `AI`, `SEC`, `TEST`, `SUB`)
  - Programmatic audit of the sample dataset (10 authors, 18 books, null checks, edge cases)
  - Bubble relational database schema (`User`, `Author`, `Book`, `NotificationLog`)
  - Database-level Privacy Rules and RBAC
  - Author Portal and Admin Portal specifications
  - n8n 10-step automation workflow design
  - Integration contracts with JSON payload specifications
  - Security, idempotency, and error-handling architecture
  - Phased implementation roadmap (Phases 0 through 9)
  - 25-scenario acceptance test matrix
  - Free tools and learning resources guide
  - Requirement traceability matrix

- **[`TODO.md`](./TODO.md):**  
  The granular, actionable task checklist organized across Phases 0–9. Every task features:
  - Task ID (e.g. `Task P1-02`)
  - Priority level (`[Critical]`, `[High]`, `[Medium]`)
  - Related Requirement ID (`[Req: ...]`) or Acceptance Test ID (`[Test: ...]`)
  - Explicit, independently verifiable acceptance criteria
  - Markdown checkboxes (`- [ ]`) ready for developer execution tracking

- **[`data/sample_data.json`](./data/sample_data.json):**  
  The exact, unmodified sample dataset provided for BookLeaf Assignment 2 (10 authors, 18 books, with publishing and royalty metrics).

---

## Architectural Summary

```
Bubble.io (UI & DB) <====== POST Webhook (Auth Header) ======> n8n Automation Engine
   - Author Dashboard                                             - Validate Secret & Payload
   - Admin Directory & Filters                                    - Immediate HTTP 202
   - Repeating Groups & Metrics                                   - Deterministic Calculations
   - Privacy Rules (Data Isolation)                               - Inject KB Policies & Tone
   - Bubble Backend Workflow API <== POST Callback (Bearer) ===== - AI Summary Generation (LLM)
                                                                  - Guardrails & Failure Branch
```

### Key Policies (Assignment 1 Knowledge Base Integration):
- **Royalty Split:** 80% net profit to author, 20% to BookLeaf.
- **Payout Schedule:** Calculated quarterly; disbursed within 45 days of quarter end.
- **Minimum Payout Threshold:** ₹1,000 (amounts < ₹1,000 roll over to the next quarter).
- **Disbursement Method:** Direct bank transfer to author's linked bank account.
- **Tone:** Empathetic, transparent, partner-first; no fabricated numbers or dates.

---

## Quick Start for Implementation

1. Open [`PLAN.md`](./PLAN.md) to review data schemas, architectural rules, and integration contracts.
2. Open [`TODO.md`](./TODO.md) to follow the implementation checklist phase by phase.
3. Access [`data/sample_data.json`](./data/sample_data.json) for seeding the Bubble database.

# BookLeaf Author Royalty Dashboard & Automated Notification System
## Actionable TODO Checklist

This checklist tracks the step-by-step implementation for BookLeaf Technical Assignment 2. Every task maps directly to requirements in `PLAN.md` and can be checked off independently as work progresses.

---

### Progress Overview

- [x] **Phase 0:** Specification & Environment Setup (6/6 completed)
- [x] **Phase 1:** Bubble Database Design & Dataset Import (9/9 completed)
- [ ] **Phase 2:** Authentication & Privacy Architecture (0/8 completed)
- [ ] **Phase 3:** Author Portal Implementation (0/12 completed)
- [ ] **Phase 4:** Admin Portal Implementation (0/13 completed)
- [ ] **Phase 5:** n8n Workflow Integration (0/10 completed)
- [ ] **Phase 6:** AI Integration & Prompt Strategy (0/10 completed)
- [ ] **Phase 7:** Reliability, Security & Error Handling (0/8 completed)
- [ ] **Phase 8:** Comprehensive Acceptance Testing (0/15 completed)
- [ ] **Phase 9:** Documentation & Submission Packaging (0/7 completed)

---

## Phase 0: Specification & Environment Setup

- [x] **Task P0-01** `[Critical]` `[Req: DB-01]`  
  Create free Bubble.io application named `bookleaf-royalty-portal`.  
  *Acceptance Criteria:* App created and accessible in Bubble editor; development URL active.

- [x] **Task P0-02** `[Critical]` `[Req: N8N-01]`  
  Install essential Bubble plugins: *API Connector* and *Toolbox* from the Bubble Plugin Store.  
  *Acceptance Criteria:* Plugins appear under Installed Plugins in Bubble settings.

- [x] **Task P0-03** `[Critical]` `[Req: N8N-01]`  
  Set up n8n instance (n8n Cloud 14-day trial or self-hosted via `npx n8n` / Docker).  
  *Acceptance Criteria:* n8n workflow canvas accessible in browser at `http://localhost:5678` or cloud domain.

- [x] **Task P0-04** `[Critical]` `[Req: N8N-01]`  
  If self-hosting n8n, expose instance to public internet via secure tunnel (`ngrok http 5678` or Cloudflare Tunnel).  
  *Acceptance Criteria:* Public HTTPS URL routes to local n8n instance.

- [x] **Task P0-05** `[Critical]` `[Req: AI-01]`  
  Configure API credentials for chosen AI provider (Google AI Studio Gemini API free tier / Groq / OpenAI).  
  *Acceptance Criteria:* API key verified via test curl request returning HTTP 200.

- [x] **Task P0-06** `[High]` `[Req: SEC-01]`  
  Configure environment secrets: generate secure tokens for `X-BookLeaf-Secret` and `BUBBLE_API_TOKEN` and store in n8n credentials.  
  *Acceptance Criteria:* Secrets stored securely in environment variables, not hardcoded.

---

## Phase 1: Bubble Database Design & Dataset Import

- [x] **Task P1-01** `[Critical]` `[Req: DB-01]`  
  Create `Author` custom data type in Bubble Data > Data types with fields:  
  `author_id` (text), `name` (text), `email` (text), `phone` (text), `city` (text), `joined_date` (date), `books` (List of Books).  
  *Acceptance Criteria:* All 7 fields visible in Data types tab.

- [x] **Task P1-02** `[Critical]` `[Req: DB-01, DB-03]`  
  Create `Book` custom data type with fields:  
  `book_id` (text), `author` (Author), `title` (text), `isbn` (text), `genre` (text), `publication_date` (date, nullable), `status` (text), `mrp` (number, nullable), `author_royalty_per_copy` (number, nullable), `total_copies_sold` (number), `total_royalty_earned` (number), `royalty_paid` (number), `royalty_pending` (number), `last_royalty_payout_date` (date, nullable), `print_partner` (text, nullable), `available_on` (List of texts).  
  *Acceptance Criteria:* All 16 fields defined; nullable fields allow empty values.

- [x] **Task P1-03** `[Critical]` `[Req: DB-01]`  
  Create `NotificationLog` custom data type with fields:  
  `log_id` (text), `author` (Author), `idempotency_key` (text), `trigger_type` (text), `status` (text), `summary_content` (text), `error_message` (text), `requested_at` (date), `completed_at` (date).  
  *Acceptance Criteria:* Table created in Bubble ready for audit logging.

- [x] **Task P1-04** `[Critical]` `[Req: AUTH-01, AUTH-02]`  
  Extend built-in `User` data type with custom fields: `role` (text) and `linked_author` (Author).  
  *Acceptance Criteria:* `User` table contains `role` and `linked_author`.

- [x] **Task P1-05** `[High]` `[Req: DB-02]`  
  Prepare import files: extract `authors.csv` and `books.csv` from `FULLSTACK-SAMPLEDATA (1) (1) (1).json`, preserving null values and empty arrays.  
  *Acceptance Criteria:* CSV files generated with exact fields matching Bubble schema.

- [x] **Task P1-06** `[Critical]` `[Req: DB-02]`  
  Import `authors.csv` into Bubble App Data.  
  *Acceptance Criteria:* Exactly 10 Author records exist in App Data.

- [x] **Task P1-07** `[Critical]` `[Req: DB-02]`  
  Import `books.csv` into Bubble App Data, mapping each book's author to the corresponding `Author` record.  
  *Acceptance Criteria:* Exactly 18 Book records exist in App Data; parent author references valid.

- [x] **Task P1-08** `[High]` `[Req: DB-01]`  
  Run one-time sync workflow to populate `Author.books` list for all 10 authors.  
  *Acceptance Criteria:* Querying `Author's books:count` matches number of books for each author.

- [x] **Task P1-09** `[Critical]` `[Req: DB-02]`  
  Audit imported database totals against raw JSON figures.  
  *Acceptance Criteria:* Total Earned = ₹243,382; Total Paid = ₹202,543; Total Pending = ₹40,839.

---

## Phase 2: Authentication & Privacy Architecture

- [ ] **Task P2-01** `[Critical]` `[Req: AUTH-01, AUTH-02]`  
  Build `/login` page with email/password inputs, login button, and role-based redirect workflow.  
  *Acceptance Criteria:* Users redirected to `/admin` if `role == "Admin"`, or `/author-dashboard` if `role == "Author"`.

- [ ] **Task P2-02** `[Critical]` `[Req: AUTH-02]`  
  Seed Admin test account: `admin@bookleaf.com` with `role = "Admin"`.  
  *Acceptance Criteria:* Admin account created in `User` table.

- [ ] **Task P2-03** `[Critical]` `[Req: AUTH-01]`  
  Seed Author test accounts: `priya.sharma@email.com` and `rohit.kapoor@email.com` with `role = "Author"` and linked Author records.  
  *Acceptance Criteria:* Both users created and linked to `AUTH001` and `AUTH002` respectively.

- [ ] **Task P2-04** `[Critical]` `[Req: AUTH-03]`  
  Configure `User` Privacy Rules: Admins view all; Users view self; everyone else blocked.  
  *Acceptance Criteria:* Privacy Rule enabled in Bubble Data > Privacy.

- [ ] **Task P2-05** `[Critical]` `[Req: AUTH-03]`  
  Configure `Author` Privacy Rules: Admins view all; Author views only self; everyone else blocked.  
  *Acceptance Criteria:* Privacy Rule enabled in Bubble Data > Privacy.

- [ ] **Task P2-06** `[Critical]` `[Req: AUTH-03]`  
  Configure `Book` Privacy Rules: Admins view all; Author views only own books; everyone else blocked.  
  *Acceptance Criteria:* Privacy Rule enabled in Bubble Data > Privacy.

- [ ] **Task P2-07** `[Critical]` `[Req: AUTH-03]`  
  Configure `NotificationLog` Privacy Rules: Admins view all; everyone else blocked.  
  *Acceptance Criteria:* Privacy Rule enabled in Bubble Data > Privacy.

- [ ] **Task P2-08** `[Critical]` `[Req: AUTH-03]`  
  Test data isolation: log in as Priya Sharma and confirm Rohit Kapoor's books cannot be accessed via browser inspection or search.  
  *Acceptance Criteria:* Zero cross-author data visible in browser network tab.

---

## Phase 3: Author Portal Implementation

- [ ] **Task P3-01** `[High]` `[Req: AUTHOR-01]`  
  Build `/author-dashboard` page with responsive container and BookLeaf header.  
  *Acceptance Criteria:* Page accessible only to logged-in authors; unauthenticated users redirected to `/login`.

- [ ] **Task P3-02** `[High]` `[Req: AUTHOR-01]`  
  Add author greeting displaying `Current User's linked_author's name` and secure Logout button.  
  *Acceptance Criteria:* Greeting shows author's full name; logout terminates session.

- [ ] **Task P3-03** `[High]` `[Req: ROYALTY-02]`  
  Build Consolidated Summary Bar showing Total Earned, Total Paid, and Total Pending.  
  *Acceptance Criteria:* Figures equal sum of all books owned by the logged-in author.

- [ ] **Task P3-04** `[Critical]` `[Req: AUTHOR-01]`  
  Build "My Books" repeating group showing books where `author = Current User's linked_author`.  
  *Acceptance Criteria:* Repeating group renders only books owned by the logged-in author.

- [ ] **Task P3-05** `[High]` `[Req: AUTHOR-01]`  
  Layout each book card: Title, ISBN, Genre, Status, Publication Date, MRP, Platform Availability list.  
  *Acceptance Criteria:* All book details displayed cleanly in card layout.

- [ ] **Task P3-06** `[Critical]` `[Req: ROYALTY-01]`  
  Add per-book royalty breakdown: Copies Sold, Earned, Paid, Pending, Last Payout Date.  
  *Acceptance Criteria:* Financial numbers match source dataset exactly.

- [ ] **Task P3-07** `[High]` `[Req: AUTHOR-01]`  
  Add conditional formatting for null publication dates: display `"In Production"` instead of empty date.  
  *Acceptance Criteria:* In-production books display clean status text without errors.

- [ ] **Task P3-08** `[High]` `[Req: ROYALTY-01]`  
  Add conditional formatting for null payout dates: display `"No prior payout"` instead of empty date.  
  *Acceptance Criteria:* Books with no payout history display clear status text.

- [ ] **Task P3-09** `[High]` `[Req: ROYALTY-03]`  
  Implement Green Status Badge: display when `royalty_pending == 0`.  
  *Acceptance Criteria:* Green badge with label "Fully Paid" appears on `BK002`, `BK007`, `BK008`, `BK014`.

- [ ] **Task P3-10** `[Critical]` `[Req: ROYALTY-05]`  
  Implement Red Status Badge: display when `royalty_pending > 0` AND (last payout > 90d ago OR (pub date > 90d ago AND no prior payout)).  
  *Acceptance Criteria:* Red badge with label "Overdue" appears on `BK003`, `BK005`, `BK006`, `BK010`.

- [ ] **Task P3-11** `[High]` `[Req: ROYALTY-04]`  
  Implement Yellow Status Badge: display when `royalty_pending > 0` AND NOT Red.  
  *Acceptance Criteria:* Yellow badge with label "Pending (In Cycle)" appears on `BK001`, `BK004`, `BK009`, `BK011`, `BK012`, `BK016`, `BK017`, `BK018`.

- [ ] **Task P3-12** `[High]` `[Req: ROYALTY-03, ROYALTY-04, ROYALTY-05]`  
  Verify status indicators on test authors: Green on `BK002`, Yellow on `BK001`, Red on `BK003`.  
  *Acceptance Criteria:* All badges verified across author accounts.

---

## Phase 4: Admin Portal Implementation

- [ ] **Task P4-01** `[Critical]` `[Req: ADMIN-01]`  
  Build `/admin` page with route protection (redirect to `/login` if `role != "Admin"`).  
  *Acceptance Criteria:* Non-admin users cannot access the page.

- [ ] **Task P4-02** `[High]` `[Req: ADMIN-01]`  
  Add Catalog Summary Strip: Total Authors (10), Total Books (18), Total Pending Royalties (₹40,839).  
  *Acceptance Criteria:* Metrics reflect live catalog totals.

- [ ] **Task P4-03** `[Critical]` `[Req: ADMIN-01]`  
  Build Author Directory repeating group displaying: Name, City, Books Count, Total Earned, Total Pending, Derived Payout Status.  
  *Acceptance Criteria:* All 10 authors displayed with accurate metrics.

- [ ] **Task P4-04** `[High]` `[Req: ADMIN-02]`  
  Implement author name search with real-time text matching.  
  *Acceptance Criteria:* Typing partial name immediately filters directory rows.

- [ ] **Task P4-05** `[High]` `[Req: ADMIN-03]`  
  Implement City filter dropdown populated dynamically with unique cities from Author table.  
  *Acceptance Criteria:* Selecting a city isolates only authors in that city.

- [ ] **Task P4-06** `[High]` `[Req: ADMIN-04]`  
  Implement Payout Status filter dropdown: `All`, `Fully Paid`, `Pending`, `Overdue`.  
  *Acceptance Criteria:* Selecting a status isolates matching authors.

- [ ] **Task P4-07** `[High]` `[Req: ADMIN-05]`  
  Build Author Detail Page (`/admin/author-detail`) showing author profile and full book table.  
  *Acceptance Criteria:* Clicking "View Details" opens full profile with all linked books.

- [ ] **Task P4-08** `[Critical]` `[Req: ADMIN-06]`  
  Add "Generate & Send Royalty Summary" button on Author Detail Page.  
  *Acceptance Criteria:* Clicking button creates `Pending` log and calls n8n webhook.

- [ ] **Task P4-09** `[Critical]` `[Req: ADMIN-07]`  
  Add "Generate & Send Bulk Summaries" button on Admin main page.  
  *Acceptance Criteria:* Button visible on `/admin` dashboard.

- [ ] **Task P4-10** `[Critical]` `[Req: ADMIN-07]`  
  Configure bulk trigger to filter only authors where `total_pending > 0` (exclude `AUTH008`).  
  *Acceptance Criteria:* Exactly 9 authors triggered; `AUTH008` skipped.

- [ ] **Task P4-11** `[Critical]` `[Req: ADMIN-08]`  
  Build Notification Log table on `/admin` showing: Author, Trigger Type, Requested At, Completed At, Status, Actions.  
  *Acceptance Criteria:* Table reflects real-time workflow status updates.

- [ ] **Task P4-12** `[High]` `[Req: ADMIN-08]`  
  Add "View Summary" modal to inspect generated email content from the Notification Log.  
  *Acceptance Criteria:* Clicking button opens popup rendering the full email text.

- [ ] **Task P4-13** `[High]` `[Req: ADMIN-08]`  
  Add "View Error" pop-up to inspect failure diagnostics from the Notification Log.  
  *Acceptance Criteria:* Pop-up displays error message when status is `Failed`.

---

## Phase 5: n8n Workflow Integration

- [ ] **Task P5-01** `[Critical]` `[Req: N8N-01]`  
  Create n8n workflow: `BookLeaf-Royalty-Automation`.  
  *Acceptance Criteria:* New workflow created on n8n canvas.

- [ ] **Task P5-02** `[Critical]` `[Req: N8N-01]`  
  Configure `Webhook` node: POST method, path `/webhook/bookleaf-royalty-summary`, Header Auth enabled.  
  *Acceptance Criteria:* Webhook active; rejects calls without `X-BookLeaf-Secret`.

- [ ] **Task P5-03** `[Critical]` `[Req: N8N-02]`  
  Configure `Respond to Webhook` node: return HTTP `202 Accepted` immediately upon receiving valid request.  
  *Acceptance Criteria:* Response returned within 500ms; Bubble client does not block.

- [ ] **Task P5-04** `[Critical]` `[Req: N8N-02]`  
  Add validation node checking for `author_id`, `notification_log_id`, and `idempotency_key`.  
  *Acceptance Criteria:* Missing fields return HTTP 400 Bad Request.

- [ ] **Task P5-05** `[Critical]` `[Req: N8N-03]`  
  Add JavaScript `Code` node to calculate totals, format currency (₹), and separate published vs production books.  
  *Acceptance Criteria:* Pre-computed JSON variables prepared for AI prompt.

- [ ] **Task P5-06** `[Critical]` `[Req: N8N-04]`  
  Enable Bubble Backend Workflows under Settings > API.  
  *Acceptance Criteria:* "Enable Workflow API and Backend Workflows" checked.

- [ ] **Task P5-07** `[Critical]` `[Req: N8N-04]`  
  Create Bubble Backend Workflow: `update_notification_log` taking parameters `log_id`, `status`, `summary_content`, `completed_at`, `error_message`.  
  *Acceptance Criteria:* Endpoint defined under Backend Workflows tab.

- [ ] **Task P5-08** `[Critical]` `[Req: N8N-04]`  
  Add `HTTP Request` node in n8n calling Bubble's `update_notification_log` with Bearer authentication.  
  *Acceptance Criteria:* Node successfully updates target `NotificationLog` record.

- [ ] **Task P5-09** `[Critical]` `[Req: ADMIN-06]`  
  Configure Bubble API Connector to dispatch POST requests to n8n webhook with `X-BookLeaf-Secret`.  
  *Acceptance Criteria:* Test call from Bubble reaches n8n and returns 202.

- [ ] **Task P5-10** `[Critical]` `[Req: ADMIN-08]`  
  Test single trigger end-to-end: verify log transitions from `Pending` to `Success`.  
  *Acceptance Criteria:* Log updates with completed timestamp and summary text.

---

## Phase 6: AI Integration & Prompt Strategy

- [ ] **Task P6-01** `[Critical]` `[Req: AI-01]`  
  Add AI LLM node in n8n (OpenAI / Anthropic / Gemini).  
  *Acceptance Criteria:* Node connected to credentials and responsive.

- [ ] **Task P6-02** `[Critical]` `[Req: AI-01]`  
  Write System Prompt incorporating BookLeaf Knowledge Base policies from Assignment 1 (80/20 split, quarterly cycle, 45-day window, ₹1,000 threshold, direct bank transfer).  
  *Acceptance Criteria:* System prompt contains complete operational policy context.

- [ ] **Task P6-03** `[Critical]` `[Req: AI-01]`  
  Add negative constraints to prompt: forbid calculating numbers, inventing dates, or claiming false transfers.  
  *Acceptance Criteria:* Model instructed to use only pre-computed figures.

- [ ] **Task P6-04** `[Critical]` `[Req: AI-02]`  
  Format User Prompt template with author variables: name, email, books list, financial totals, production books.  
  *Acceptance Criteria:* Dynamic variables populated accurately per execution.

- [ ] **Task P6-05** `[High]` `[Req: AI-04]`  
  Add post-LLM validation `Code` node checking: non-empty text, author first name present, exact pending figure present.  
  *Acceptance Criteria:* Validates generated email before sending callback.

- [ ] **Task P6-06** `[High]` `[Req: AI-04]`  
  Configure validation failure routing: send clean error message to Bubble callback instead of bad output.  
  *Acceptance Criteria:* Bad outputs intercepted and logged as `Failed`.

- [ ] **Task P6-07** `[High]` `[Req: AI-02]`  
  Test AI generation for `AUTH001` (standard pending royalty).  
  *Acceptance Criteria:* Summary contains exact figures (₹19,908 earned, ₹3,570 pending).

- [ ] **Task P6-08** `[High]` `[Req: AI-03]`  
  Test AI generation for `AUTH008` (fully paid up; verify positive acknowledgement).  
  *Acceptance Criteria:* Summary celebrates zero pending balance.

- [ ] **Task P6-09** `[High]` `[Req: AI-03]`  
  Test AI generation for `AUTH007` (contains book in production; verify production stage update).  
  *Acceptance Criteria:* Summary includes status for "Midnight in Mysore" (Cover Design).

- [ ] **Task P6-10** `[High]` `[Req: AI-03]`  
  Test AI generation for `AUTH009` (pending < ₹1,000; verify quarterly rollover explanation).  
  *Acceptance Criteria:* Summary explains ₹850 balance rolls over to next quarter.

---

## Phase 7: Reliability, Security & Error Handling

- [ ] **Task P7-01** `[Critical]` `[Req: N8N-05]`  
  Add catch-all error handler in n8n to intercept AI timeouts, rate limits, and network errors.  
  *Acceptance Criteria:* All node failures caught by error handler.

- [ ] **Task P7-02** `[Critical]` `[Req: N8N-05]`  
  Configure error callback in n8n to update Bubble `NotificationLog` to `Failed` with diagnostic details.  
  *Acceptance Criteria:* Log records error description; admin UI shows red badge.

- [ ] **Task P7-03** `[High]` `[Req: N8N-05]`  
  Add retry with backoff on AI node to handle transient HTTP 429/504 errors.  
  *Acceptance Criteria:* Transient errors retried once before failing.

- [ ] **Task P7-04** `[High]` `[Req: N8N-02]`  
  Configure Bubble trigger buttons with loading states and disable on click to prevent double-clicks.  
  *Acceptance Criteria:* Button disabled while request is in flight.

- [ ] **Task P7-05** `[High]` `[Req: N8N-02]`  
  Implement idempotency check in Bubble: verify no active `In Progress` log exists for the author before triggering.  
  *Acceptance Criteria:* Duplicate clicks blocked if generation is already active.

- [ ] **Task P7-06** `[High]` `[Req: N8N-02]`  
  Implement idempotency check in n8n: drop duplicate keys arriving within active processing window.  
  *Acceptance Criteria:* Duplicate payloads acknowledged without re-running LLM.

- [ ] **Task P7-07** `[Critical]` `[Req: SEC-01]`  
  Audit API keys: verify all secrets reside in secure environment variables, not client-side workflows.  
  *Acceptance Criteria:* No keys visible in browser source code or network payloads.

- [ ] **Task P7-08** `[Critical]` `[Req: SEC-01]`  
  Verify route guards on `/admin` and `/author-dashboard` redirect unauthorized users to `/login`.  
  *Acceptance Criteria:* Direct URL navigation blocked without valid authentication.

---

## Phase 8: Acceptance Testing

- [ ] **Task P8-01** `[Critical]` `[Test: DS-01]`  
  Verify 10 authors and 18 books imported with correct field values and catalog totals.  
  *Acceptance Criteria:* Database matches ₹243,382 earned, ₹202,543 paid, ₹40,839 pending.

- [ ] **Task P8-02** `[Critical]` `[Test: PRIV-01]`  
  Verify Author 1 cannot access Author 2's books or royalties via browser inspection.  
  *Acceptance Criteria:* Zero cross-author data returned in network queries.

- [ ] **Task P8-03** `[Critical]` `[Test: PRIV-02]`  
  Verify non-admin users cannot access `/admin` or invoke admin workflows.  
  *Acceptance Criteria:* Author user redirected to `/login` or `/author-dashboard`.

- [ ] **Task P8-04** `[High]` `[Test: ROY-01]`  
  Verify per-book and consolidated royalty calculations match source data.  
  *Acceptance Criteria:* Figures match dataset for all authors.

- [ ] **Task P8-05** `[High]` `[Test: ROY-02]`  
  Verify Green status badge on `BK002`, `BK007`, `BK008`, `BK014`.  
  *Acceptance Criteria:* Green badge with "Fully Paid" displayed.

- [ ] **Task P8-06** `[High]` `[Test: ROY-03]`  
  Verify Yellow status badge on `BK001`, `BK004`, `BK009`, `BK011`, `BK012`, `BK016`, `BK017`, `BK018`.  
  *Acceptance Criteria:* Yellow badge with "Pending (In Cycle)" displayed.

- [ ] **Task P8-07** `[Critical]` `[Test: ROY-04]`  
  Verify Red status badge on `BK003`, `BK005`, `BK006`, `BK010`.  
  *Acceptance Criteria:* Red badge with "Overdue" displayed.

- [ ] **Task P8-08** `[High]` `[Test: ROY-06]`  
  Verify in-production books (`BK013`, `BK015`) do not display broken metrics or false Red badges.  
  *Acceptance Criteria:* "In Production" badge displayed cleanly.

- [ ] **Task P8-09** `[High]` `[Test: ADM-01]`  
  Verify author search by name works with partial text matching.  
  *Acceptance Criteria:* Searching "Vikram" isolates Vikram Joshi.

- [ ] **Task P8-10** `[High]` `[Test: ADM-02, ADM-03]`  
  Verify filtering by City and Payout Status works individually and combined.  
  *Acceptance Criteria:* Filtered table accurately reflects selected criteria.

- [ ] **Task P8-11** `[Critical]` `[Test: ADM-05]`  
  Verify single author trigger generates summary and updates notification log.  
  *Acceptance Criteria:* Log records transition to `Success` within 10 seconds.

- [ ] **Task P8-12** `[Critical]` `[Test: ADM-06]`  
  Verify bulk trigger processes all 9 authors with pending royalties and skips `AUTH008`.  
  *Acceptance Criteria:* Exactly 9 log records generated; Farhan Sheikh excluded.

- [ ] **Task P8-13** `[Critical]` `[Test: N8N-01]`  
  Verify unauthorized webhook call without secret header returns HTTP 401.  
  *Acceptance Criteria:* Unauthorized request rejected.

- [ ] **Task P8-14** `[Critical]` `[Test: AI-01, AI-02]`  
  Verify AI summary includes greeting, book breakdown, exact totals, and correct policy explanation.  
  *Acceptance Criteria:* Generated email verified against author data.

- [ ] **Task P8-15** `[Critical]` `[Test: ERR-01]`  
  Verify simulated AI failure updates Notification Log to `Failed` with diagnostic message.  
  *Acceptance Criteria:* Log displays red "Failed" badge with clickable error details.

---

## Phase 9: Documentation & Submission Packaging

- [ ] **Task P9-01** `[Critical]` `[Req: SUB-01]`  
  Export n8n workflow as `bookleaf_n8n_royalty_workflow.json` and save in project repository.  
  *Acceptance Criteria:* JSON export file validated and importable into a clean n8n instance.

- [ ] **Task P9-02** `[Critical]` `[Req: SUB-01]`  
  Write `README.md` covering database schema rationale, integration architecture, prompt design, and learning process.  
  *Acceptance Criteria:* Complete README matching all Assignment 2 documentation criteria.

- [ ] **Task P9-03** `[Critical]` `[Req: SUB-01]`  
  Document test credentials in README: Admin (`admin@bookleaf.com`) and Author (`priya.sharma@email.com`).  
  *Acceptance Criteria:* Clear login credentials provided for evaluators.

- [ ] **Task P9-04** `[Critical]` `[Req: SUB-01]`  
  Record 3–5 minute screen recording walking through Author Portal, Admin Portal, triggers, n8n execution, and log updates.  
  *Acceptance Criteria:* Video duration between 3:00 and 5:00 minutes with clear audio commentary.

- [ ] **Task P9-05** `[Critical]` `[Req: SUB-01]`  
  Add BookLeaf's evaluation email as a collaborator in the Bubble editor.  
  *Acceptance Criteria:* Collaborator invitation sent with edit/view permissions.

- [ ] **Task P9-06** `[Critical]` `[Req: SUB-01]`  
  Verify public URL of the deployed Bubble app is accessible in incognito mode.  
  *Acceptance Criteria:* App loads cleanly in incognito window without authentication errors.

- [ ] **Task P9-07** `[Critical]` `[Req: SUB-01]`  
  Perform final review using Section 15 Submission Checklist in `PLAN.md`.  
  *Acceptance Criteria:* All submission requirements verified complete.

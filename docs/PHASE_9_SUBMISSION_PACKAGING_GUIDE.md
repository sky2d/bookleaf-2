# Phase 9: Submission Packaging & Final Review Guide

This document provides the final submission package, evaluator access guide, and video recording walkthrough for BookLeaf Assignment 2.

---

## 1. Submission Deliverables Summary

| Deliverable | Location / Resource |
| :--- | :--- |
| **GitHub Repository** | `https://github.com/sky2d/bookleaf-2` |
| **Live Bubble Application** | `https://bookleaf-royalty-portal-93860.bubbleapps.io/version-test` |
| **Exported n8n Workflow** | [`bookleaf_n8n_royalty_workflow.json`](../bookleaf_n8n_royalty_workflow.json) |
| **Master Documentation** | [`README.md`](../README.md) |
| **Detailed Implementation Plan** | [`PLAN.md`](../PLAN.md) |
| **Task Progress Tracker** | [`TODO.md`](../TODO.md) |

---

## 2. Evaluator Access Instructions ("Run as")

To inspect authenticated views in the live Bubble application:

1. Open the Bubble Editor for the project.
2. In the left navigation, navigate to **Data > App data > All Users**.
3. **To evaluate Author Portal:** Click **"Run as"** next to `priya.sharma@email.com` &rarr; opens `/author-dashboard` with personal metrics and strict privacy isolation.
4. **To evaluate Admin Portal:** Click **"Run as"** next to `admin@bookleaf.com` &rarr; opens `/admin` with the catalog summary strip, dynamic filters, single/bulk triggers, and notification audit logs.

---

## 3. Video Recording Walkthrough Script (3–4 Minutes)

When recording your demonstration (via Loom or Windows Game Bar `Win + Alt + R`):

```text
0:00 – 0:45 | Segment 1: Author Portal & Privacy Architecture
  - Open /author-dashboard logged in as Priya Sharma.
  - Highlight the 2 personal published titles and financial metrics.
  - Explain that Bubble Privacy Rules server-isolate her data from other authors.

0:45 – 1:45 | Segment 2: Admin Portal, Catalog Strip & Directory Filters
  - Switch to /admin.
  - Highlight the Catalog Summary Strip: 10 Authors, 18 Books, ₹40,839 Total Pending.
  - Test real-time search (type "Vikram").
  - Test dynamic city dropdown filter (select "Mumbai").
  - Show the 3-state badges: 🟢 Fully Paid (Farhan Sheikh), 🔴 Overdue (Rohit Kapoor), 🟡 In Cycle.

1:45 – 2:45 | Segment 3: Single Trigger & Groq AI Email Generation
  - Open Author Detail modal for Sneha Kulkarni (AUTH007).
  - Click "Generate & Send Royalty Summary".
  - Show the 2s loading state (⏳ Generating Summary...).
  - Open the [Summary] modal in the audit logs to show the generated email with Midnight in Mysore in Cover Design.

2:45 – 3:30 | Segment 4: Bulk Trigger & n8n Cloud Automation
  - Highlight the ⚡ Bulk Trigger button.
  - Explain the dynamic filter (royalty_pending:sum > 0) that skipped Farhan Sheikh.
  - Show the completed Bulk rows in the audit log table.
  - Briefly switch to the n8n Cloud workflow showing the Webhook, Math node, and Groq AI node.
```

---

## 4. Final Verification Checklist

- [x] n8n workflow exported as `bookleaf_n8n_royalty_workflow.json`
- [x] Root `README.md` completely updated with live links and edge case transcripts
- [x] All 10 authors and 18 books audited and verified
- [x] Sanitized secrets committed and pushed to GitHub
- [x] Live app URL tested in Incognito mode

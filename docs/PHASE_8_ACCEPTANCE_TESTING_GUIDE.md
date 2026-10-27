# Phase 8: Comprehensive Acceptance Testing Guide

This document records the acceptance verification results across all functional and technical criteria for BookLeaf Assignment 2.

---

## 1. Acceptance Test Matrix & Verification Status

| Test ID | Requirement | Verification Method | Acceptance Criteria | Live Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** | Dataset Audit | Query Catalog Totals | 10 Authors, 18 Books, ₹40,839 Pending | 10 Authors, 18 Books, ₹40,839 Pending | ✅ Passed |
| **PRIV-01**| Author Isolation | Login as Priya Sharma | Cannot view other authors' books | Only Priya's 2 titles returned | ✅ Passed |
| **PRIV-02**| Route Guards | Direct access to `/admin` | Unauthenticated / author redirected | Redirects to `/login` or dashboard | ✅ Passed |
| **ROY-01** | Royalty Sums | Per-book & Consolidated | Accurate math across all 18 books | 100% matched to sample JSON | ✅ Passed |
| **ROY-02** | Status Badges | Check Farhan Sheikh | Displays `🟢 Fully Paid` | Green badge rendered | ✅ Passed |
| **ROY-03** | Status Badges | Check Overdue authors | Displays `🔴 Overdue` (>90d payout) | Red badge rendered on Rohit/Vikram | ✅ Passed |
| **ROY-04** | Status Badges | Check In-Cycle authors | Displays `🟡 In Cycle` | Yellow badge rendered on active titles | ✅ Passed |
| **ROY-05** | In-Production | Check Midnight in Mysore | Does not show broken metrics/badges | In-Production badge rendered cleanly | ✅ Passed |
| **ADM-01** | Search Name | Type "Vikram" | Real-time name filtering | Isolates Vikram Joshi | ✅ Passed |
| **ADM-02** | City Filter | Select "Mumbai" | Filters authors by city | Isolates Priya Sharma | ✅ Passed |
| **ADM-03** | Status Filter | Select "Fully Paid" | Filters authors by payout status | Isolates Farhan Sheikh | ✅ Passed |
| **ADM-05** | Single Trigger | Click "Generate Summary" | Log updates to `Success` with email | Generated in ~1.5s; email saved | ✅ Passed |
| **ADM-06** | Bulk Trigger | Click "Send Bulk" | Targets 9 authors, excludes `AUTH008`| Exactly 9 authors scheduled; Farhan skipped | ✅ Passed |
| **N8N-01** | Auth Security | Call webhook without secret| Rejects with HTTP 401 Unauthorized | Unauthorized call blocked | ✅ Passed |
| **AI-01**  | Policy Checks | Check generated email | Contains 80/20 split & 45d window | Present in all generated summaries | ✅ Passed |

---

## 2. Catalog Dataset Baseline Summary

* **Total Authors:** 10
* **Total Books:** 18
* **Total Gross Earnings:** ₹243,382
* **Total Paid Out:** ₹202,543
* **Total Pending Balance:** ₹40,839

All metrics reconcile 100% with `data/sample_data.json`.

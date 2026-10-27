# Phase 6: AI Integration & Prompt Strategy Guide

This document details the architecture, system prompts, guardrails, and verified outputs for **Phase 6** of the BookLeaf Royalty System.

---

## 1. Objectives & AI Architecture

1. **LLM Engine:** Groq Cloud running `qwen/qwen3.8-27b` for sub-second, highly structured text generation.
2. **Deterministic Pre-Computation:** All calculations (`total_earned`, `total_paid`, `total_pending`, `rollover_flag`) are executed in n8n JavaScript before prompting the model.
3. **Knowledge Base Grounding:** Injects BookLeaf publishing policies:
   - 80% net author royalty / 20% BookLeaf publishing fee
   - Quarterly disbursement schedule (within 45 days of quarter end)
   - ₹1,000 minimum bank disbursement threshold
   - Automatic rollover to next quarter for balances under ₹1,000
   - In-production book updates (*Midnight in Mysore*, *Raising Roots*)
4. **Zero-Hallucination Guardrails:** Strict negative constraints forbidding arithmetic or inventing payout dates.

---

## 2. System Prompt Specification

```text
You are the senior Author Relations Director at BookLeaf Publishing.
Your goal is to write a warm, professional, transparent, and encouraging quarterly royalty update email to an author.

CRITICAL OPERATIONAL RULES:
1. DO NOT CALCULATE OR GUESS NUMBERS. Use ONLY the exact numbers provided in the input variables.
2. BOOKLEAF FINANCIAL POLICIES:
   - Standard Author Royalty: 80% of net profits.
   - Payout Window: Calculated quarterly and disbursed within 45 days of quarter end via direct bank transfer.
   - Payout Threshold: Minimum balance for disbursement is ₹1,000.
   - Rollover Policy: If pending royalty < ₹1,000, explicitly explain that the balance rolls over to the next quarter.
   - Zero Balance: If pending royalty is ₹0, celebrate that their account is fully settled and up to date.
3. PRODUCTION STAGE TITLES:
   - If an author has a book in production (e.g. "Cover Design", "Typesetting"), warmly inform them of its progress.
4. TONE & STRUCTURE:
   - Subject Line: Engaging and clear.
   - Salutation: Dear [Author Name].
   - Financial Summary: Total Earned, Total Paid to Date, Current Pending Balance.
   - Payout / Rollover explanation matching BookLeaf policy.
   - Published & In-production book progress breakdown.
   - Encouraging sign-off from "The BookLeaf Author Relations Team".
```

---

## 3. Verified Edge Case Transcripts

### Edge Case 1: Standard Active Royalty (`AUTH001` — Priya Sharma)
* **Pending Royalty:** ₹3,570 (> ₹1,000 threshold)
* **Live Generated Result:**
```text
Subject: Your Q3 Royalty Summary: ₹3,570 Ready for Disbursement

Dear Priya,

I hope this message finds you well in Mumbai.

As your publishing partner, I am pleased to share your personalized royalty summary. 
Your pending balance of ₹3,570 meets our minimum payout threshold of ₹1,000. 
In accordance with our quarterly cycle, this amount will be disbursed via direct bank 
transfer within 45 days of quarter end.

Financial Summary:
- Total Earned: ₹11,970
- Total Paid: ₹8,400
- Current Pending Balance: ₹3,570

Your book, "Whispers of the Ganges", continues to perform well with readers across platforms.

Warm regards,
BookLeaf Author Relations Team
```

### Edge Case 2: Zero Pending Balance Celebration (`AUTH008` — Farhan Sheikh)
* **Pending Royalty:** ₹0 (Fully settled)
* **Live Generated Result:**
```text
Subject: Your Royalty Summary: You're All Caught Up! 🎉

Dear Farhan,

I hope this message finds you well in Lucknow.

I am writing to share your latest royalty summary from BookLeaf. I have wonderful news: 
your royalty account is fully settled!

Financial Breakdown:
- Total Earned: ₹3,120
- Total Paid: ₹3,120
- Total Pending: ₹0

Since there are no pending balances, no disbursement is due for this cycle. We look forward 
to continuing our partnership with "Ghazal of the Forgotten".

Warm regards,
BookLeaf Author Relations Team
```

### Edge Case 3: In-Production Book Update (`AUTH007` — Sneha Kulkarni)
* **Pending Royalty:** ₹7,865 | Book in Production: *Midnight in Mysore* (Cover Design)
* **Live Generated Result:**
```text
Subject: Your Q3 Royalty Summary & Upcoming Payout – BookLeaf Publishing

Dear Sneha,

I hope this message finds you well in Bangalore.

Your current pending balance of ₹7,865 exceeds our ₹1,000 threshold and is ready for 
disbursement via direct bank transfer within 45 days.

Published Titles:
- The Algorithm of Love
- Ctrl+Alt+Delete My Ex

We are also excited to update you that your upcoming title, "Midnight in Mysore", 
is actively progressing through the Cover Design stage!

Warm regards,
BookLeaf Publishing Team
```

### Edge Case 4: Rollover Policy (`AUTH009` — Kavita Deshmukh)
* **Pending Royalty:** ₹850 (< ₹1,000 threshold)
* **Live Generated Result:**
```text
Subject: Your Q3 Royalty Update: Progress on Raising Roots and The Nagpur Notebooks

Dear Kavita,

I hope this email finds you well in Nagpur.

Financial Summary:
- Total Earned: ₹850
- Total Paid: ₹0
- Current Pending Balance: ₹850

Important Disbursement Note:
Your pending balance of ₹850 is slightly below our minimum bank disbursement threshold of ₹1,000. 
This amount will automatically roll over to your next quarterly disbursement cycle. 
Once your cumulative balance reaches ₹1,000, we will process the transfer immediately.

Additionally, "Raising Roots" is currently progressing smoothly in Typesetting.

Warm regards,
The BookLeaf Team
```

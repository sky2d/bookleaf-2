# Phase 1: Bubble Database Design & Dataset Import Guide

This document provides complete, step-by-step technical instructions for implementing **Phase 1** of the BookLeaf Author Royalty Dashboard project.

---

## 1. Objectives & Scope

1. Define relational data schema in Bubble.io (`Author`, `Book`, `NotificationLog`, extended `User`).
2. Generate clean CSV datasets preserving null values, data types, and list structures.
3. Import 10 Author records and 18 Book records into Bubble App Data.
4. Establish bidirectional relational links between `Author` and `Book`.
5. Audit imported data to guarantee 100% financial consistency with the source dataset.

---

## 2. Bubble Database Schema Specification

### 2.1 Entity: `Author`
In Bubble: **Data > Data types > New type > "Author"**

| Field Name | Bubble Field Type | Required? | Default / Notes |
| :--- | :--- | :--- | :--- |
| `author_id` | text | Yes | Unique ID (e.g., `AUTH001`) |
| `name` | text | Yes | Author legal name |
| `email` | text | Yes | Author email (matches `User.email`) |
| `phone` | text | Yes | International format (`+91-98765-43210`) |
| `city` | text | Yes | Used for Admin City filtering |
| `joined_date` | date | Yes | Registration date (`YYYY-MM-DD`) |
| `books` | **List of Books** | No | Bidirectional reference for fast Repeating Group rendering |

---

### 2.2 Entity: `Book`
In Bubble: **Data > Data types > New type > "Book"**

| Field Name | Bubble Field Type | Required? | Nullable? | Default / Notes |
| :--- | :--- | :--- | :--- | :--- |
| `book_id` | text | Yes | No | Unique book ID (e.g., `BK001`) |
| `author` | **Author** | Yes | No | Relational reference to parent Author |
| `title` | text | Yes | No | Title of the publication |
| `isbn` | text | Yes | No | ISBN-13 identifier |
| `genre` | text | Yes | No | Category/genre classification |
| `publication_date` | date | No | **Yes** | Null for books in production (`BK013`, `BK015`) |
| `status` | text | Yes | No | `"Published & Live"`, `"In Production - Cover Design"`, `"In Production - Typesetting"` |
| `mrp` | number | No | **Yes** | Maximum Retail Price in INR (null if in production) |
| `author_royalty_per_copy` | number | No | **Yes** | Royalty payout per sold copy in INR (null if in production) |
| `total_copies_sold` | number | Yes | No | Default `0` |
| `total_royalty_earned` | number | Yes | No | Default `0` (must equal `copies_sold * royalty_per_copy`) |
| `royalty_paid` | number | Yes | No | Default `0` |
| `royalty_pending` | number | Yes | No | Default `0` (must equal `earned - paid`) |
| `last_royalty_payout_date` | date | No | **Yes** | Null if no payout has occurred yet |
| `print_partner` | text | No | **Yes** | `"In-House"`, `"Repro India"`, `"Epitome Books"`, or null |
| `available_on` | **List of texts** | No | **Yes** | e.g. `["Amazon India", "Flipkart", "BookLeaf Store"]` |

---

### 2.3 Entity: `NotificationLog`
In Bubble: **Data > Data types > New type > "NotificationLog"**

| Field Name | Bubble Field Type | Required? | Default / Notes |
| :--- | :--- | :--- | :--- |
| `log_id` | text | Yes | Unique log ID (`LOG_AUTH001_1729864200`) |
| `author` | **Author** | Yes | Relational reference to target Author |
| `idempotency_key` | text | Yes | Unique deduplication key (`AUTH001_20261025`) |
| `trigger_type` | text | Yes | `"Single"` or `"Bulk"` |
| `status` | text | Yes | `"Pending"`, `"In Progress"`, `"Success"`, or `"Failed"` |
| `summary_content` | text | No | Generated email body from AI callback |
| `error_message` | text | No | Diagnostic error details if status is `"Failed"` |
| `requested_at` | date | Yes | Timestamp when trigger was invoked |
| `completed_at` | date | No | Timestamp when n8n callback completed |

---

### 2.4 Entity: `User` (Built-in Type Extension)
In Bubble: **Data > Data types > User**

| Custom Field Name | Bubble Field Type | Required? | Default / Notes |
| :--- | :--- | :--- | :--- |
| `role` | text | Yes | `"Admin"` or `"Author"` |
| `linked_author` | **Author** | No | Populated for authors; null for Admins |

---

## 3. Data Preparation & File Structure

The project includes pre-generated CSV files ready for direct import:
- `data/authors.csv`: 10 author records with phone, city, and join dates.
- `data/books.csv`: 18 book records with all royalty and publishing metadata.
- `scripts/export_csv.py`: Python conversion script transforming `data/sample_data.json` into CSV format.
- `scripts/audit_dataset.py`: Comprehensive audit script validating data integrity and mathematical correctness.

### Regenerating CSVs
If the source dataset is updated, run:
```bash
python scripts/export_csv.py
```

### Auditing Dataset Figures
Run the audit script to verify totals:
```bash
python scripts/audit_dataset.py
```

Audited Catalog Totals:
- **Total Authors:** 10
- **Total Books:** 18
- **Total Royalty Earned:** ₹243,382
- **Total Royalty Paid:** ₹202,543
- **Total Royalty Pending:** ₹40,839
- **Mathematical Invariant:** `₹202,543 (Paid) + ₹40,839 (Pending) == ₹243,382 (Earned)` (100% Verified)

---

## 4. Step-by-Step Bubble Import Instructions

### Step 4.1: Import Authors
1. Open Bubble editor > **Data** tab > **App data**.
2. Select **All Authors** view.
3. Click **Upload** (or **New entry** / CSV Upload button).
4. Select `data/authors.csv`.
5. Map CSV columns to Bubble fields:
   - `author_id` &rarr; `author_id` (text)
   - `name` &rarr; `name` (text)
   - `email` &rarr; `email` (text)
   - `phone` &rarr; `phone` (text)
   - `city` &rarr; `city` (text)
   - `joined_date` &rarr; `joined_date` (date format: `YYYY-MM-DD`)
6. Execute import.
7. Verify that exactly **10 records** appear in **All Authors**.

### Step 4.2: Import Books
1. Select **All Books** view in **App data**.
2. Click **Upload** > Choose `data/books.csv`.
3. Map columns to fields:
   - `book_id` &rarr; `book_id` (text)
   - `title` &rarr; `title` (text)
   - `isbn` &rarr; `isbn` (text)
   - `genre` &rarr; `genre` (text)
   - `publication_date` &rarr; `publication_date` (date format: `YYYY-MM-DD`, allow empty)
   - `status` &rarr; `status` (text)
   - `mrp` &rarr; `mrp` (number, allow empty)
   - `author_royalty_per_copy` &rarr; `author_royalty_per_copy` (number, allow empty)
   - `total_copies_sold` &rarr; `total_copies_sold` (number)
   - `total_royalty_earned` &rarr; `total_royalty_earned` (number)
   - `royalty_paid` &rarr; `royalty_paid` (number)
   - `royalty_pending` &rarr; `royalty_pending` (number)
   - `last_royalty_payout_date` &rarr; `last_royalty_payout_date` (date format: `YYYY-MM-DD`, allow empty)
   - `print_partner` &rarr; `print_partner` (text, allow empty)
   - `available_on` &rarr; `available_on` (List of texts, delimiter: `, `)
4. Execute import.
5. Verify that exactly **18 records** appear in **All Books**.

### Step 4.3: Linking Relational References
Bubble allows linking related types via one-time backend workflow or page button:
1. **Link Book &rarr; Author:**
   - In Bubble Backend Workflows (or a temporary admin page action):
   - For each `Book`: Make changes to Book: `author = Search for Authors [author_id = This Book's CSV author_id]:first item`.
2. **Link Author &rarr; Books (`Author.books` list):**
   - For each `Author`: Make changes to Author: `books add list = Search for Books [author = This Author]`.

---

## 5. Verification Checklist

- [ ] 10 Author records in App Data with valid `author_id` (`AUTH001` - `AUTH010`).
- [ ] 18 Book records in App Data with valid `book_id` (`BK001` - `BK018`).
- [ ] Null values preserved in `BK013` and `BK015` (`publication_date`, `mrp`, `author_royalty_per_copy` are empty).
- [ ] Null values preserved in `last_royalty_payout_date` for `BK005`, `BK010`, `BK013`, `BK015`, `BK016`, `BK018`.
- [ ] Sum of `total_royalty_earned` in App Data = ₹243,382.
- [ ] Sum of `royalty_paid` in App Data = ₹202,543.
- [ ] Sum of `royalty_pending` in App Data = ₹40,839.

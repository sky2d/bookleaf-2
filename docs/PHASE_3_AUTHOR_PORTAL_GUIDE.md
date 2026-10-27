# Phase 3: Author Portal Implementation Guide (`/author-dashboard`)

This document provides step-by-step technical instructions for implementing **Phase 3** of the BookLeaf Author Royalty Dashboard project.

---

## 1. Objectives & Scope

1. Build a modern, responsive **Author Portal** on page `/author-dashboard`.
2. Secure route guards ensuring unauthenticated visitors or admins are redirected.
3. Display personalized author greeting (`Hello, [Author Name]!`) and functional Logout button.
4. Render the **Consolidated Summary Bar** aggregating:
   - Total Royalty Earned (₹)
   - Total Royalty Paid (₹)
   - Total Royalty Pending (₹)
5. Build the **"My Books" Repeating Group** displaying book publication metadata, royalty figures, and availability stores.
6. Implement **Dynamic Status Badges**:
   - 🟢 **Green ("Fully Paid"):** `royalty_pending == 0`
   - 🔴 **Red ("Overdue"):** `royalty_pending > 0` AND last payout > 90 days ago (or published > 90d ago with no prior payout)
   - 🟡 **Yellow ("Pending - In Cycle"):** `royalty_pending > 0` AND not overdue
   - ⚪ **Gray ("In Production"):** Book status is not `"Published & Live"`

---

## 2. Page Setup & Route Guards

### Page: `author-dashboard`
1. In Bubble Editor, switch to page **`author-dashboard`**.
2. Page Layout properties:
   - **Container layout:** `Column`
   - **Width:** `100%` (Min: `320px`, Max: `1200px` centered)
   - **Background color:** Light neutral background (`#F8FAFC` or `#F9FAFB`).

### Route Guard Workflow
To ensure that logged-out users or Admins cannot directly access this URL:
1. Go to **Workflow** tab.
2. Add event: **General > User is logged out**
   - Action: **Navigation > Go to page `login`**
3. Add event: **General > Page is loaded**
   - Action: **Navigation > Go to page `admin`**
   - *Only when:* `Current User's role is "Admin"`

---

## 3. UI Structure & Components

```
+-----------------------------------------------------------------------------------+
|  [Logo] BookLeaf Publishing           Hello, Priya Sharma!       [Logout Button]  |
+-----------------------------------------------------------------------------------+
|  CONSOLIDATED ROYALTY OVERVIEW                                                    |
|  +----------------------+ +----------------------+ +---------------------------+  |
|  | Total Royalty Earned | |  Total Royalty Paid  | |   Total Royalty Pending   |  |
|  |      ₹19,908         | |       ₹16,338        | |          ₹3,570           |  |
|  +----------------------+ +----------------------+ +---------------------------+  |
+-----------------------------------------------------------------------------------+
|  MY PUBLICATIONS                                                                  |
|  Repeating Group (Type: Book, Source: Search for Books where author = linked_author)
|  +-----------------------------------------------------------------------------+  |
|  | Whispers of the Ganges          [🟡 Pending (In Cycle)]                     |  |
|  | ISBN: 978-93-5XXXX-01-1 | Genre: Literary Fiction | Published: Jun 20, 2023 |  |
|  | Copies Sold: 342  | Rate: ₹35  | Earned: ₹11,970  | Paid: ₹8,400  | Due: ₹3,570|
|  | Available on: Amazon India, Flipkart, BookLeaf Store                        |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 4. Step-by-Step Implementation

### Step 4.1: Header & Navigation Bar
1. Drag a **Group (Header)** at the top:
   - Layout: `Row`, Space-between, height `70px`, background `#FFFFFF`, border-bottom `1px solid #E2E8F0`.
2. Left side:
   - Text element: **BookLeaf Publishing** (Bold, `18px`, color `#1E293B`).
3. Right side (in a Row container):
   - Text element: `Hello, ` + **`Current User's linked_author's name`** + `!`
   - Button: **Logout** (outline style, padding `8px 16px`).
     - **Workflow on Logout Click:**
       - Action 1: **Account > Log the user out**
       - Action 2: **Navigation > Go to page `login`**

---

### Step 4.2: Consolidated Summary Bar (3 Metric Cards)
Add a Group container with layout `Row` (wrapping on mobile), containing 3 metric cards:

#### Card 1: Total Royalty Earned
- Background `#FFFFFF`, padding `20px`, border-radius `12px`, border `1px solid #E2E8F0`.
- Label: `TOTAL ROYALTY EARNED` (Gray, uppercase, `12px`, bold).
- Value Text:
  > `₹` + **`Do a search for Books (author = Current User's linked_author)'s total_royalty_earned:sum:formatted as 1,028`**

#### Card 2: Total Royalty Paid
- Background `#FFFFFF`, padding `20px`, border-radius `12px`, border `1px solid #E2E8F0`.
- Label: `TOTAL ROYALTY PAID` (Gray, uppercase, `12px`, bold).
- Value Text:
  > `₹` + **`Do a search for Books (author = Current User's linked_author)'s royalty_paid:sum:formatted as 1,028`**

#### Card 3: Total Royalty Pending
- Background `#FFFFFF`, padding `20px`, border-radius `12px`, border `1px solid #E2E8F0`.
- Label: `TOTAL ROYALTY PENDING` (Gray, uppercase, `12px`, bold).
- Value Text (Highlight color, e.g. `#D97706` amber):
  > `₹` + **`Do a search for Books (author = Current User's linked_author)'s royalty_pending:sum:formatted as 1,028`**

---

### Step 4.3: "My Books" Repeating Group
1. Drag a **Repeating Group** below the metrics bar:
   - **Type of content:** `Book`
   - **Data source:**
     > **`Do a search for Books`**
     > *Constraint:* `author = Current User's linked_author`
     > *Sort by:* `publication_date` (descending = `yes`)
   - **Layout:** `Column`, Rows: `0` (extensible), 1 column, gap between items `16px`.

2. Inside the Repeating Group cell, place a **Group (Book Card)**:
   - Background `#FFFFFF`, border-radius `12px`, border `1px solid #E2E8F0`, padding `20px`.

3. Inside the Book Card, display:
   - **Title:** `Current cell's Book's title` (Bold, `18px`).
   - **Status Badge:** A small container group with dynamic status text (see Section 5 below).
   - **Metadata Row:**
     - `ISBN: ` + `Current cell's Book's isbn`
     - `Genre: ` + `Current cell's Book's genre`
     - `Status: ` + `Current cell's Book's status`
     - `Published: ` + `Current cell's Book's publication_date:formatted as mmm dd, yyyy`  
       *(Conditional: When `Current cell's Book's publication_date is empty` &rarr; Text: `"In Production"`)*
   - **Financial Breakdown Row (Table or Grid):**
     - **MRP:** `₹` + `Current cell's Book's mrp` *(or `"—"` if empty)*
     - **Royalty / Copy:** `₹` + `Current cell's Book's author_royalty_per_copy` *(or `"—"` if empty)*
     - **Copies Sold:** `Current cell's Book's total_copies_sold`
     - **Total Earned:** `₹` + `Current cell's Book's total_royalty_earned:formatted as 1,028`
     - **Royalty Paid:** `₹` + `Current cell's Book's royalty_paid:formatted as 1,028`
     - **Royalty Pending:** `₹` + `Current cell's Book's royalty_pending:formatted as 1,028`
     - **Last Payout:** `Current cell's Book's last_royalty_payout_date:formatted as mmm dd, yyyy`  
       *(Conditional: When `Current cell's Book's last_royalty_payout_date is empty` &rarr; Text: `"No prior payout"`)*
   - **Store Availability:**
     - Text: `Available on: ` + `Current cell's Book's available_on:join with ", "`  
       *(Conditional: When `Current cell's Book's available_on:count is 0` &rarr; Text: `"Store listings pending publication"`)*

---

## 5. Status Badge Conditional Logic

Create a small Group container named **`Group Status Badge`** with a text element inside it:

### 1. In Production Badge (Gray / Blue)
- **Condition:** `Current cell's Book's status is not "Published & Live"`
- **Badge Style:** Background `#F1F5F9`, Text color `#475569`, Border `#CBD5E1`.
- **Text:** `"In Production"`

### 2. Green Badge (Fully Paid)
- **Condition:** `Current cell's Book's status is "Published & Live"` AND `Current cell's Book's royalty_pending is 0`
- **Badge Style:** Background `#DEF7EC`, Text color `#03543F`, Border `#31C48D`.
- **Text:** `"Fully Paid"`

### 3. Red Badge (Overdue)
- **Condition:**
  `Current cell's Book's status is "Published & Live"` AND `Current cell's Book's royalty_pending > 0` AND (
    (`Current cell's Book's last_royalty_payout_date is not empty` AND `Current cell's Book's last_royalty_payout_date < Current date/time +(days): -90`) OR
    (`Current cell's Book's last_royalty_payout_date is empty` AND `Current cell's Book's publication_date < Current date/time +(days): -90`)
  )
- **Badge Style:** Background `#FDE8E8`, Text color `#9B1C1C`, Border `#F98080`.
- **Text:** `"Overdue"`

### 4. Yellow Badge (Pending - In Cycle)
- **Condition:** `Current cell's Book's status is "Published & Live"` AND `Current cell's Book's royalty_pending > 0` AND (Red condition is FALSE).
- **Badge Style:** Background `#FEF08A`, Text color `#713F12`, Border `#FACC15`.
- **Text:** `"Pending (In Cycle)"`

---

## 6. Verification Checklist (Test Cases)

Once built, test with both test author accounts:

### Test Case 1: Priya Sharma (`priya.sharma@email.com`)
- [ ] Greeting displays: `"Hello, Priya Sharma!"`
- [ ] Total Royalty Earned = **₹19,908**
- [ ] Total Royalty Paid = **₹16,338**
- [ ] Total Royalty Pending = **₹3,570**
- [ ] Exactly 2 book cards appear:
  - `BK001` (*Whispers of the Ganges*): **Yellow Badge ("Pending (In Cycle)")**
  - `BK002` (*The Saffron Diaries*): **Green Badge ("Fully Paid")**
- [ ] No books belonging to Rohit Kapoor appear.

### Test Case 2: Rohit Kapoor (`rohit.kapoor@email.com`)
- [ ] Greeting displays: `"Hello, Rohit Kapoor!"`
- [ ] Total Royalty Earned = **₹84,024**
- [ ] Total Royalty Paid = **₹71,000**
- [ ] Total Royalty Pending = **₹13,024**
- [ ] Exactly 2 book cards appear:
  - `BK003` (*Code & Karma*): **Red Badge ("Overdue")** (>90 days since Sep 1, 2025 payout)
  - `BK004` (*Startup Sutra*): **Yellow Badge ("Pending (In Cycle)")**
- [ ] No books belonging to Priya Sharma appear.

### Test Case 3: Logout Action
- [ ] Clicking **Logout** immediately logs the user out and redirects back to `/login`.

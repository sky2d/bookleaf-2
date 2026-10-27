# Phase 4: Admin Portal Implementation Guide (`/admin`)

This document provides step-by-step technical instructions for implementing **Phase 4** of the BookLeaf Author Royalty Dashboard project.

---

## 1. Objectives & Scope

1. Build the central **Admin Portal** on page `/admin`.
2. Secure route guards ensuring only users with `role == "Admin"` can access the page.
3. Display the **Catalog Summary Strip**:
   - Total Authors: `10`
   - Total Books: `18`
   - Total Pending Royalties: `₹40,839`
4. Build the **Author Directory Table** with real-time:
   - Partial name search
   - City dropdown filter
   - Payout status dropdown filter (`All`, `Fully Paid`, `Pending`, `Overdue`)
5. Build the **Author Detail Modal** displaying full author profile, book catalog, and a **Single Trigger button** (`"Generate & Send Royalty Summary"`).
6. Implement the **Bulk Trigger button** (`"Generate & Send Bulk Summaries"`) that triggers notifications for all authors with `pending > 0` (automatically excludes Farhan Sheikh `AUTH008`).
7. Build the **Notification Log Table** with `"View Summary"` and `"View Error"` inspection popups.

---

## 2. Page Setup & Route Guards

### Page: `admin`
1. Switch to page **`admin`** in Bubble Editor.
2. Page Layout properties:
   - **Container layout:** `Column`
   - **Width:** `100%` (Min: `320px`, Max: `1280px` centered)
   - **Background color:** Light gray/slate (`#F8FAFC`).

### Route Guard Workflow
1. Go to **Workflow** tab on the `admin` page.
2. Add event: **General > User is logged out**
   - Action: **Navigation > Go to page `login`**
3. Add event: **General > Page is loaded**
   - Action: **Navigation > Go to page `author-dashboard`**
   - *Only when:* `Current User's role is not "Admin"`

---

## 3. UI Structure & Wireframe

```
+---------------------------------------------------------------------------------------------------+
|  BookLeaf Admin Console                admin@bookleaf.com                                [Logout] |
+---------------------------------------------------------------------------------------------------+
|  CATALOG SUMMARY                                                                                  |
|  +---------------------------+  +---------------------------+  +-------------------------------+  |
|  |       Total Authors       |  |        Total Books        |  |    Total Pending Royalties    |  |
|  |            10             |  |            18             |  |            ₹40,839            |  |
|  +---------------------------+  +---------------------------+  +-------------------------------+  |
+---------------------------------------------------------------------------------------------------+
|  AUTHOR DIRECTORY                                                                                 |
|  [ Search by author name... ]  [ Filter by City v ]  [ Filter by Status v ]  [⚡ Send Bulk (9)]   |
|                                                                                                   |
|  Name            City         Books   Total Earned    Total Pending   Status        Action        |
|  -----------------------------------------------------------------------------------------------  |
|  Priya Sharma    Mumbai         2       ₹19,908          ₹3,570       🟡 In Cycle   [View Details]|
|  Rohit Kapoor    Delhi          2       ₹84,024         ₹13,024       🔴 Overdue    [View Details]|
|  Farhan Sheikh   Lucknow        1        ₹3,120              ₹0       🟢 Fully Paid [View Details]|
+---------------------------------------------------------------------------------------------------+
|  NOTIFICATION AUDIT LOGS                                                                          |
|  Author          Trigger      Requested At      Status       Email Preview                        |
|  -----------------------------------------------------------------------------------------------  |
|  Priya Sharma    Single       Oct 26, 1:15 pm   🟢 Success   [View Email Summary]                 |
|  Bulk Batch      Bulk         Oct 26, 1:00 pm   🟢 Success   9 processed                          |
+---------------------------------------------------------------------------------------------------+
```

---

## 4. Step-by-Step Implementation

### Step 4.1: Top Navigation Bar
1. Drag a **Group (Header)**:
   - Layout: `Row`, Space-between, height `70px`, background `#FFFFFF`, border-bottom `1px solid #E2E8F0`.
2. Left:
   - Text: **BookLeaf Admin Console** (Bold, `18px`, color `#0F172A`).
3. Right:
   - Text: `Current User's email` (`admin@bookleaf.com`)
   - Button: **Logout**
     - Workflow: **Account > Log the user out** &rarr; **Navigation > Go to page `login`**.

---

### Step 4.2: Catalog Summary Strip (3 Metric Cards)
Place a Group with layout `Row` (wrapping on mobile), containing 3 metric cards:

#### Card 1: Total Authors
- Label: `TOTAL REGISTERED AUTHORS`
- Value Text:
  > **`Do a search for Authors:count`** (Evaluates to **`10`**)

#### Card 2: Total Books
- Label: `TOTAL CATALOG PUBLICATIONS`
- Value Text:
  > **`Do a search for Books:count`** (Evaluates to **`18`**)

#### Card 3: Total Pending Royalties
- Label: `TOTAL PENDING ROYALTIES`
- Value Text (Highlight color `#D97706`):
  > `₹` + **`Do a search for Books's royalty_pending:sum:formatted as 1,028`** (Evaluates to **`₹40,839`**)

---

### Step 4.3: Author Directory & Filter Controls
Create a container for the Directory with 4 controls above the table:

1. **Search Input (`Input Author Search`):**
   - Placeholder: `Search author name...`
   - Content format: `Text`

2. **City Dropdown (`Dropdown City Filter`):**
   - Placeholder: `All Cities`
   - Choices style: **Dynamic choices**
   - Type of choices: `text`
   - Choices source: **`Do a search for Authors's city:unique elements`**

3. **Status Dropdown (`Dropdown Status Filter`):**
   - Placeholder: `All Statuses`
   - Choices style: **Static choices**
   - Options:
     ```text
     All
     Pending
     Overdue
     Fully Paid
     ```

4. **Bulk Trigger Button (`Btn Bulk Trigger`):**
   - Label: `⚡ Generate & Send Bulk Summaries`
   - Style: Purple / Navy Primary Button (`#4F46E5`).

---

### Step 4.4: Author Directory Repeating Group
1. Drag a **Repeating Group**:
   - **Type of content:** `Author`
   - **Data source:**
     > **`Do a search for Authors`**
     > *Constraint 1:* `name contains Input Author Search's value` *(ignore empty constraints = yes)*
     > *Constraint 2:* `city = Dropdown City Filter's value` *(ignore empty constraints = yes)*
   - **Sort by:** `name` (ascending = `yes`)

2. Inside each row / cell:
   - **Name:** `Current cell's Author's name` (Bold)
   - **City:** `Current cell's Author's city`
   - **Books Count:** `Do a search for Books (author = Current cell's Author):count`
   - **Total Earned:** `₹` + `Do a search for Books (author = Current cell's Author)'s total_royalty_earned:sum:formatted as 1,028`
   - **Total Pending:** `₹` + `Do a search for Books (author = Current cell's Author)'s royalty_pending:sum:formatted as 1,028`
   - **Status Badge:**
     - 🟢 **Fully Paid:** When `Total Pending is 0` (Farhan Sheikh)
     - 🔴 **Overdue:** When `Total Pending > 0` AND any book has `last payout > 90d ago`
     - 🟡 **In Cycle:** When `Total Pending > 0` AND not overdue
   - **Action Button:** `"View Details"`
     - Workflow: **Set custom state** `selected_author = Current cell's Author` &rarr; **Show Popup Author Detail**.

---

### Step 4.5: Author Detail Modal (`Popup Author Detail`)
Drag a **Popup** onto the page named `Popup Author Detail`:
- **Type of content:** `Author`
- **Data source:** (leave empty, populated dynamically when opened).

Inside the popup:
1. **Profile Header:**
   - Author Name, Email, Phone, City, Joined Date (`Apr 10, 2024`).
2. **Single Trigger Action Button:**
   - Label: `✉️ Generate & Send Royalty Summary`
   - Workflow:
     - Step 1: **Data > Create a new thing > `NotificationLog`**:
       - `author`: `Popup Author Detail's Author`
       - `trigger_type`: `"Single"`
       - `status`: `"Pending"`
       - `idempotency_key`: `[author_id]_[Current date/time:formatted as yyyymmdd]`
       - `requested_at`: `Current date/time`
     - Step 2: Show alert: `"Notification request queued! Dispatched to n8n workflow."`
     - Step 3: Call n8n webhook (connected in Phase 5).
3. **Books Table (Repeating Group):**
   - Type of content: `Book`
   - Data source: `Do a search for Books (author = Popup Author Detail's Author)`
   - Displays: Title, Status, Copies Sold, Earned, Paid, Pending, Last Payout.

---

### Step 4.6: Notification Audit Log Table
Below the author directory on the `/admin` page, add the Notification Audit Log:
1. Drag a **Repeating Group**:
   - **Type of content:** `NotificationLog`
   - **Data source:** `Do a search for NotificationLogs` (Sort by `requested_at`, descending = `yes`).
2. Inside each row:
   - **Target Author:** `Current cell's NotificationLog's author's name`
   - **Trigger Type:** `Current cell's NotificationLog's trigger_type` (`Single` or `Bulk`)
   - **Requested At:** `Current cell's NotificationLog's requested_at:formatted as mmm dd, yyyy hh:mm am`
   - **Status Badge:**
     - 🟡 `Pending` (Yellow)
     - 🔵 `In Progress` (Blue)
     - 🟢 `Success` (Green)
     - 🔴 `Failed` (Red)
   - **Action Button:** `"View Email Summary"`
     - *Only visible when:* `Current cell's NotificationLog's summary_content is not empty`
     - Workflow: Open `Popup View Summary` displaying the generated AI email text!
   - **Action Button:** `"View Error"`
     - *Only visible when:* `Current cell's NotificationLog's status is "Failed"`
     - Workflow: Open `Popup View Error` displaying `error_message`.

---

## 5. Phase 4 Verification Checklist

- [ ] Route Guard: Non-admin users attempting to open `/admin` are redirected to `/author-dashboard` or `/login`.
- [ ] Catalog Summary Strip displays: Authors: **10**, Books: **18**, Pending: **₹40,839**.
- [ ] Author Search filters the 10 rows in real-time as text is typed.
- [ ] City Filter dropdown isolates authors by city (e.g. selecting `Mumbai` shows only Priya Sharma).
- [ ] Status Filter dropdown filters by `Fully Paid`, `Pending`, or `Overdue`.
- [ ] Clicking `"View Details"` opens `Popup Author Detail` populated with that author's full profile and book catalog.
- [ ] Clicking `"Generate & Send Royalty Summary"` creates a `Pending` record in `NotificationLog`.
- [ ] Clicking `"Generate & Send Bulk Summaries"` targets the 9 eligible authors (skips Farhan Sheikh `AUTH008`).
- [ ] Notification Log table renders rows with real-time status badges and view summary modals.

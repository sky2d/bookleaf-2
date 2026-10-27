# Phase 2: Authentication & Privacy Architecture Guide

This document provides step-by-step technical instructions for implementing **Phase 2** of the BookLeaf Author Royalty Dashboard project.

---

## 1. Objectives & Scope

1. Build the `/login` authentication page with role-based routing (Admin vs. Author).
2. Seed test accounts for Admin and Authors in Bubble App Data.
3. Configure strict database-level **Privacy Rules** in Bubble to enforce zero data leakage between authors.
4. Set up route guards on future protected routes (`/admin` and `/author-dashboard`).
5. Verify cross-author isolation via browser developer tools.

---

## 2. Test Account Credentials

The following test accounts will be created in Bubble (**Data > App Data > All Users > New entry** or via registration workflow):

| Role | Email | Password (Recommended) | Linked Author | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Admin** | `admin@bookleaf.com` | `AdminPass@2026` | *(None / empty)* | Full access to Admin Portal, all authors, books, and logs |
| **Author 1** | `priya.sharma@email.com` | `AuthorPass@2026` | `AUTH001` (Priya Sharma) | Access only to Priya Sharma's books (`BK001`, `BK002`) |
| **Author 2** | `rohit.kapoor@email.com` | `AuthorPass@2026` | `AUTH002` (Rohit Kapoor) | Access only to Rohit Kapoor's books (`BK003`, `BK004`) |

---

## 3. Step-by-Step Execution Plan

### Task P2-01: Build `/login` Page & Routing Workflow

1. In Bubble Editor, open **Pages** dropdown &rarr; click **Add a new page** &rarr; Page name: `login` (or configure on `index`).
2. Add a clean, centered container card:
   - **Header:** "BookLeaf Publishing - Portal Login"
   - **Subheader:** "Sign in to access your author royalty dashboard or admin console"
   - **Input A:** Type: `Email`, Placeholder: `Enter your email address`, ID: `input-email`
   - **Input B:** Type: `Password`, Placeholder: `Enter your password`, ID: `input-password`
   - **Button:** Label: "Sign In", ID: `btn-login`
   - **Alert / Text element (Conditional):** "Invalid email or password", hidden by default.
3. Configure Login Workflow on **Button "Sign In" is clicked**:
   - **Action 1: Account &rarr; Log the user in**:
     - Email: `Input Email's value`
     - Password: `Input Password's value`
     - Stay logged in: `yes`
   - **Action 2: Navigation &rarr; Go to page `admin`**:
     - *Only when:* `Current User's role is "Admin"`
   - **Action 3: Navigation &rarr; Go to page `author-dashboard`**:
     - *Only when:* `Current User's role is "Author"`

---

### Task P2-02 & P2-03: Seed User Accounts in Bubble

In Bubble Editor &rarr; **Data &rarr; App Data &rarr; All Users**:

#### Step 1: Create Admin Account
1. Click **New entry**.
2. Set:
   - `email`: `admin@bookleaf.com`
   - `role`: `Admin`
   - `linked_author`: *(leave blank)*
3. Use Bubble's **Send password reset email** or run a one-time "Sign the user up" workflow to set password to `AdminPass@2026`.

#### Step 2: Create Author 1 (Priya Sharma)
1. Click **New entry**.
2. Set:
   - `email`: `priya.sharma@email.com`
   - `role`: `Author`
   - `linked_author`: Select `AUTH001 - Priya Sharma`
3. Set password: `AuthorPass@2026`.

#### Step 3: Create Author 2 (Rohit Kapoor)
1. Click **New entry**.
2. Set:
   - `email`: `rohit.kapoor@email.com`
   - `role`: `Author`
   - `linked_author`: Select `AUTH002 - Rohit Kapoor`
3. Set password: `AuthorPass@2026`.

---

### Task P2-04 through P2-07: Configure Bubble Privacy Rules

Navigate to **Data &rarr; Privacy** in Bubble. Privacy Rules run server-side and guarantee zero sensitive data is exposed over the network.

#### 1. Entity: `User` (Task P2-04)
- **Rule Name:** `Admin Full Access`
  - *When:* `Current User's role is "Admin"`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Rule Name:** `Self Access`
  - *When:* `This User is Current User`
  - *Permissions:* Check **View all fields**.
- **Everyone Else (Default permissions):**
  - **Uncheck** all field checkboxes.
  - **Uncheck** "Find this in searches".

#### 2. Entity: `Author` (Task P2-05)
- **Rule Name:** `Admin Full Access`
  - *When:* `Current User's role is "Admin"`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Rule Name:** `Author Self View`
  - *When:* `Current User's linked_author is This Author`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Everyone Else (Default permissions):**
  - **Uncheck** all field checkboxes.
  - **Uncheck** "Find this in searches".

#### 3. Entity: `Book` (Task P2-06)
- **Rule Name:** `Admin Full Access`
  - *When:* `Current User's role is "Admin"`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Rule Name:** `Author Own Books View`
  - *When:* `Current User's linked_author is This Book's author`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Everyone Else (Default permissions):**
  - **Uncheck** all field checkboxes.
  - **Uncheck** "Find this in searches".

#### 4. Entity: `NotificationLog` (Task P2-07)
- **Rule Name:** `Admin Full Access`
  - *When:* `Current User's role is "Admin"`
  - *Permissions:* Check **View all fields**, Check **Find this in searches**.
- **Everyone Else (Default permissions):**
  - **Uncheck** all field checkboxes.
  - **Uncheck** "Find this in searches".

---

### Task P2-08: Data Isolation & Route Guard Verification

1. **Verify Author Isolation:**
   - In Bubble App Data, click **Run as** next to `priya.sharma@email.com`.
   - Open browser Developer Tools (`F12` &rarr; **Network** tab).
   - In the console, inspect data objects or check requests.
   - Confirm only Priya Sharma's 2 books (`BK001`, `BK002`) are fetched.
   - Confirm Rohit Kapoor's books (`BK003`, `BK004`) cannot be queried or viewed.
2. **Verify Route Guards:**
   - Attempt to navigate directly to `/admin` while logged in as Priya Sharma.
   - Confirm the page automatically redirects back to `/login` or `/author-dashboard`.
   - Attempt to navigate to `/admin` or `/author-dashboard` in an Incognito window without logging in.
   - Confirm unauthenticated users are forced to `/login`.

---

## 4. Phase 2 Checklist

- [ ] `P2-01`: Build `/login` page and role-based redirect workflow
- [ ] `P2-02`: Seed Admin user `admin@bookleaf.com`
- [ ] `P2-03`: Seed Author users `priya.sharma@email.com` and `rohit.kapoor@email.com`
- [ ] `P2-04`: Configure `User` Privacy Rules
- [ ] `P2-05`: Configure `Author` Privacy Rules
- [ ] `P2-06`: Configure `Book` Privacy Rules
- [ ] `P2-07`: Configure `NotificationLog` Privacy Rules
- [ ] `P2-08`: Audit data isolation in browser DevTools (zero cross-author leaks)

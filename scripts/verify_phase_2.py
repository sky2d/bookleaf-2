#!/usr/bin/env python3
"""
scripts/verify_phase_2.py
-------------------------
Verification script for Phase 2: Authentication & Privacy Architecture.
Checks page accessibility on Bubble version-test and audits required accounts/privacy configurations.
"""

import sys
import urllib.request
import urllib.error

BASE_URL = "https://bookleaf-royalty-portal-93860.bubbleapps.io/version-test"

PAGES_TO_CHECK = [
    ("login", "Task P2-01: Login Page"),
    ("admin", "Admin Route Target"),
    ("author-dashboard", "Author Dashboard Route Target"),
]

def check_page_status(slug, description):
    url = f"{BASE_URL}/{slug}"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        response = urllib.request.urlopen(req, timeout=10)
        status = response.getcode()
        print(f"  [PASS] {description}: '{slug}' returned HTTP {status} (Page exists)")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [PENDING] {description}: '{slug}' returned HTTP 404 (Page not created yet)")
        else:
            print(f"  [WARN] {description}: '{slug}' returned HTTP {e.code}")
        return False
    except Exception as e:
        print(f"  [ERROR] {description}: Failed to connect ({e})")
        return False

def print_phase_2_audit_checklist():
    print("\n" + "="*70)
    print("PHASE 2: AUTHENTICATION & PRIVACY ARCHITECTURE CHECKLIST")
    print("="*70)
    
    print("\n1. Page Availability Check:")
    results = [check_page_status(slug, desc) for slug, desc in PAGES_TO_CHECK]
    all_pages_ready = all(results)

    print("\n2. Test Account Seeding Specs:")
    print("  - Admin:  admin@bookleaf.com   | role: 'Admin'  | linked_author: (empty)")
    print("  - Author: priya.sharma@email.com | role: 'Author' | linked_author: AUTH001")
    print("  - Author: rohit.kapoor@email.com | role: 'Author' | linked_author: AUTH002")

    print("\n3. Privacy Rules Requirements (Bubble Data > Privacy):")
    print("  - User:            Admin Full Access, Self View Only, Others Blocked")
    print("  - Author:          Admin Full Access, linked_author == This Author, Others Blocked")
    print("  - Book:            Admin Full Access, linked_author == This Book's author, Others Blocked")
    print("  - NotificationLog: Admin Full Access, Others Blocked")

    print("\n" + "="*70)
    if all_pages_ready:
        print("Status: All Phase 2 routes are reachable on Bubble!")
    else:
        print("Status: Routes pending creation in Bubble Editor.")
    print("="*70 + "\n")

if __name__ == "__main__":
    print_phase_2_audit_checklist()

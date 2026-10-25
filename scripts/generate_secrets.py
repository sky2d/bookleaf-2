import secrets
import sys

def generate():
    sys.stdout.reconfigure(encoding='utf-8')
    webhook_secret = secrets.token_hex(24)
    bubble_token = secrets.token_hex(32)
    
    print("=" * 70)
    print(" BookLeaf Security Token Generator (Phase 0 - Task P0-06)")
    print("=" * 70)
    print(f"X-BookLeaf-Secret (Webhook Shared Secret):\n  {webhook_secret}\n")
    print(f"BUBBLE_API_TOKEN (Bearer Token for n8n -> Bubble callback):\n  {bubble_token}\n")
    print("Copy these values into your .env or n8n credential store.")
    print("=" * 70)

if __name__ == '__main__':
    generate()

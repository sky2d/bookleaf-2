import json

def audit():
    with open('data/sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    authors = data.get('authors', [])
    print(f"Total authors: {len(authors)}")
    
    total_books = 0
    total_earned = 0
    total_paid = 0
    total_pending = 0
    
    for a in authors:
        books = a.get('books', [])
        total_books += len(books)
        for b in books:
            earned = b.get('total_royalty_earned') or 0
            paid = b.get('royalty_paid') or 0
            pending = b.get('royalty_pending') or 0
            
            total_earned += earned
            total_paid += paid
            total_pending += pending
            
            # check math consistency
            sold = b.get('total_copies_sold') or 0
            royalty_per_copy = b.get('author_royalty_per_copy') or 0
            if royalty_per_copy > 0:
                assert earned == sold * royalty_per_copy, f"Math mismatch in {b['book_id']}"
            assert earned == paid + pending, f"Earned != Paid + Pending in {b['book_id']}"
            
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 80)
    print(f"{'Author ID':<10} {'Name':<20} {'Books':<6} {'Earned':<12} {'Paid':<12} {'Pending':<12}")
    print("-" * 80)
    for a in authors:
        a_books = a.get('books', [])
        a_earned = sum(b.get('total_royalty_earned') or 0 for b in a_books)
        a_paid = sum(b.get('royalty_paid') or 0 for b in a_books)
        a_pending = sum(b.get('royalty_pending') or 0 for b in a_books)
        print(f"{a['author_id']:<10} {a['name']:<20} {len(a_books):<6} {a_earned:<12} {a_paid:<12} {a_pending:<12}")
    print("=" * 80)
    print(f"Total authors: {len(authors)}")
    print(f"Total books: {total_books}")
    print(f"Total Earned: INR {total_earned:,}")
    print(f"Total Paid: INR {total_paid:,}")
    print(f"Total Pending: INR {total_pending:,}")

if __name__ == '__main__':
    audit()

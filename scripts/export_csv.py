import json
import csv
import os

def export_csvs():
    with open('data/sample_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    authors = data.get('authors', [])
    
    os.makedirs('data', exist_ok=True)
    
    # Export authors.csv
    author_fields = ['author_id', 'name', 'email', 'phone', 'city', 'joined_date']
    with open('data/authors.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=author_fields)
        writer.writeheader()
        for a in authors:
            writer.writerow({
                'author_id': a.get('author_id', ''),
                'name': a.get('name', ''),
                'email': a.get('email', ''),
                'phone': a.get('phone', ''),
                'city': a.get('city', ''),
                'joined_date': a.get('joined_date', '')
            })
    print(f"Exported {len(authors)} authors to data/authors.csv")
    
    # Export books.csv
    book_fields = [
        'book_id',
        'author_id',
        'title',
        'isbn',
        'genre',
        'publication_date',
        'status',
        'mrp',
        'author_royalty_per_copy',
        'total_copies_sold',
        'total_royalty_earned',
        'royalty_paid',
        'royalty_pending',
        'last_royalty_payout_date',
        'print_partner',
        'available_on'
    ]
    
    books_count = 0
    with open('data/books.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=book_fields)
        writer.writeheader()
        for a in authors:
            for b in a.get('books', []):
                books_count += 1
                available_on_list = b.get('available_on') or []
                # Delimit list with comma or pipe for Bubble multi-value import
                available_on_str = ", ".join(available_on_list)
                
                writer.writerow({
                    'book_id': b.get('book_id', ''),
                    'author_id': a.get('author_id', ''),
                    'title': b.get('title', ''),
                    'isbn': b.get('isbn', ''),
                    'genre': b.get('genre', ''),
                    'publication_date': b.get('publication_date') or '',
                    'status': b.get('status', ''),
                    'mrp': b.get('mrp') if b.get('mrp') is not None else '',
                    'author_royalty_per_copy': b.get('author_royalty_per_copy') if b.get('author_royalty_per_copy') is not None else '',
                    'total_copies_sold': b.get('total_copies_sold', 0),
                    'total_royalty_earned': b.get('total_royalty_earned', 0),
                    'royalty_paid': b.get('royalty_paid', 0),
                    'royalty_pending': b.get('royalty_pending', 0),
                    'last_royalty_payout_date': b.get('last_royalty_payout_date') or '',
                    'print_partner': b.get('print_partner') or '',
                    'available_on': available_on_str
                })
    print(f"Exported {books_count} books to data/books.csv")

if __name__ == '__main__':
    export_csvs()

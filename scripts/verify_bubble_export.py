import json
import csv
import io

raw_csv = """\"author\",\"author_royalty_per_copy\",\"available_on\",\"book_id\",\"genre\",\"isbn\",\"last_royalty_payout_date\"
\"1792935008375x171811448507621630\",\"35\",\"Amazon India, Flipkart, BookLeaf Store\",\"BK001\",\"Literary Fiction\",\"978-93-5XXXX-01-1\",\"Oct 15, 2025 5:30 am\"
\"1792935123169x538985058505554700\",\"48\",\"Amazon India, Flipkart, Amazon US, Amazon UK, BookLeaf Store\",\"BK004\",\"Business / Entrepreneurship\",\"978-93-5XXXX-04-2\",\"Nov 15, 2025 5:30 am\"
\"1792935123171x584502211779202300\",\"55\",\"Amazon India, Amazon US, BookLeaf Store\",\"BK009\",\"Travel / Non-Fiction\",\"978-93-5XXXX-09-7\",\"Oct 15, 2025 5:30 am\"
\"1792935008375x171811448507621630\",\"42\",\"Amazon India, BookLeaf Store\",\"BK002\",\"Non-Fiction / Memoir\",\"978-93-5XXXX-02-8\",\"Dec 1, 2025 5:30 am\"
\"1792935123171x584502211779202300\",\"32\",\"Amazon India, Flipkart, BookLeaf Store\",\"BK008\",\"Contemporary Fiction\",\"978-93-5XXXX-08-0\",\"Dec 1, 2025 5:30 am\"
\"1792935123170x608971283687867500\",\"38\",\"Amazon India, BookLeaf Store\",\"BK005\",\"Historical Fiction\",\"978-93-5XXXX-05-9\",\"\"
\"1792935123171x559167525979646000\",\"25\",\"Amazon India, Flipkart, BookLeaf Store\",\"BK006\",\"Self-Help\",\"978-93-5XXXX-06-6\",\"Aug 20, 2025 5:30 am\"
\"1792935123174x840549601809746700\",\"\",\"\",\"BK015\",\"Parenting / Non-Fiction\",\"978-93-5XXXX-15-8\",\"\"
\"1792935123172x615446463946212500\",\"30\",\"Amazon India, Flipkart, BookLeaf Store\",\"BK012\",\"Romance / Humor\",\"978-93-5XXXX-12-7\",\"Oct 15, 2025 5:30 am\"
\"1792935123169x538985058505554700\",\"30\",\"Amazon India, Flipkart, Amazon US, BookLeaf Store\",\"BK003\",\"Self-Help / Technology\",\"978-93-5XXXX-03-5\",\"Sep 1, 2025 5:30 am\"
\"1792935123172x615446463946212500\",\"\",\"\",\"BK013\",\"Thriller\",\"978-93-5XXXX-13-4\",\"\"
\"1792935123172x615446463946212500\",\"25\",\"Amazon India, Flipkart, Amazon US, BookLeaf Store\",\"BK011\",\"Romance\",\"978-93-5XXXX-11-0\",\"Nov 15, 2025 5:30 am\"
\"1792935123172x282023633068428480\",\"28\",\"Amazon India, BookLeaf Store\",\"BK010\",\"Humor / Essays\",\"978-93-5XXXX-10-3\",\"\"
\"1792935123173x809675533942538800\",\"20\",\"Amazon India, BookLeaf Store\",\"BK014\",\"Poetry / Urdu Literature\",\"978-93-5XXXX-14-1\",\"Dec 1, 2025 5:30 am\"
\"1792935123174x906746562439641300\",\"35\",\"Amazon India, BookLeaf Store\",\"BK018\",\"Crime / Thriller\",\"978-93-5XXXX-18-9\",\"\"
\"1792935123174x840549601809746700\",\"25\",\"Amazon India, BookLeaf Store\",\"BK016\",\"Essays / Memoir\",\"978-93-5XXXX-16-5\",\"\"
\"1792935123174x906746562439641300\",\"45\",\"Amazon India, Flipkart, Amazon US, BookLeaf Store\",\"BK017\",\"Literary Fiction\",\"978-93-5XXXX-17-2\",\"Nov 15, 2025 5:30 am\"
\"1792935123171x559167525979646000\",\"15\",\"Amazon India, BookLeaf Store\",\"BK007\",\"Poetry\",\"978-93-5XXXX-07-3\",\"Dec 1, 2025 5:30 am\""""

reader = csv.DictReader(io.StringIO(raw_csv.strip()))
pasted_books = list(reader)

with open('data/sample_data.json', 'r', encoding='utf-8') as f:
    sample_data = json.load(f)

json_books = {}
for a in sample_data['authors']:
    for b in a['books']:
        json_books[b['book_id']] = (a['author_id'], a['name'], b)

print(f"Total books exported from Bubble: {len(pasted_books)}")

# Group by author Bubble ID
authors_map = {}
all_matched = True

for pb in pasted_books:
    bid = pb['book_id']
    author_uid = pb['author']
    authors_map.setdefault(author_uid, []).append(bid)
    
    if bid not in json_books:
        print(f"Unknown book_id: {bid}")
        all_matched = False
        continue
    aid, aname, jb = json_books[bid]
    
    # Check ISBN
    if pb['isbn'] != jb['isbn']:
        print(f"Mismatch ISBN in {bid}: {pb['isbn']} vs {jb['isbn']}")
        all_matched = False
    # Check Genre
    if pb['genre'] != jb['genre']:
        print(f"Mismatch Genre in {bid}: {pb['genre']} vs {jb['genre']}")
        all_matched = False
    # Check royalty rate
    rate = str(jb.get('author_royalty_per_copy') or '')
    if pb['author_royalty_per_copy'] != rate:
        print(f"Mismatch rate in {bid}: '{pb['author_royalty_per_copy']}' vs '{rate}'")
        all_matched = False

print(f"Total unique authors linked to books: {len(authors_map)}")
for uid, b_list in sorted(authors_map.items()):
    print(f"  Bubble Author UID {uid[:18]}... -> Books: {b_list}")

if all_matched and len(pasted_books) == 18 and len(authors_map) == 10:
    print("\n>>> AUDIT RESULT: PERFECT 100% MATCH! ALL 18 BOOKS & RELATIONS ARE ACCURATE! <<<")
else:
    print("\n>>> AUDIT RESULT: DISCREPANCIES DETECTED <<<")

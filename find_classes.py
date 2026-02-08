import sys
sys.path.insert(0, 'brauler')

from data_parser import Parser

print("=" * 60)
print("Finding the correct div classes")
print("=" * 60)

course_id = 61954
parser = Parser(course_id)

# Find all divs with 'Table' class
table_divs = parser.html.find_all('div', class_='Table')
print(f"\nFound {len(table_divs)} divs with class 'Table'")

for i, div in enumerate(table_divs):
    classes = div.get('class', [])
    print(f"\nDiv {i} classes: {' '.join(classes)}")
    
    # Check if it has rows
    rows = div.find_all('div', class_='row')
    print(f"  Rows found: {len(rows)}")
    
    if len(rows) >= 2:
        print(f"  ✅ This div has lesson data!")
        # Try to extract data from row[1]
        try:
            cells = rows[1].find_all('div')
            print(f"  Cells in row[1]: {len(cells)}")
            if len(cells) > 0:
                print(f"  Sample data: {[cell.text.strip()[:20] for cell in cells[:5]]}")
        except Exception as e:
            print(f"  Error extracting: {e}")

print("\n" + "=" * 60)

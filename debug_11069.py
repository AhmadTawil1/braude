import sys
sys.path.insert(0, 'brauler')

from data_parser import Parser

print("=" * 60)
print("Inspecting Course 11069 HTML Structure")
print("=" * 60)

course_id = 11069
print(f"\nFetching HTML for course {course_id}...")

try:
    parser = Parser(course_id)
    
    print(f"\n✅ HTML fetched successfully")
    print(f"Course name: {parser.get_name()}")
    print(f"Types found: {parser.types_list}")
    print(f"Data list length: {len(parser.data_list)}")
    
    print("\n" + "=" * 60)
    print("Analyzing all Table divs:")
    print("=" * 60)
    
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
            print(f"  ✅ This div has 2+ rows")
            # Try to extract data from row[1]
            try:
                cells = rows[1].find_all('div')
                print(f"  Cells in row[1]: {len(cells)}")
                if len(cells) > 0:
                    cell_texts = [cell.text.strip()[:30] for cell in cells[:10]]
                    print(f"  Sample data: {cell_texts}")
            except Exception as e:
                print(f"  Error extracting: {e}")
    
    print("\n" + "=" * 60)
    print("Checking 'ncontainer WithSearch' divs specifically:")
    print("=" * 60)
    
    search_divs = parser.html.find_all('div', class_='Table container ncontainer WithSearch')
    print(f"\nFound {len(search_divs)} divs with 'ncontainer WithSearch'")
    
    for i, div in enumerate(search_divs):
        rows = div.find_all('div', class_='row')
        print(f"\nDiv {i}: {len(rows)} rows")
        if len(rows) == 2:
            print(f"  ✅ Has exactly 2 rows - should be included!")
        elif len(rows) == 1:
            print(f"  ⚠️ Only 1 row - filtered out")
        else:
            print(f"  ⚠️ {len(rows)} rows - filtered out")
    
    # Save full HTML for manual inspection
    with open('course_11069_debug.html', 'w', encoding='utf-8') as f:
        f.write(parser.html.prettify())
    print(f"\n✅ Saved full HTML to course_11069_debug.html")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

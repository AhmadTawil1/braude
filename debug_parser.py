import sys
sys.path.insert(0, 'brauler')

from data_parser import Parser

print("=" * 60)
print("Inspecting Braude Website HTML Structure")
print("=" * 60)

course_id = 61954
print(f"\nFetching HTML for course {course_id}...")

try:
    parser = Parser(course_id)
    
    print(f"\n✅ HTML fetched successfully")
    print(f"Course name: {parser.get_name()}")
    print(f"Types found: {parser.types_list}")
    print(f"Data list length: {len(parser.data_list)}")
    
    print("\n" + "=" * 60)
    print("Analyzing data_list structure:")
    print("=" * 60)
    
    for i, data_item in enumerate(parser.data_list):
        print(f"\nData item {i}:")
        print(f"  Type: {parser.types_list[i] if i < len(parser.types_list) else 'N/A'}")
        
        # Try to find rows
        rows = data_item.find_all('div', class_='row')
        print(f"  Rows found: {len(rows)}")
        
        if len(rows) > 1:
            print(f"  Row[1] children: {len(list(rows[1].children))}")
            row_data = [cell.text.strip() for cell in rows[1]]
            print(f"  Row[1] data: {row_data}")
        
        # Save HTML for inspection
        if i == 0:
            with open('debug_html.html', 'w', encoding='utf-8') as f:
                f.write(str(data_item.prettify()))
            print(f"  ✅ Saved first data item HTML to debug_html.html")
    
    print("\n" + "=" * 60)
    print("Checking for alternative table structures...")
    print("=" * 60)
    
    # Check for other possible table structures
    all_tables = parser.html.find_all('table')
    print(f"Total <table> elements: {len(all_tables)}")
    
    all_divs_with_table = parser.html.find_all('div', class_='Table')
    print(f"Total <div class='Table'> elements: {len(all_divs_with_table)}")
    
    all_divs_with_container = parser.html.find_all('div', class_='container')
    print(f"Total <div class='container'> elements: {len(all_divs_with_container)}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

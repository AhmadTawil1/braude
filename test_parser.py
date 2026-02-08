"""
Debug script to test the course parser
"""
import sys
sys.path.insert(0, 'brauler')

from data_parser import Parser

# Test with the working course ID
course_id = 61954

print(f"Testing parser with course ID: {course_id}")
print("=" * 50)

try:
    parser = Parser(course_id)
    print(f"✓ Parser created successfully")
    print(f"✓ URL: {parser.url}")
    
    # Test get_name
    try:
        name = parser.get_name()
        print(f"✓ Course name: {name}")
    except Exception as e:
        print(f"✗ Error getting name: {e}")
    
    # Test get_types
    try:
        types = parser.get_types()
        print(f"✓ Types found: {types}")
        print(f"  Number of types: {len(types)}")
    except Exception as e:
        print(f"✗ Error getting types: {e}")
    
    # Test get_about
    try:
        about = parser.get_about()
        print(f"✓ About info found")
        print(f"  Number of about items: {len(about)}")
        if about:
            print(f"  First item: {about[0][:100]}...")
    except Exception as e:
        print(f"✗ Error getting about: {e}")
    
    # Test get_data
    try:
        data = parser.get_data()
        print(f"✓ Data found")
        print(f"  Number of data items: {len(data)}")
    except Exception as e:
        print(f"✗ Error getting data: {e}")
    
    print("\n" + "=" * 50)
    print("Parser test completed!")
    
except Exception as e:
    print(f"✗ Fatal error creating parser: {e}")
    import traceback
    traceback.print_exc()

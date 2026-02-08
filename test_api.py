import requests
import json

# Test the API
BASE_URL = "http://localhost:5000"

# Create a session to maintain cookies
session = requests.Session()

print("=" * 60)
print("Testing Tanzim Braude API")
print("=" * 60)

# Test 1: Add a course
print("\n1. Adding course 61954...")
response = session.post(
    f"{BASE_URL}/api/courses",
    json={"course_id": 61954},
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print(f"Response:")
data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

# Check schedule
if data.get('schedule'):
    print(f"\n✅ Schedule has {len(data['schedule'])} lessons")
    print(f"Total schedules available: {data.get('total_schedules', 0)}")
else:
    print("\n❌ Schedule is null or empty!")
    print(f"Total schedules available: {data.get('total_schedules', 0)}")

# Test 2: Get schedule
print("\n" + "=" * 60)
print("2. Getting current schedule...")
response = session.get(f"{BASE_URL}/api/schedule")
print(f"Status Code: {response.status_code}")
data = response.json()
print(f"Response:")
print(json.dumps(data, indent=2, ensure_ascii=False))

if data.get('schedule'):
    print(f"\n✅ Schedule has {len(data['schedule'])} lessons")
else:
    print("\n❌ Schedule is null or empty!")

print("\n" + "=" * 60)

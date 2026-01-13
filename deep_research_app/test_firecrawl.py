"""
Test script to verify Firecrawl API functionality
"""
import os
import sys
from dotenv import load_dotenv
from firecrawl import Firecrawl

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("FIRECRAWL_API_KEY")

if not api_key:
    print("[ERROR] FIRECRAWL_API_KEY not found in environment variables")
    exit(1)

print(f"[OK] API Key found: {api_key[:10]}...")

# Initialize Firecrawl client
try:
    firecrawl = Firecrawl(api_key=api_key)
    print("[OK] Firecrawl client initialized successfully")
except Exception as e:
    print(f"[ERROR] Error initializing Firecrawl client: {e}")
    exit(1)

# Test 1: Simple scrape
print("\n" + "="*50)
print("TEST 1: Scraping a simple URL")
print("="*50)
try:
    scrape_result = firecrawl.scrape('https://firecrawl.dev', formats=['markdown'])
    print("[OK] Scrape successful!")
    print(f"  - Status: {scrape_result.get('success', 'N/A')}")
    if 'markdown' in scrape_result:
        preview = scrape_result['markdown'][:200]
        print(f"  - Content preview: {preview}...")
except Exception as e:
    print(f"[ERROR] Scrape failed: {e}")

# Test 2: Search functionality
print("\n" + "="*50)
print("TEST 2: Testing search functionality")
print("="*50)
try:
    search_results = firecrawl.search(
        query="artificial intelligence",
        limit=3
    )
    print("[OK] Search successful!")
    print(f"  - Type: {type(search_results)}")
    print(f"  - Keys: {search_results.keys() if isinstance(search_results, dict) else 'N/A'}")

    if isinstance(search_results, dict) and 'data' in search_results:
        print(f"  - Number of results: {len(search_results['data'])}")
        for i, result in enumerate(search_results['data'][:3], 1):
            print(f"  - Result {i}: {result.get('url', 'N/A')}")
    else:
        print(f"  - Results: {search_results}")

except Exception as e:
    print(f"[ERROR] Search failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Search with scrape options
print("\n" + "="*50)
print("TEST 3: Search with content extraction")
print("="*50)
try:
    search_results = firecrawl.search(
        query="Python programming",
        limit=2,
        scrape_options={
            "formats": ["markdown"]
        }
    )
    print("[OK] Search with scrape options successful!")

    if isinstance(search_results, dict) and 'data' in search_results:
        print(f"  - Number of results: {len(search_results['data'])}")
        for i, result in enumerate(search_results['data'], 1):
            print(f"\n  Result {i}:")
            print(f"    - URL: {result.get('url', 'N/A')}")
            print(f"    - Title: {result.get('title', 'N/A')}")
            if 'markdown' in result:
                preview = result['markdown'][:150]
                print(f"    - Content preview: {preview}...")
    else:
        print(f"  - Results structure: {search_results}")

except Exception as e:
    print(f"[ERROR] Search with scrape options failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("[OK] All tests completed!")
print("="*50)

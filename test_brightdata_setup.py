from dotenv import load_dotenv
import os
import requests

def test_brightdata_setup():
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv('BRIGHTDATA_API_KEY')
    if not api_key:
        print("❌ ERROR: BRIGHTDATA_API_KEY not found in .env file!")
        return False
    
    # Setup headers
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    # Test API connection
    test_url = "https://api.brightdata.com/datasets/v3/datasets"
    try:
        print("\n🔍 Testing Bright Data API connection...")
        response = requests.get(test_url, headers=headers)
        
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text[:500]}...")  # Show first 500 chars
        
        if response.status_code == 401:
            print("\n❌ ERROR: Invalid API key or unauthorized access")
            return False
        elif response.status_code != 200:
            print(f"\n❌ ERROR: API test failed with status {response.status_code}")
            return False
        
        print("\n✅ API connection successful!")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    if test_brightdata_setup():
        print("\nYour Bright Data setup is correct! You can now run the main script.")
    else:
        print("\nPlease fix the errors above and try again.")
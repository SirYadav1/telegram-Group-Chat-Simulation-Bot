import requests
import time

def test_llm_connection():
    url = "http://XXX.XXX.XX.30:5000/v1/chat"
    headers = {"Authorization": "Mygtafive"}
    
    print("🔍 Testing LLM Server Connection...")
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json={"prompt": "Hello, are you working?"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ LLM Server is WORKING!")
            print(f"Response: {response.json().get('response', 'No response')}")
        else:
            print(f"❌ LLM Server error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ LLM Server: Connection refused - Server is DOWN or URL wrong")
    except requests.exceptions.Timeout:
        print("❌ LLM Server: Timeout - Server too slow")
    except Exception as e:
        print(f"❌ LLM Server error: {e}")

if __name__ == "__main__":
    test_llm_connection()

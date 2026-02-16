import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.abspath("src"))

def test_priority_and_cloudflare():
    from index import chat_with_ai, get_env_list
    
    print("--- [AI PRIORITY & CLOUDFLARE VERIFICATION] ---")
    load_dotenv(override=True)
    env = get_env_list()
    
    # Test 1: Priority Logic (Master Groq should be used even if User Key is provided)
    print("Test 1: Master Priority Logic")
    user_api_key = "dummy_user_key"
    response_groq = chat_with_ai(
        user_prompt="Explain why Master key is better than User key briefly.",
        user_api_key=user_api_key,
        provider="Groq",
        model_id="llama-3.1-8b-instant"
    )
    print(f"🤖 [Groq Response]: {response_groq[:100]}...")
    
    # Test 2: Cloudflare Integration
    print("\nTest 2: Cloudflare Workers AI")
    cf_id = env.get("CLOUDFLARE_ID")
    cf_key = env.get("CLOUDFLARE_API_KEY")
    
    if cf_id and cf_key:
        response_cf = chat_with_ai(
            user_prompt="Say 'Cloudflare is Online'",
            user_api_key="",
            provider="Cloudflare",
            model_id="@cf/meta/llama-3.1-8b-instruct"
        )
        print(f"🤖 [Cloudflare Response]: {response_cf}")
    else:
        print("⚠️ Cloudflare credentials missing in .env")

    print("\n--- [VERIFICATION COMPLETE] ---")

if __name__ == "__main__":
    test_priority_and_cloudflare()

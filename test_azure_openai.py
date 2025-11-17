"""
Test script to verify Azure OpenAI API connection and configuration.
Configured for Cloud9AI Project Resource.

Run this script to ensure your Azure OpenAI credentials are working correctly.

Usage:
    python test_azure_openai.py
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from openai import APIError, APITimeoutError, APIConnectionError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_azure_openai_connection():
    """Test Azure OpenAI API connection and basic functionality"""
    
    print("=" * 70)
    print("Azure OpenAI Connection Test - Cloud9AI Project")
    print("=" * 70)
    
    # Step 1: Check environment variables
    print("\n1. Checking environment variables...")
    
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    
    if not azure_endpoint:
        print("   ❌ AZURE_OPENAI_ENDPOINT is not set")
        print("   Expected: https://cloud9ai-project-resource.cognitiveservices.azure.com/")
        return False
    else:
        print(f"   ✓ AZURE_OPENAI_ENDPOINT: {azure_endpoint}")
        
        # Verify it matches expected endpoint
        expected_base = "cognitiveservices.azure.com"
        if expected_base not in azure_endpoint:
            print(f"   ⚠️  Warning: Endpoint should contain '{expected_base}'")
    
    if not azure_api_key:
        print("   ❌ AZURE_OPENAI_API_KEY (subscription_key) is not set")
        return False
    else:
        # Show only first and last 4 characters
        masked_key = f"{azure_api_key[:4]}...{azure_api_key[-4:]}" if len(azure_api_key) > 8 else "****"
        print(f"   ✓ AZURE_OPENAI_API_KEY: {masked_key} (subscription_key)")
    
    if not azure_deployment:
        print("   ❌ AZURE_OPENAI_DEPLOYMENT_NAME is not set")
        return False
    else:
        print(f"   ✓ AZURE_OPENAI_DEPLOYMENT_NAME: {azure_deployment}")
    
    print(f"   ✓ AZURE_OPENAI_API_VERSION: {azure_api_version}")
    
    # Verify API version
    if azure_api_version != "2024-12-01-preview":
        print(f"   ⚠️  Warning: Expected API version '2024-12-01-preview', got '{azure_api_version}'")
    
    # Step 2: Initialize Azure OpenAI client
    print("\n2. Initializing Azure OpenAI client...")
    
    try:
        client = AsyncAzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=azure_api_version
        )
        print("   ✓ Client initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize client: {str(e)}")
        return False
    
    # Step 3: Test API call with a simple prompt
    print("\n3. Testing API call with simple prompt...")
    print("   (This will verify your deployment is working)")
    
    try:
        response = await client.chat.completions.create(
            model=azure_deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Say 'Hello! Azure OpenAI is working correctly with Cloud9AI project!' and nothing else."
                }
            ],
            temperature=0.1,
            max_tokens=50,
            timeout=30
        )
        
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            print(f"   ✓ API Response: {response_text}")
            print(f"   ✓ Model Used: {response.model}")
            
            # Log token usage
            if response.usage:
                print(f"   ✓ Token Usage:")
                print(f"     - Prompt tokens: {response.usage.prompt_tokens}")
                print(f"     - Completion tokens: {response.usage.completion_tokens}")
                print(f"     - Total tokens: {response.usage.total_tokens}")
        else:
            print("   ❌ No response from API")
            return False
            
    except APITimeoutError:
        print("   ❌ Request timed out")
        print("   Troubleshooting:")
        print("   - Check your internet connection")
        print("   - Verify Azure service is not experiencing issues")
        return False
    except APIConnectionError as e:
        print(f"   ❌ Connection error: {str(e)}")
        print("   Troubleshooting:")
        print("   - Verify endpoint URL is correct")
        print("   - Check firewall settings")
        return False
    except APIError as e:
        print(f"   ❌ API error: {str(e)}")
        print("   Troubleshooting:")
        print("   - Verify API key (subscription_key) is correct")
        print("   - Check deployment name matches Azure Portal")
        print("   - Ensure deployment is in 'Succeeded' state")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        return False
    
    # Step 4: Test with a JSON response (similar to audit analysis)
    print("\n4. Testing JSON response generation...")
    print("   (This simulates the actual audit analysis workflow)")
    
    try:
        response = await client.chat.completions.create(
            model=azure_deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that responds in JSON format."
                },
                {
                    "role": "user",
                    "content": 'Return exactly this JSON: {"status": "working", "message": "Azure OpenAI configured correctly for Cloud9AI", "test": "passed"}'
                }
            ],
            temperature=0.1,
            max_tokens=100,
            timeout=30
        )
        
        if response.choices and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            print(f"   ✓ JSON Response received (length: {len(response_text)} chars)")
            
            # Try to parse as JSON
            import json
            try:
                parsed = json.loads(response_text)
                print("   ✓ Response is valid JSON")
                print(f"   ✓ JSON Content: {json.dumps(parsed, indent=2)}")
            except json.JSONDecodeError:
                print("   ⚠️  Response is not valid JSON (this may be OK for testing)")
                print(f"   Response: {response_text[:150]}...")
        else:
            print("   ❌ No response from API")
            return False
            
    except Exception as e:
        print(f"   ❌ Error during JSON test: {str(e)}")
        return False
    
    # All tests passed
    print("\n" + "=" * 70)
    print("✓ All tests passed! Azure OpenAI is configured correctly.")
    print("=" * 70)
    print("\nYour configuration:")
    print(f"  • Endpoint: {azure_endpoint}")
    print(f"  • Deployment: {azure_deployment}")
    print(f"  • API Version: {azure_api_version}")
    print("\nYou can now run the main application:")
    print("  python main.py")
    print("  OR")
    print("  docker-compose up --build")
    print("=" * 70)
    return True


async def main():
    """Main function"""
    success = await test_azure_openai_connection()
    
    if not success:
        print("\n" + "=" * 70)
        print("❌ Tests failed. Please check your configuration.")
        print("=" * 70)
        print("\nTroubleshooting Steps:")
        print("1. Verify your .env file exists and has all required variables")
        print("2. Check Azure Portal:")
        print("   - Go to: https://portal.azure.com")
        print("   - Open your Azure OpenAI resource")
        print("   - Verify deployment is in 'Succeeded' state")
        print("3. Get fresh credentials:")
        print("   - Go to 'Keys and Endpoint'")
        print("   - Copy endpoint URL")
        print("   - Copy KEY 1 or KEY 2 (subscription_key)")
        print("4. Verify deployment name:")
        print("   - Go to 'Model deployments'")
        print("   - Copy exact deployment name")
        print("5. Check API version:")
        print("   - Should be: 2024-12-01-preview")
        print("\nFor detailed help, see: AZURE_CONFIG.md")
        print("=" * 70)
        return False
    
    return True


if __name__ == "__main__":
    # Run the test
    result = asyncio.run(main())
    exit(0 if result else 1)

import os
import sys
import argparse
import httpx
import json

def main():
    parser = argparse.ArgumentParser(description="Hyperbots API CLI")
    parser.add_argument("task", choices=["parse", "classify", "split", "extract"], help="API task to perform")
    parser.add_argument("file", help="Path to the document file (PDF, PNG, JPG)")
    parser.add_argument("--api-key", help="Hyperbots API Key (defaults to HYPERBOTS_API_KEY env var)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("HYPERBOTS_API_KEY")
    if not api_key:
        print("Error: API Key is required. Set HYPERBOTS_API_KEY environment variable or use --api-key.")
        sys.exit(1)
        
    base_url = "https://api.hyperapi.dev/v1"
    url = f"{base_url}/{args.task}"
    
    headers = {
        "X-API-Key": api_key
    }
    
    with open(args.file, "rb") as f:
        files = {"file": f}
        try:
            response = httpx.post(url, headers=headers, files=files, timeout=30.0)
            response.raise_for_status()
            print(json.dumps(response.json(), indent=2))
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()

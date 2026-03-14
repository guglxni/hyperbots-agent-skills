import os
import sys
import argparse
import httpx
import json
from pathlib import Path

# Updated base URL from SDK
DEFAULT_BASE_URL = "http://hyperapi-production-12097051.us-east-1.elb.amazonaws.com"

def main():
    parser = argparse.ArgumentParser(description="Hyperbots API (HyperAPI) CLI")
    parser.add_argument("task", choices=["parse", "classify", "split", "extract", "process", "upload"], help="API task to perform")
    parser.add_argument("file", help="Path to the document file (PDF, PNG, JPG, etc.)")
    parser.add_argument("--api-key", help="HyperAPI Key (defaults to HYPERAPI_KEY env var)")
    parser.add_argument("--base-url", help=f"Base URL (defaults to {DEFAULT_BASE_URL})")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.getenv("HYPERAPI_KEY") or "hk_live_9015f91550d87dbf23f73f5baea68d5d"
    if not api_key:
        print("Error: API Key is required. Set HYPERAPI_KEY environment variable or use --api-key.")
        sys.exit(1)
        
    base_url = args.base_url or os.getenv("HYPERAPI_URL") or DEFAULT_BASE_URL
    headers = {
        "X-API-Key": api_key
    }
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)

    try:
        if args.task == "upload":
            url = f"{base_url}/v1/documents/upload"
            resp = httpx.post(url, json={"filename": file_path.name, "content_type": "application/octet-stream"}, headers=headers)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
        
        elif args.task == "process":
            # Simplified process: parse then extract using the same upload (requires SDK-like logic if using document_key)
            # For this CLI, we'll just use multipart for simplicity or assume small files
            print("Processing (Parse + Extract)...")
            with open(file_path, "rb") as f:
                files = {"file": f}
                # This is a bit complex for a simple CLI without implementing the full 3-step flow
                # We'll just point users to the Python SDK for 'process' or implement a basic version
                url_parse = f"{base_url}/v1/parse"
                url_extract = f"{base_url}/v1/extract"
                
                # We'll do it sequentially for now
                r_parse = httpx.post(url_parse, headers=headers, files={"file": open(file_path, "rb")}, timeout=120.0)
                r_extract = httpx.post(url_extract, headers=headers, files={"file": open(file_path, "rb")}, timeout=600.0)
                
                result = {
                    "ocr": r_parse.json().get("result", {}).get("ocr"),
                    "data": r_extract.json().get("result", {})
                }
                print(json.dumps(result, indent=2))

        else:
            url = f"{base_url}/v1/{args.task}"
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = httpx.post(url, headers=headers, files=files, timeout=600.0)
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

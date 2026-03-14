---
name: hyperbots-api
description: "Financial document processing with HyperAPI (parse, classify, split, extract, process). Use when processing invoices, receipts, or financial PDFs to extract structured data, OCR text, or categorize document types. Supports S3 presigned upload flow for large files."
license: MIT
metadata:
  author: hyperbots
  version: "1.2.0"
---

# HyperAPI Skill (by Hyperbots)

This skill provides comprehensive access to HyperAPI financial document intelligence.

## Base URL

```
https://api.hyperapi.dev
```

## Capabilities

The API supports five main document processing tasks:

| Endpoint | Task | Description | Cost | Latency | Model |
|----------|------|-------------|------|---------|-------|
| `/v1/parse` | Parse | Extract raw text using OCR. Best for searchable PDFs or unstructured text. | $0.05/page | ~1s | hyperbots_vlm_ocr |
| `/v1/extract` | Extract | Vision-language extraction of structured fields (vendor, total, line items). | $0.08/page | ~2s | hyperbots_vlm_extract |
| `/v1/classify` | Classify | Automatically categorize financial documents (invoices, receipts, contracts). | $0.03/page | ~0.8s | hyperbots_vlm_ocr |
| `/v1/split` | Split | Logical segmentation of multi-document PDFs. | $0.02/page | ~0.5s | hyperbots_vlm_ocr |
| `/v1/process` | Process | Combined Parse + Extract in one upload. | Varies | Varies | Mixed |
| Upload | Upload | Presigned S3 flow for files > 50 MB. | N/A | N/A | N/A |

## Workflow

### 1. Prerequisites

- **API Key**: Requires `X-API-Key` header with prefix `hk_live_` (production) or `hk_test_` (testing).
- **SDK**: Use the `hyperapi` Python package (`pip install hyperapi`).

### 2. Authentication

```bash
curl -X POST https://api.hyperapi.dev/v1/parse \
  -H "X-API-Key: hk_live_your_key_here" \
  -F "file=@invoice.pdf"
```

### 3. Implementation Guide

For a detailed reference of all endpoints and SDK methods, see [references/api_docs.md](references/api_docs.md).

#### Python SDK Example - Quickstart

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_your_key_here")

# Parse: Extract OCR text
result = client.parse("invoice.pdf")
print(result["result"]["ocr"])

# Extract: Get structured data
result = client.extract("invoice.pdf")
print(result["result"]["entities"])
print(result["result"]["line_items"])

# Classify: Document categorization
result = client.classify("document.pdf")
print(result["result"]["label"])  # e.g., "invoice"
print(result["result"]["confidence"])  # e.g., 0.98

# Split: Multi-document segmentation
result = client.split("batch.pdf")
for segment in result["result"]["segments"]:
    print(f"Document {segment['document_index']}: pages {segment['start_page']}-{segment['end_page']}")

# Process: Combined Parse + Extract
result = client.process("invoice.pdf")
print(result["result"]["ocr"])
print(result["result"]["entities"])

client.close()
```

#### CLI Interaction

A bundled script is available: `scripts/hyperbots_cli.py`.

```bash
export HYPERAPI_KEY=hk_live_...
python3 <skill-path>/scripts/hyperbots_cli.py extract invoice.pdf
```

## Response Structure

All successful responses follow this structure:

```json
{
  "status": "success",
  "request_id": "req_01j9x...",
  "task": "parse|extract|classify|split",
  "model_used": "hyperbots_vlm_ocr|hyperbots_vlm_extract",
  "result": { ... },
  "duration_ms": 843,
  "metadata": {
    "pages": 2,
    "file_type": "pdf"
  }
}
```

## Error Handling

All errors return a JSON body with an error object and a standard HTTP status code.

| Status | Error | Description |
|--------|-------|-------------|
| 401 | Unauthorized | Missing or invalid X-API-Key |
| 402 | Payment Required | Insufficient credit balance |
| 413 | Payload Too Large | File exceeds 50 MB limit |
| 422 | Unprocessable Entity | Unsupported file type |
| 429 | Too Many Requests | Rate limit exceeded |
| 503 | Service Unavailable | Inference backend unavailable (circuit open) |

### Error Response Format

```json
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "Your credit balance is too low to process this request."
  }
}
```

## Rate Limits

Rate limits are applied per API key, per minute. Limits scale with your plan tier.

| Tier | Requests / min | Concurrency | Priority weight |
|------|----------------|-------------|-----------------|
| Free | 10 | 1 | 1 |
| Pro | 100 | 10 | 10 |
| Enterprise | Unlimited | 100 | 100 |

## SDKs

### Python SDK

Python 3.9+ · httpx · asyncio support

```bash
pip install hyperapi
```

Available methods:
- `client.parse(file)` - Extract raw OCR text
- `client.extract(file)` - Extract structured entities and line items
- `client.classify(file)` - Categorize document type
- `client.split(file)` - Segment multi-document PDFs
- `client.process(file)` - Combined parse + extract
- `client.upload_document(file)` - S3 presigned upload for large files

### Node.js SDK

Coming soon

```bash
npm install hyperapi
```

## Best Practices

- **S3 Presigned Flow**: Enabled by default in SDK (`use_presigned=True`). Highly recommended for production.
- **Models**: 
  - `hyperbots_vlm_ocr` (Parse, Classify, Split)
  - `hyperbots_vlm_extract` (Extract)
- **File Size**: Maximum 50 MB per file
- **Supported Formats**: PDF, PNG, JPG

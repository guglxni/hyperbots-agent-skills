---
name: hyperbots-api
description: "Integrate with HyperAPI for financial document processing - OCR text extraction, document classification, PDF splitting, and structured data extraction from invoices, receipts, and financial documents. Use when the user needs to parse PDFs, extract text from documents, classify document types, split multi-document PDFs, or extract structured entities like invoice numbers, vendor names, line items. Keywords: hyperapi, hyperbots, document parsing, OCR, PDF processing, invoice extraction, receipt processing, document classification, VLM, vision language model."
license: MIT
metadata:
  author: hyperbots
  version: "2.0.0"
  tags: ["api", "document-processing", "ocr", "financial", "pdf"]
---

# HyperAPI Skill

This skill provides access to HyperAPI, a financial document intelligence platform with four core endpoints for processing invoices, receipts, and financial documents.

## Capabilities

HyperAPI provides four document intelligence endpoints:

| Endpoint | Task | Use Case | Cost | Latency |
|----------|------|----------|------|---------|
| `/v1/parse` | OCR Text Extraction | Extract raw text from any document | $0.05/page | ~1s |
| `/v1/extract` | Structured Data Extraction | Get entities and line items from invoices | $0.08/page | ~2s |
| `/v1/classify` | Document Classification | Categorize documents automatically | $0.03/page | ~0.8s |
| `/v1/split` | PDF Segmentation | Split multi-document PDFs logically | $0.02/page | ~0.5s |

## Base URL

```
https://api.hyperapi.dev
```

## Authentication

All API requests require an `X-API-Key` header:
- Production keys: `hk_live_...`
- Test keys: `hk_test_...`

Generate keys from your dashboard at https://hyperbots.com/dashboard

## Quick Start

### Installation

```bash
pip install hyperapi
```

### Basic Usage

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_your_key_here")

# Parse - extract OCR text
result = client.parse("document.pdf")
print(result["result"]["ocr"])

# Extract - get structured data
result = client.extract("invoice.pdf")
print(result["result"]["entities"])
print(result["result"]["line_items"])

client.close()
```

## API Reference

### Parse Endpoint

Extract raw text from documents using OCR.

**Request:**
```bash
curl -X POST https://api.hyperapi.dev/v1/parse \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "request_id": "req_01j9x...",
  "task": "parse",
  "model_used": "hyperbots_vlm_ocr",
  "result": {
    "ocr": "Invoice\n\nBill To: Acme Corp\nDate: 2024-01-15..."
  },
  "duration_ms": 843,
  "metadata": {
    "pages": 2,
    "file_type": "pdf"
  }
}
```

### Extract Endpoint

Extract structured entities and line items from documents.

**Request:**
```bash
curl -X POST https://api.hyperapi.dev/v1/extract \
  -H "X-API-Key: hk_live_..." \
  -F "file=@invoice.pdf"
```

**Response:**
```json
{
  "status": "success",
  "request_id": "req_01ja0...",
  "task": "extract",
  "model_used": "hyperbots_vlm_extract",
  "result": {
    "entities": {
      "invoice_number": "INV-2024-0042",
      "date": "2024-01-15",
      "due_date": "2024-02-15",
      "vendor_name": "Acme Supplies Ltd",
      "total_amount": "1,250.00",
      "currency": "USD"
    },
    "line_items": [
      {
        "description": "Widget A",
        "quantity": 10,
        "unit_price": "100.00",
        "total": "1,000.00"
      }
    ]
  },
  "duration_ms": 1820,
  "metadata": { "pages": 2 }
}
```

### Classify Endpoint

Categorize documents into financial document types.

**Request:**
```bash
curl -X POST https://api.hyperapi.dev/v1/classify \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "request_id": "req_01j9y...",
  "task": "classify",
  "model_used": "hyperbots_vlm_ocr",
  "result": {
    "label": "invoice",
    "confidence": 0.98,
    "candidates": [
      { "label": "invoice", "confidence": 0.98 },
      { "label": "receipt", "confidence": 0.01 },
      { "label": "contract", "confidence": 0.01 }
    ]
  },
  "duration_ms": 612,
  "metadata": { "pages": 1 }
}
```

### Split Endpoint

Segment multi-document PDFs into individual documents.

**Request:**
```bash
curl -X POST https://api.hyperapi.dev/v1/split \
  -H "X-API-Key: hk_live_..." \
  -F "file=@batch.pdf"
```

**Response:**
```json
{
  "status": "success",
  "request_id": "req_01j9z...",
  "task": "split",
  "model_used": "hyperbots_vlm_ocr",
  "result": {
    "segments": [
      { "document_index": 0, "start_page": 1, "end_page": 3, "type": "invoice" },
      { "document_index": 1, "start_page": 4, "end_page": 5, "type": "receipt" }
    ]
  },
  "duration_ms": 490,
  "metadata": { "pages": 5 }
}
```

## Error Handling

All errors return a JSON body with an error object:

| Status | Code | Description |
|--------|------|-------------|
| 401 | Unauthorized | Missing or invalid X-API-Key |
| 402 | Payment Required | Insufficient credit balance |
| 413 | Payload Too Large | File exceeds 50 MB limit |
| 422 | Unprocessable Entity | Unsupported file type |
| 429 | Too Many Requests | Rate limit exceeded |
| 503 | Service Unavailable | Backend unavailable (circuit open) |

**Error Response:**
```json
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "Your credit balance is too low to process this request."
  }
}
```

## Rate Limits

Rate limits are applied per API key, per minute:

| Tier | Requests/min | Concurrency | Priority |
|------|--------------|-------------|----------|
| Free | 10 | 1 | 1 |
| Pro | 100 | 10 | 10 |
| Enterprise | Unlimited | 100 | 100 |

## SDK Methods

### Python SDK

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_...")

# All available methods
client.parse(file_path)                    # OCR extraction
client.extract(file_path)                  # Structured data extraction
client.classify(file_path)                 # Document classification
client.split(file_path)                    # PDF segmentation
client.process(file_path)                  # Parse + Extract combined
client.upload_document(file_path)          # S3 presigned upload

client.close()
```

### Node.js SDK

Coming soon.

## Best Practices

1. **Use Presigned Uploads**: For files > 50 MB, use `client.upload_document()` which handles S3 presigned URL flow.

2. **Choose the Right Endpoint**:
   - Need raw text? Use `parse`
   - Need structured data? Use `extract`
   - Need to categorize? Use `classify`
   - Have multi-doc PDFs? Use `split`

3. **Handle Rate Limits**: Implement exponential backoff for 429 responses.

4. **Verify File Types**: Supported formats are PDF, PNG, and JPG.

## CLI Usage

A bundled CLI script is available:

```bash
export HYPERAPI_KEY=hk_live_...
python3 scripts/hyperbots_cli.py extract invoice.pdf
```

See [references/api_docs.md](references/api_docs.md) for complete documentation.

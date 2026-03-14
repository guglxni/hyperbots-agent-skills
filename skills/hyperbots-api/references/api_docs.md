# HyperAPI Documentation

**Base URL:** `https://api.hyperapi.dev`

HyperAPI provides four document intelligence endpoints. All requests are authenticated with an API key and accept multipart file uploads.

---

## Authentication

All API requests require an `X-API-Key` header. Keys are prefixed with `hk_live_` for production or `hk_test_` for testing. Generate keys from your dashboard.

```bash
curl -X POST https://api.hyperapi.dev/v1/parse \
  -H "X-API-Key: hk_live_your_key_here" \
  -F "file=@invoice.pdf"
```

---

## Quickstart

Install the Python SDK and run your first API call in under a minute.

### Install

```bash
pip install hyperapi
```

### Parse a document

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_your_key_here")

result = client.parse("invoice.pdf")
print(result["result"]["ocr"])

client.close()
```

---

## Endpoints

### POST /v1/parse

**Parse** - Extract raw text from documents using OCR. Supports PDFs and images. Returns structured markdown with page-level text.

- **Cost:** $0.05/page
- **Latency:** ~1s
- **Model:** hyperbots_vlm_ocr

#### Request Headers

| Header | Description |
|--------|-------------|
| `X-API-Key` | required — your API key |
| `Content-Type` | multipart/form-data |

#### Request Body

| Field | Description |
|-------|-------------|
| `file` | required — PDF, PNG, JPG |

#### cURL Example

```bash
curl -X POST https://api.hyperapi.dev/v1/parse \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

#### Python Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_...")
result = client.parse("document.pdf")
print(result["result"]["ocr"])
```

#### Response (200 OK)

```json
{
  "status": "success",
  "request_id": "req_01j9x...",
  "task": "parse",
  "model_used": "hyperbots_vlm_ocr",
  "result": {
    "ocr": "Invoice\n\nBill To: Acme Corp\nDate: 2024-01-15\n\n..."
  },
  "duration_ms": 843,
  "metadata": {
    "pages": 2,
    "file_type": "pdf"
  }
}
```

---

### POST /v1/classify

**Classify** - Categorize document type automatically. Returns a label and confidence score from a set of financial document classes.

- **Cost:** $0.03/page
- **Latency:** ~0.8s
- **Model:** hyperbots_vlm_ocr

#### Request Headers

| Header | Description |
|--------|-------------|
| `X-API-Key` | required — your API key |
| `Content-Type` | multipart/form-data |

#### Request Body

| Field | Description |
|-------|-------------|
| `file` | required — PDF, PNG, JPG |

#### cURL Example

```bash
curl -X POST https://api.hyperapi.dev/v1/classify \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

#### Python Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_...")
result = client.classify("document.pdf")
print(result["result"]["label"])
```

#### Response (200 OK)

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

---

### POST /v1/split

**Split** - Segment a multi-document PDF into individual logical documents. Returns page ranges for each detected document.

- **Cost:** $0.02/page
- **Latency:** ~0.5s
- **Model:** hyperbots_vlm_ocr

#### Request Headers

| Header | Description |
|--------|-------------|
| `X-API-Key` | required — your API key |
| `Content-Type` | multipart/form-data |

#### Request Body

| Field | Description |
|-------|-------------|
| `file` | required — PDF, PNG, JPG |

#### cURL Example

```bash
curl -X POST https://api.hyperapi.dev/v1/split \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

#### Python Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_...")
result = client.split("document.pdf")
print(result["result"]["segments"])
```

#### Response (200 OK)

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

---

### POST /v1/extract

**Extract** - Extract structured data fields from documents using a vision-language model. Returns named entities and line items.

- **Cost:** $0.08/page
- **Latency:** ~2s
- **Model:** hyperbots_vlm_extract

#### Request Headers

| Header | Description |
|--------|-------------|
| `X-API-Key` | required — your API key |
| `Content-Type` | multipart/form-data |

#### Request Body

| Field | Description |
|-------|-------------|
| `file` | required — PDF, PNG, JPG |

#### cURL Example

```bash
curl -X POST https://api.hyperapi.dev/v1/extract \
  -H "X-API-Key: hk_live_..." \
  -F "file=@document.pdf"
```

#### Python Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="hk_live_...")
result = client.extract("document.pdf")
print(result["result"]["entities"])
```

#### Response (200 OK)

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
      { "description": "Widget A", "quantity": 10, "unit_price": "100.00", "total": "1,000.00" },
      { "description": "Shipping", "quantity": 1, "unit_price": "250.00", "total": "250.00" }
    ]
  },
  "duration_ms": 1820,
  "metadata": { "pages": 2 }
}
```

---

## Errors

All errors return a JSON body with an error object and a standard HTTP status code.

| Status | Code | Description |
|--------|------|-------------|
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

---

## Rate Limits

Rate limits are applied per API key, per minute. Limits scale with your plan tier.

| Tier | Requests / min | Concurrency | Priority weight |
|------|----------------|-------------|-----------------|
| Free | 10 | 1 | 1 |
| Pro | 100 | 10 | 10 |
| Enterprise | Unlimited | 100 | 100 |

---

## SDKs

### Python SDK

Python 3.9+ · httpx · asyncio support

```bash
pip install hyperapi
```

Available methods:
- `client.parse(file)`
- `client.extract(file)`
- `client.classify(file)`
- `client.split(file)`
- `client.process(file)`
- `client.upload_document(file)`

### Node.js SDK

Coming soon

```bash
npm install hyperapi
```

---

## Support

**HyperAPI** - Financial document processing APIs that actually work. Built for developers who ship fast.

- **Product:** APIs, Pricing, Waitlist
- **Resources:** Research, Blog
- **Company:** About, Hyperbots, Contact
- **Legal:** Terms and Conditions

© 2026 Hyperbots. All rights reserved.

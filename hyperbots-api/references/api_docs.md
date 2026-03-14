# HyperAPI (Hyperbots API) Documentation

Financial document processing APIs that actually work. Built for developers who ship fast.

## Base URL
The default production base URL is:
`http://hyperapi-production-12097051.us-east-1.elb.amazonaws.com`
*(Note: Always check for the latest stable endpoint or use the Python SDK which defaults to this).*

## Authentication
All API requests require an `X-API-Key` header.
- Production keys: `hk_live_...`
- Testing keys: `hk_test_...`

```bash
X-API-Key: hk_live_your_key_here
```

## Document Upload Flow (S3 Presigned)
For large files (>50MB) or production use, HyperAPI uses a 3-step upload flow:
1. **Request Upload URL**: `POST /v1/documents/upload` with `filename` and `content_type`.
2. **Direct S3 Upload**: `PUT` the file bytes to the provided `upload_url` with header `x-amz-server-side-encryption: AES256`.
3. **Inference**: Call endpoints (parse, extract, etc.) using the `document_key` returned in Step 1.

The Python SDK handles this automatically when `use_presigned=True` (default).

## Endpoints

### 1. Parse (`POST /v1/parse`)
Extract raw text using OCR. Supports PDFs, PNG, JPG, WEBP, TIFF, GIF.
- **Input**: `file` (multipart) OR `document_key` (JSON/Form).
- **Model**: `hyperbots_vlm_ocr`
- **Output**: Structured markdown with page-level text.

### 2. Extract (`POST /v1/extract`)
Extract structured data fields (entities + line items) using vision-language models.
- **Input**: `file` (multipart) OR `document_key` (JSON/Form).
- **Model**: `hyperbots_vlm_extract`
- **Output**: JSON containing `entities` (invoice_number, date, vendor, total) and `line_items`.

### 3. Classify (`POST /v1/classify`)
Categorize document type automatically.
- **Input**: `file` (multipart) OR `document_key` (JSON/Form).
- **Output**: `label` (e.g., "invoice", "receipt") and confidence scores.

### 4. Split (`POST /v1/split`)
Segment multi-document binders into logical document ranges.
- **Input**: `file` (multipart) OR `document_key` (JSON/Form).
- **Output**: List of `segments` with `start_page`, `end_page`, and detected `type`.

### 5. Upload (`POST /v1/documents/upload`)
Get a presigned S3 URL for direct document upload.
- **Input**: `filename`, `content_type`.
- **Output**: `document_key`, `upload_url`.

## Python SDK (`hyperapi`)

### Installation
```bash
pip install hyperapi
```

### Basic Usage
```python
from hyperapi import HyperAPIClient

# Reads HYPERAPI_KEY from environment or defaults to provided key
client = HyperAPIClient(api_key="hk_live_...")

# Parse (Default uses S3 presigned flow)
result = client.parse("invoice.pdf")
print(result["result"]["ocr"])

# Extract
fields = client.extract("invoice.pdf")
print(fields["result"]["entities"])

# Process (Parse + Extract in one upload)
combined = client.process("invoice.pdf")
print(combined["ocr"])
print(combined["data"])

client.close()
```

## Error Handling
- **401 Unauthorized**: Invalid or missing API key.
- **402 Payment Required**: Insufficient credits.
- **413 Payload Too Large**: File exceeds limit (only for direct multipart).
- **504 Gateway Timeout**: Request timed out (inference can take time).

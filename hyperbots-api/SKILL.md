---
name: hyperbots-api
description: "Financial document processing with HyperAPI (parse, classify, split, extract, process). Use when processing invoices, receipts, or financial PDFs to extract structured data, OCR text, or categorize document types. Supports S3 presigned upload flow for large files."
---

# HyperAPI Skill (by Hyperbots)

This skill provides comprehensive access to HyperAPI financial document intelligence.

## Capabilities

The API supports five main document processing tasks:

1.  **Parse (`/v1/parse`)**: Extract raw text using OCR. Best for searchable PDFs or unstructured text.
2.  **Extract (`/v1/extract`)**: Vision-language extraction of structured fields (vendor, total, line items).
3.  **Classify (`/v1/classify`)**: Automatically categorize financial documents (invoices, receipts, contracts).
4.  **Split (`/v1/split`)**: Logical segmentation of multi-document PDFs.
5.  **Process**: Combined Parse + Extract in one upload.
6.  **Upload**: Presigned S3 flow for files > 50 MB.

## Workflow

### 1. Prerequisites

-   **API Key**: Requires `X-API-Key` header (e.g. `hk_live_...`).
-   **SDK**: Use the `hyperapi` Python package.

### 2. Implementation Guide

For a detailed reference of all endpoints and SDK methods, see [references/api_docs.md](references/api_docs.md).

#### Python SDK Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="your_key_here")

# Process: Parse + Extract in one call
result = client.process("invoice.pdf")
print(result["ocr"])
print(result["data"]["entities"])

# Extraction only
entities = client.extract("receipt.png")

# Parsing only
text = client.parse("document.pdf")
```

#### CLI Interaction

A bundled script is available: `scripts/hyperbots_cli.py`.

```bash
export HYPERAPI_KEY=hk_live_...
python3 <skill-path>/scripts/hyperbots_cli.py extract invoice.pdf
```

## Error Handling

-   **401**: Missing/Invalid Key.
-   **402**: Insufficient credits.
-   **504**: Timeout (use 120s+).

## Best Practices

-   **S3 Presigned Flow**: Enabled by default in SDK (`use_presigned=True`). Highly recommended for production.
-   **Models**: 
    - `hyperbots_vlm_ocr` (Parse, Classify, Split)
    - `hyperbots_vlm_extract` (Extract)

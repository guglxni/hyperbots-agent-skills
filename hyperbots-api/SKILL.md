---
name: hyperbots-api
description: "Financial document processing with Hyperbots APIs (parse, classify, split, extract). Use when processing invoices, receipts, or financial PDFs to extract structured data, OCR text, or categorize document types."
---

# Hyperbots API Skill

This skill provides comprehensive access to Hyperbots financial document intelligence APIs.

## Capabilities

The API supports four main document processing tasks:

1.  **Parse (`/v1/parse`)**: Extract raw text using OCR. Best for searchable PDFs or unstructured text.
2.  **Classify (`/v1/classify`)**: Automatically categorize financial documents (invoices, receipts, contracts).
3.  **Split (`/v1/split`)**: Logical segmentation of multi-document PDFs (e.g., separating multiple invoices in one file).
4.  **Extract (`/v1/extract`)**: Vision-language extraction of structured fields (vendor, total, line items).

## Workflow

### 1. Prerequisites

-   **API Key**: Requires `X-API-Key` header (get from dashboard). Keys start with `hk_live_` or `hk_test_`.
-   **SDK**: Use the `hyperapi` Python package if available.

### 2. Implementation Guide

For a detailed reference of all endpoints, parameters, and response schemas, see [references/api_docs.md](references/api_docs.md).

#### Python SDK Example

```python
from hyperapi import HyperAPIClient

client = HyperAPIClient(api_key="your_key_here")

# Parse: OCR raw text
ocr_result = client.parse("document.pdf")

# Extract: Structured fields
entities = client.extract("invoice.pdf")
print(entities["result"]["entities"]) # Vendor, total, items

# Classify: Document type
doc_type = client.classify("scan.pdf")

# Split: Page segments
segments = client.split("bundle.pdf")
```

#### CLI Interaction

A bundled script is available in the skill: `scripts/hyperbots_cli.py`.

```bash
# Set API Key
export HYPERBOTS_API_KEY=hk_live_...

# Run a task
python3 <skill-path>/scripts/hyperbots_cli.py extract invoice.pdf
```

## Error Handling

-   **401**: Missing/Invalid Key.
-   **402**: Insufficient credits.
-   **413**: File > 50 MB.
-   **429**: Rate limit (Free: 10/min, Pro: 100/min).

For more details on error codes and rate limits, consult the [full docs](references/api_docs.md).

## Best Practices

-   **Extraction**: Prefer `extract` for invoices/receipts where you need structured JSON.
-   **OCR**: Use `parse` for high-fidelity text extraction in Markdown.
-   **File Types**: Supports PDF, PNG, JPG.
-   **Multipart**: All requests must be `multipart/form-data`.

# HyperAPI Skill (by Hyperbots)

Comprehensive agent skill for interacting with [HyperAPI](https://apis.hyperbots.com/).

## Features
- **Parse**: OCR raw text with page-level accuracy.
- **Extract**: Structured financial data (entities, line items).
- **Classify**: Document type detection (invoices, receipts, etc.).
- **Split**: Logical document segmentation.
- **Process**: Unified parse/extract workflow.
- **S3 Presigned Flow**: Optimized for files > 50MB.

## Installation
```bash
npx skills add guglxni/hyperbots-agent-skills@hyperbots-api
```

## SDK Usage
```python
from hyperapi import HyperAPIClient
client = HyperAPIClient(api_key="your_key")
result = client.process("document.pdf")
```

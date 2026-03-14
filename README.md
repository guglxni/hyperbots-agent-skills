# Hyperbots Agent Skills

A collection of Gemini CLI agent skills for interacting with [Hyperbots](https://apis.hyperbots.com/) Financial Document Intelligence APIs.

## Included Skills

### 1. `hyperbots-api`
Comprehensive skill for document processing:
- **Parse**: OCR raw text from PDFs and images.
- **Classify**: Categorize documents (invoices, receipts, contracts).
- **Split**: Segment multi-document PDFs.
- **Extract**: Vision-language extraction of structured financial fields.

## Installation

To install the `hyperbots-api` skill in your Gemini CLI:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/hyperbots-agent-skills.git

# Install the skill
gemini skills install hyperbots-agent-skills/hyperbots-api.skill --scope user

# Reload your agent
# (Run this inside your interactive gemini-cli session)
/skills reload
```

## Usage

Once installed, the agent will automatically trigger this skill when you ask about processing financial documents. You can also use the bundled CLI script:

```bash
export HYPERBOTS_API_KEY=your_key_here
python3 hyperbots-api/scripts/hyperbots_cli.py extract invoice.pdf
```

## Development

This repository includes the raw scraping scripts used to generate these skills using `Scrapling` and `Playwright`.

- `scrape_docs_raw.py`: Playwright scraper for dynamic documentation.
- `hyperbots-api/`: The raw skill source directory.
- `hyperbots-api.skill`: The packaged distributable skill.

## License
MIT

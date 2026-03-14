# Hyperbots Agent Skills

A collection of agent skills for [Hyperbots](https://apis.hyperbots.com/) Document Intelligence APIs, built for the [Agent Skills](https://agentskills.io) standard.

## Included Skills

### 1. `hyperbots-api`
Comprehensive skill for financial document intelligence:
- **Parse**: High-fidelity OCR text extraction.
- **Classify**: Automated document categorization (invoices, receipts, etc.).
- **Split**: Logical multi-document segmentation.
- **Extract**: Vision-language structured data extraction.
- **Process**: Unified Parse + Extract workflow.

## Installation

Install the `hyperbots-api` skill using the [Skills CLI](https://github.com/anthropics/skills):

```bash
npx skills add guglxni/hyperbots-agent-skills --skill hyperbots-api
```

Alternatively, if you're using **Gemini CLI**, you can install the packaged version:

```bash
gemini skills install https://github.com/guglxni/hyperbots-agent-skills/raw/master/skills/hyperbots-api/hyperbots-api.skill --scope user
```

*(Note: Package version must be present in the skill directory. We recommend the `npx skills add` command for direct source installation).*

## Usage

Once installed, your agent (Claude Code, Gemini CLI, etc.) will automatically trigger this skill when you ask about processing financial documents.

### Manual CLI Usage
The skill includes a standalone CLI script for direct interaction:

```bash
export HYPERAPI_KEY=your_key_here
python3 skills/hyperbots-api/scripts/hyperbots_cli.py extract invoice.pdf
```

## Development

This repository follows the standardized approach for agent skills. Each skill is self-contained in its own folder under `skills/` with a `SKILL.md` file.

- `skills/hyperbots-api/`: The main document intelligence skill.
- `metadata.json`: Standardized metadata for the skill.

## License
MIT

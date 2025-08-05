# PDF Integration Guide for VS Code

This guide explains how to effectively reference and work with PDF documents in VS Code, making them as accessible as markdown files.

## 🚀 Quick Setup

1. **Install PDF Tools**:
   ```bash
   chmod +x scripts/setup/install-pdf-tools.sh
   ./scripts/setup/install-pdf-tools.sh
   ```

2. **Install VS Code Extensions**:
   ```bash
   # Install recommended extensions
   code --install-extension tomoki1207.pdf
   code --install-extension mathematic.vscode-pdf
   code --install-extension yzhang.markdown-all-in-one
   ```

3. **Reload VS Code** to apply the new settings.

## 📚 Available PDF Tools

### VS Code Extensions

| Extension | Purpose | Features |
|-----------|---------|----------|
| `tomoki1207.pdf` | PDF Viewer | View PDFs directly in VS Code |
| `mathematic.vscode-pdf` | Enhanced PDF Support | Advanced PDF viewing with annotations |
| `analytic-signal.preview-pdf` | PDF Preview | Quick PDF preview in sidebar |

### Command Line Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| `pdftotext` | Extract text from PDFs | `pdftotext document.pdf document.txt` |
| `pdfinfo` | Get PDF metadata | `pdfinfo document.pdf` |
| `pdfgrep` | Search text in PDFs | `pdfgrep "search term" *.pdf` |
| `pandoc` | Convert between formats | `pandoc document.pdf -o document.md` |

### Custom Python Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| `create_pdf_summary.py` | Generate PDF summaries | `python3 tools/pdf-conversion/create_pdf_summary.py file.pdf` |
| `validate_links.py` | Validate PDF links | `python3 tools/maintenance/validate_links.py docs/` |
| `generate_doc_index.py` | Create documentation index | `python3 tools/maintenance/generate_doc_index.py docs/` |

## 🔍 How to Reference PDFs

### 1. Direct PDF Links in Markdown

```markdown
# Reference PDF directly
[Technical Guide](docs/assets/pdfs/technical-guide.pdf)

# Link to specific page (if supported by viewer)
[Setup Instructions - Page 15](docs/assets/pdfs/technical-guide.pdf#page=15)
```

### 2. PDF Summaries

Generate searchable summaries of PDFs:

```bash
# Create a summary
python3 tools/pdf-conversion/create_pdf_summary.py docs/assets/pdfs/technical-guide.pdf

# This creates:
# - technical-guide-summary.md (structured summary)
# - Links to original PDF
# - Table of contents
# - Key sections overview
```

### 3. Converted Markdown Versions

```markdown
# Link to both PDF and markdown versions
- 📄 [Original PDF](docs/assets/pdfs/deployment-guide.pdf)
- 📝 [Markdown Version](docs/assets/pdfs/deployment-guide.md)
```

## 🛠️ VS Code Integration Features

### File Nesting

PDFs and their related files are automatically nested in the explorer:

```
📁 docs/assets/pdfs/
├── 📄 technical-guide.pdf
├── 📝 technical-guide.md (nested under PDF)
└── 📋 technical-guide-summary.md (nested under PDF)
```

### Search Integration

- **Ctrl+F**: Search within open PDF
- **Ctrl+Shift+F**: Search across all files (includes PDF text if indexed)
- **Command Palette**: PDF-specific commands

### Tasks Integration

Use VS Code tasks (Ctrl+Shift+P → "Tasks: Run Task"):

- **Convert PDF to Markdown**: Converts selected PDF to markdown
- **Extract PDF Text**: Extracts plain text from PDF
- **Create PDF Summary**: Generates structured summary
- **Validate Documentation Links**: Checks all PDF references

## 📖 Best Practices

### 1. Organize PDFs

```
docs/
├── assets/
│   └── pdfs/
│       ├── technical-guide.pdf
│       ├── technical-guide.md
│       └── technical-guide-summary.md
├── guides/
│   └── user-guide.md (references PDFs)
└── INDEX.md (generated index)
```

### 2. Create Summaries for Large PDFs

```bash
# For documents > 50 pages, create summaries
python3 tools/pdf-conversion/create_pdf_summary.py large-document.pdf
```

### 3. Use Consistent Naming

```
document-name.pdf           # Original PDF
document-name.md           # Full markdown conversion
document-name-summary.md   # Quick reference summary
```

### 4. Link Strategically

```markdown
## Instructions

For complete details, see the [Technical Deployment Guide](assets/pdfs/technical-guide.pdf).

Quick reference: [Quick Summary](assets/pdfs/technical-guide-summary.md#overview-section)
```

## 🔧 Advanced Features

### PDF Search with Context

```bash
# Search with line numbers and context
pdfgrep -n -C 2 "configuration" docs/**/*.pdf

# Search multiple terms
pdfgrep -e "install" -e "configure" docs/**/*.pdf
```

### Batch Processing

```bash
# Process all PDFs in a directory
find docs/ -name "*.pdf" -exec python3 tools/pdf-conversion/create_pdf_summary.py {} \;

# Validate all documentation
python3 tools/maintenance/validate_links.py docs/ --pdf-only
```

### Custom VS Code Snippets

Add to your VS Code snippets:

```json
{
  "PDF Reference": {
    "prefix": "pdfref",
    "body": [
      "## ${1:Section Title}",
      "",
      "📄 **Reference**: [${2:Document Title}](${3:path/to/document.pdf})",
      "",
      "📝 **Quick Reference**: [${2:Document Title} Summary](${3:path/to/document}-summary.md)",
      "",
      "${4:Description}"
    ],
    "description": "Insert PDF reference with summary link"
  }
}
```

## 🚨 Troubleshooting

### PDF Not Opening in VS Code

1. Check if PDF extension is installed:
   ```bash
   code --list-extensions | grep pdf
   ```

2. Verify file association in settings:
   ```json
   "workbench.editorAssociations": {
     "*.pdf": "pdf.preview"
   }
   ```

### Search Not Finding PDF Content

1. Install `pdfgrep`:
   ```bash
   sudo apt install pdfgrep  # Ubuntu/Debian
   brew install pdfgrep      # macOS
   ```

2. Use command line search:
   ```bash
   pdfgrep "search term" docs/**/*.pdf
   ```

### PDF Tools Not Working

1. Run the setup script:
   ```bash
   ./scripts/setup/install-pdf-tools.sh
   ```

2. Check tool availability:
   ```bash
   which pdftotext pdfinfo pdfgrep pandoc
   ```

## 📊 Monitoring and Maintenance

### Regular Tasks

```bash
# Weekly: Update documentation index
python3 tools/maintenance/generate_doc_index.py docs/

# Monthly: Validate all links
python3 tools/maintenance/validate_links.py docs/

# As needed: Create summaries for new PDFs
find docs/ -name "*.pdf" -newer docs/INDEX.md -exec python3 tools/pdf-conversion/create_pdf_summary.py {} \;
```

### Automation with Git Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate documentation before commit
python3 tools/maintenance/validate_links.py docs/ --pdf-only
```

## 🎯 Integration Examples

### In Setup Guides

```markdown
# System Setup

## Prerequisites

Before starting, review these documents:

1. 📄 [Technical Guide](assets/pdfs/technical-guide.pdf) - Complete reference
2. 📝 [Quick Summary](assets/pdfs/technical-guide-summary.md) - Key steps only
3. 📋 [Configuration Guide](assets/pdfs/config-guide.pdf#page=15) - Page 15 specifically

## Step 1: System Configuration

Follow the instructions in [Configuration Guide](assets/pdfs/config-guide.pdf), specifically:

- Section 3.2: System Configuration
- Section 4.1: Security Setup
- Appendix A: Troubleshooting
```

### In README Files

```markdown
## 📚 Documentation

### User Guides
- 🚀 [Complete User Guide](docs/guides/user-guide.md)
- 📄 [Official Documentation](docs/assets/pdfs/technical-guide.pdf)
- 📝 [Quick Reference](docs/assets/pdfs/technical-guide-summary.md)

### Browse All Documentation
- 📖 [Documentation Index](docs/INDEX.md) - Complete file listing
- 🔍 [Search Tips](#search-integration)
```

## 🎉 Success Metrics

After setup, you should be able to:

- ✅ Open PDFs directly in VS Code
- ✅ Search PDF content from command line
- ✅ Generate summaries of new PDFs
- ✅ Validate all PDF links in documentation
- ✅ Navigate between PDF and markdown versions seamlessly

---

*This integration makes PDFs as accessible as markdown files in your development workflow!*
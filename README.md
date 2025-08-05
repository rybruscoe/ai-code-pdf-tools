# PDF Tools for VS Code

A comprehensive toolkit for integrating PDF documents into VS Code workflows, making PDFs as accessible as markdown files.

## 🚀 Features

- **VS Code Integration**: Extensions, settings, and tasks for seamless PDF handling
- **PDF Processing**: Convert, summarize, and extract content from PDFs
- **Documentation Tools**: Validate links, generate indexes, and maintain documentation
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Command Line Interface**: Powerful CLI tools for automation

## 📦 Installation

### Quick Setup
```bash
# Clone the repository
git clone git@github.com:rybruscoe/kilo-code-pdf-tools.git
cd kilo-code-pdf-tools

# Run the setup script
./scripts/install-pdf-tools.sh

# Install VS Code extensions
code --install-extension tomoki1207.pdf
code --install-extension mathematic.vscode-pdf
```

### As Git Submodule
```bash
# Add as submodule to your project
git submodule add git@github.com:rybruscoe/kilo-code-pdf-tools.git pdf-tools

# Initialize and update
git submodule update --init --recursive

# Setup in your project
./pdf-tools/scripts/install-pdf-tools.sh
```

## 🛠️ Tools

### PDF Processing
- **`pdf_summary.py`** - Generate structured summaries of PDF documents
- **`pdf_converter.py`** - Convert PDFs to various formats (markdown, text, etc.)
- **`pdf_metadata.py`** - Extract and manage PDF metadata

### Documentation Management
- **`validate_links.py`** - Validate all documentation links including PDFs
- **`generate_doc_index.py`** - Create comprehensive documentation indexes
- **`doc_maintenance.py`** - Automated documentation maintenance tasks

### VS Code Integration
- **Extensions configuration** - Recommended extensions for PDF work
- **Settings and tasks** - Optimized VS Code configuration
- **Snippets and shortcuts** - Productivity enhancements

## 📖 Usage

### Generate PDF Summary
```bash
python3 tools/pdf_summary.py document.pdf
# Creates: document-summary.md with structured overview
```

### Convert PDF to Markdown
```bash
python3 tools/pdf_converter.py document.pdf --format markdown
# Creates: document.md with full content
```

### Validate Documentation
```bash
python3 tools/validate_links.py docs/ --include-pdfs
# Checks all links and PDF references
```

### Generate Documentation Index
```bash
python3 tools/generate_doc_index.py docs/
# Creates: docs/INDEX.md with complete file listing
```

## 🔧 Configuration

### VS Code Setup
The toolkit includes pre-configured VS Code settings:

- **Extensions**: PDF viewers, markdown enhancers, documentation tools
- **Settings**: File associations, search configuration, spell checking
- **Tasks**: Common PDF operations accessible via Command Palette
- **Snippets**: Quick insertion of PDF references and documentation blocks

### Command Line Tools
Required system packages (installed automatically):

- **poppler-utils**: PDF text extraction and metadata
- **pdfgrep**: Search text within PDFs
- **pandoc**: Document format conversion
- **python3**: Runtime for custom tools

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Examples](docs/USAGE.md) - Common workflows and examples
- [VS Code Integration](docs/VSCODE.md) - Complete VS Code setup guide
- [API Reference](docs/API.md) - Tool APIs and configuration options
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

*Making PDFs as accessible as markdown files in your development workflow.*
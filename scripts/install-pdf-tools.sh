#!/bin/bash
# PDF Tools Installation Script
# Installs necessary tools for PDF integration in VS Code

set -e

echo "🔧 Installing PDF Tools for VS Code Integration"
echo "=============================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "📦 Installing packages via apt-get..."
        sudo apt-get update
        sudo apt-get install -y \
            poppler-utils \
            pdfgrep \
            pandoc \
            python3-pip \
            python3-venv
    elif command -v yum &> /dev/null; then
        echo "📦 Installing packages via yum..."
        sudo yum install -y \
            poppler-utils \
            pdfgrep \
            pandoc \
            python3-pip
    elif command -v dnf &> /dev/null; then
        echo "📦 Installing packages via dnf..."
        sudo dnf install -y \
            poppler-utils \
            pdfgrep \
            pandoc \
            python3-pip
    elif command -v pacman &> /dev/null; then
        echo "📦 Installing packages via pacman..."
        sudo pacman -S --noconfirm \
            poppler \
            pdfgrep \
            pandoc \
            python-pip
    else
        echo "❌ Unsupported Linux distribution"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        echo "📦 Installing packages via Homebrew..."
        brew install \
            poppler \
            pdfgrep \
            pandoc \
            python3
    else
        echo "❌ Homebrew not found. Please install Homebrew first."
        exit 1
    fi
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo ""
echo "🐍 Setting up Python environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install \
    PyPDF2 \
    pdfplumber \
    markdown \
    pyyaml \
    requests

echo ""
echo "🔍 Verifying installations..."

# Verify installations
echo "Checking installed tools:"

if command -v pdftotext &> /dev/null; then
    echo "✅ pdftotext: $(pdftotext -v 2>&1 | head -1)"
else
    echo "❌ pdftotext not found"
fi

if command -v pdfinfo &> /dev/null; then
    echo "✅ pdfinfo: $(pdfinfo -v 2>&1 | head -1)"
else
    echo "❌ pdfinfo not found"
fi

if command -v pdfgrep &> /dev/null; then
    echo "✅ pdfgrep: $(pdfgrep --version | head -1)"
else
    echo "❌ pdfgrep not found"
fi

if command -v pandoc &> /dev/null; then
    echo "✅ pandoc: $(pandoc --version | head -1)"
else
    echo "❌ pandoc not found"
fi

echo ""
echo "🎯 Making tools executable..."
chmod +x tools/pdf_summary.py
chmod +x tools/validate_links.py
chmod +x tools/generate_doc_index.py

echo ""
echo "📚 Testing PDF tools..."

# Test with any PDF if available
PDF_FILE=$(find . -name "*.pdf" | head -1)
if [ -n "$PDF_FILE" ]; then
    echo "Testing with: $PDF_FILE"
    
    # Test pdfinfo
    echo "📄 PDF Info:"
    pdfinfo "$PDF_FILE" | head -5
    
    # Test pdftotext
    echo "📝 Text extraction (first 100 chars):"
    pdftotext "$PDF_FILE" - | head -c 100
    echo "..."
    
    echo ""
    echo "🔧 Testing custom tools..."
    
    # Test our custom PDF summary tool
    if python3 tools/pdf_summary.py "$PDF_FILE" --help &> /dev/null; then
        echo "✅ PDF summary tool is working"
    else
        echo "❌ PDF summary tool has issues"
    fi
else
    echo "ℹ️  No PDF files found for testing"
fi

echo ""
echo "✅ PDF Tools Installation Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Install VS Code extensions: code --install-extension tomoki1207.pdf"
echo "2. Copy vscode/ configuration to your project's .vscode/ directory"
echo "3. Reload VS Code to apply settings"
echo "4. Try opening a PDF file in VS Code"
echo ""
echo "🛠️  Available Commands:"
echo "• Generate PDF summary: python3 tools/pdf_summary.py <pdf-file>"
echo "• Validate links: python3 tools/validate_links.py docs/"
echo "• Generate doc index: python3 tools/generate_doc_index.py docs/"
echo "• Search in PDFs: pdfgrep 'search term' **/*.pdf"
echo "• Extract PDF text: pdftotext document.pdf document.txt"
echo ""
echo "📖 For more information, see the README.md"
#!/bin/bash

# VS Code PDF Tools Setup Script
# This script sets up VS Code configuration for PDF integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VSCODE_DIR="$PROJECT_ROOT/.vscode"

echo "Setting up VS Code configuration for PDF tools..."

# Create .vscode directory if it doesn't exist
if [ ! -d "$VSCODE_DIR" ]; then
    echo "Creating .vscode directory..."
    mkdir -p "$VSCODE_DIR"
fi

# Copy VS Code configuration files
echo "Copying VS Code configuration files..."

if [ -f "$PROJECT_ROOT/vscode/extensions.json" ]; then
    cp "$PROJECT_ROOT/vscode/extensions.json" "$VSCODE_DIR/"
    echo "✓ Copied extensions.json"
else
    echo "⚠ Warning: extensions.json not found"
fi

if [ -f "$PROJECT_ROOT/vscode/settings.json" ]; then
    # Check if settings.json already exists
    if [ -f "$VSCODE_DIR/settings.json" ]; then
        echo "⚠ Warning: settings.json already exists. Creating backup..."
        cp "$VSCODE_DIR/settings.json" "$VSCODE_DIR/settings.json.backup"
    fi
    cp "$PROJECT_ROOT/vscode/settings.json" "$VSCODE_DIR/"
    echo "✓ Copied settings.json"
else
    echo "⚠ Warning: settings.json not found"
fi

if [ -f "$PROJECT_ROOT/vscode/tasks.json" ]; then
    # Check if tasks.json already exists
    if [ -f "$VSCODE_DIR/tasks.json" ]; then
        echo "⚠ Warning: tasks.json already exists. Creating backup..."
        cp "$VSCODE_DIR/tasks.json" "$VSCODE_DIR/tasks.json.backup"
    fi
    cp "$PROJECT_ROOT/vscode/tasks.json" "$VSCODE_DIR/"
    echo "✓ Copied tasks.json"
else
    echo "⚠ Warning: tasks.json not found"
fi

echo ""
echo "VS Code configuration setup complete!"
echo ""
echo "Next steps:"
echo "1. Restart VS Code to apply the new configuration"
echo "2. Install recommended extensions when prompted"
echo "3. Use Ctrl+Shift+P (Cmd+Shift+P on Mac) to access PDF tasks"
echo ""
echo "Available tasks:"
echo "- PDF Summary: Generate summary of PDF files"
echo "- Validate Links: Check links in documentation"
echo "- Generate Documentation Index: Create doc index"
echo "- Convert PDF to Text/Markdown: Convert PDF files"
echo "- Search PDF Content: Search within PDF files"
echo "- PDF Info: Display PDF metadata"
echo ""
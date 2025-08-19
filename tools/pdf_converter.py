#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF documents to full markdown format for better readability and editing.
"""

import sys
import os
import argparse
from pathlib import Path
import subprocess
import json
from datetime import datetime

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, '-'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    except FileNotFoundError:
        print("pdftotext not found. Install poppler-utils: sudo apt install poppler-utils")
        return None

def extract_pdf_metadata(pdf_path):
    """Extract metadata from PDF using pdfinfo."""
    try:
        result = subprocess.run(
            ['pdfinfo', pdf_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        metadata = {}
        for line in result.stdout.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        return metadata
    except subprocess.CalledProcessError as e:
        print(f"Error extracting metadata from PDF: {e}")
        return {}
    except FileNotFoundError:
        print("pdfinfo not found. Install poppler-utils: sudo apt install poppler-utils")
        return {}

def convert_to_markdown(pdf_path, text_content, metadata):
    """Convert PDF text content to markdown format."""
    pdf_name = Path(pdf_path).stem
    markdown_path = Path(pdf_path).parent / f"{pdf_name}.md"
    
    # Process text content
    lines = text_content.split('\n')
    markdown_content = []
    
    # Add header with metadata
    markdown_content.append(f"# {metadata.get('Title', pdf_name)}")
    markdown_content.append("")
    markdown_content.append("## Document Information")
    markdown_content.append("")
    markdown_content.append(f"- **Source**: [{Path(pdf_path).name}]({Path(pdf_path).name})")
    markdown_content.append(f"- **Converted**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    markdown_content.append(f"- **Author**: {metadata.get('Author', 'N/A')}")
    markdown_content.append(f"- **Subject**: {metadata.get('Subject', 'N/A')}")
    markdown_content.append(f"- **Creator**: {metadata.get('Creator', 'N/A')}")
    markdown_content.append(f"- **Pages**: {metadata.get('Pages', 'N/A')}")
    markdown_content.append(f"- **Creation Date**: {metadata.get('CreationDate', 'N/A')}")
    markdown_content.append("")
    markdown_content.append("---")
    markdown_content.append("")
    
    # Process content line by line
    for line in lines:
        line = line.rstrip()
        
        # Skip empty lines at the beginning
        if not line and not markdown_content[-1].strip():
            continue
            
        # Detect headings (simple heuristics)
        if line.isupper() and len(line) > 5 and len(line.split()) < 10:
            # Likely a heading
            markdown_content.append(f"## {line.title()}")
        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
            # Numbered list item
            markdown_content.append(line)
        elif line.startswith(('•', '-', '*')):
            # Bullet point
            markdown_content.append(line)
        elif line.startswith('   ') and line.strip():
            # Indented text (code block or continuation)
            markdown_content.append(f"    {line.strip()}")
        elif not line:
            # Empty line
            markdown_content.append("")
        else:
            # Regular paragraph
            markdown_content.append(line)
    
    # Clean up multiple empty lines
    cleaned_content = []
    prev_empty = False
    for line in markdown_content:
        if line == "":
            if not prev_empty:
                cleaned_content.append(line)
            prev_empty = True
        else:
            cleaned_content.append(line)
            prev_empty = False
    
    # Join content
    final_content = '\n'.join(cleaned_content)
    
    # Write markdown file
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return markdown_path

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to markdown format')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Output directory (default: same as PDF)')
    parser.add_argument('--format', choices=['markdown', 'md'], default='markdown',
                       help='Output format (default: markdown)')
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Converting PDF: {pdf_path}")
    
    # Extract text content
    print("Extracting text content...")
    text_content = extract_pdf_text(pdf_path)
    if not text_content:
        print("Failed to extract text content")
        sys.exit(1)
    
    # Extract metadata
    print("Extracting metadata...")
    metadata = extract_pdf_metadata(pdf_path)
    
    # Convert to markdown
    print("Converting to markdown...")
    markdown_path = convert_to_markdown(pdf_path, text_content, metadata)
    
    print(f"Markdown file created: {markdown_path}")
    print("Conversion complete!")

if __name__ == '__main__':
    main()
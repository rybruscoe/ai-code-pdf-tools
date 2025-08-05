#!/usr/bin/env python3
"""
PDF Summary Generator
Creates structured summaries of PDF documents for better referencing in VS Code.
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

def create_summary_markdown(pdf_path, text_content, metadata):
    """Create a structured markdown summary of the PDF."""
    pdf_name = Path(pdf_path).stem
    summary_path = Path(pdf_path).parent / f"{pdf_name}-summary.md"
    
    # Extract key sections (basic heuristic)
    lines = text_content.split('\n')
    sections = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect potential headings (all caps, or starting with numbers/bullets)
        if (line.isupper() and len(line) > 5) or \
           (line.startswith(('1.', '2.', '3.', '4.', '5.', '•', '-', '*'))) or \
           ('Table of Contents' in line) or \
           ('Chapter' in line) or \
           ('Section' in line):
            if current_section:
                sections.append(current_section)
            current_section = {'title': line, 'content': []}
        elif current_section:
            current_section['content'].append(line)
    
    if current_section:
        sections.append(current_section)
    
    # Generate markdown summary
    summary_content = f"""# PDF Summary: {pdf_name}

## Document Information

- **File**: [`{Path(pdf_path).name}`]({Path(pdf_path).name})
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Title**: {metadata.get('Title', 'N/A')}
- **Author**: {metadata.get('Author', 'N/A')}
- **Subject**: {metadata.get('Subject', 'N/A')}
- **Creator**: {metadata.get('Creator', 'N/A')}
- **Pages**: {metadata.get('Pages', 'N/A')}
- **Creation Date**: {metadata.get('CreationDate', 'N/A')}

## Quick Reference Links

- [📄 View Original PDF]({Path(pdf_path).name})
- [📝 Full Markdown Version]({pdf_name}.md)
- [🔍 Search in PDF](#search-tips)

## Document Structure

"""
    
    # Add table of contents
    if sections:
        summary_content += "### Table of Contents\n\n"
        for i, section in enumerate(sections[:20], 1):  # Limit to first 20 sections
            title = section['title'][:100]  # Truncate long titles
            summary_content += f"{i}. [{title}](#{title.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('(', '').replace(')', '')})\n"
        
        summary_content += "\n## Key Sections\n\n"
        
        # Add section summaries
        for section in sections[:10]:  # Limit to first 10 sections for summary
            title = section['title']
            content_preview = ' '.join(section['content'][:3])[:200] + "..." if section['content'] else "No content"
            
            summary_content += f"### {title}\n\n"
            summary_content += f"{content_preview}\n\n"
    
    # Add search tips
    summary_content += """## Search Tips

### VS Code PDF Search
1. Open the PDF in VS Code using the PDF extension
2. Use `Ctrl+F` to search within the PDF
3. Use `Ctrl+Shift+F` to search across all files including PDFs

### Command Line Search
```bash
# Search for text in PDF
pdfgrep "search term" "{Path(pdf_path).name}"

# Search with context
pdfgrep -n -C 2 "search term" "{Path(pdf_path).name}"
```

### Cross-Reference with Markdown
- This PDF has been converted to markdown: [`{pdf_name}.md`]({pdf_name}.md)
- Use markdown for better searchability and linking

---
*This summary was auto-generated from the PDF content. For complete information, refer to the original PDF document.*
"""
    
    # Write summary file
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    return summary_path

def main():
    parser = argparse.ArgumentParser(description='Create a structured summary of a PDF document')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Output directory (default: same as PDF)')
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    print(f"Processing PDF: {pdf_path}")
    
    # Extract text content
    print("Extracting text content...")
    text_content = extract_pdf_text(pdf_path)
    if not text_content:
        print("Failed to extract text content")
        sys.exit(1)
    
    # Extract metadata
    print("Extracting metadata...")
    metadata = extract_pdf_metadata(pdf_path)
    
    # Create summary
    print("Creating summary...")
    summary_path = create_summary_markdown(pdf_path, text_content, metadata)
    
    print(f"Summary created: {summary_path}")
    print(f"You can now reference this PDF easily in VS Code!")

if __name__ == '__main__':
    main()
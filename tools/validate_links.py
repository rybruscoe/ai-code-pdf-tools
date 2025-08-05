#!/usr/bin/env python3
"""
Documentation Link Validator
Validates all links in markdown files including PDF references.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from urllib.parse import urlparse
import subprocess

def find_markdown_files(directory):
    """Find all markdown files in directory."""
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files

def extract_links(content):
    """Extract all links from markdown content."""
    # Markdown link pattern: [text](url)
    markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    
    # Reference link pattern: [text]: url
    reference_links = re.findall(r'^\[([^\]]+)\]:\s*(.+)$', content, re.MULTILINE)
    
    # HTML link pattern: <a href="url">
    html_links = re.findall(r'<a\s+href=["\']([^"\']+)["\']', content)
    
    all_links = []
    
    # Process markdown links
    for text, url in markdown_links:
        all_links.append({'type': 'markdown', 'text': text, 'url': url})
    
    # Process reference links
    for text, url in reference_links:
        all_links.append({'type': 'reference', 'text': text, 'url': url})
    
    # Process HTML links
    for url in html_links:
        all_links.append({'type': 'html', 'text': '', 'url': url})
    
    return all_links

def validate_local_file(file_path, base_dir):
    """Validate if local file exists."""
    if file_path.startswith('#'):
        return True, "Anchor link"
    
    if file_path.startswith('http'):
        return True, "External URL (not validated)"
    
    # Handle relative paths
    if not file_path.startswith('/'):
        full_path = base_dir / file_path
    else:
        full_path = Path(file_path)
    
    # Resolve relative paths
    try:
        resolved_path = full_path.resolve()
        if resolved_path.exists():
            return True, f"File exists: {resolved_path}"
        else:
            return False, f"File not found: {resolved_path}"
    except Exception as e:
        return False, f"Error resolving path: {e}"

def validate_pdf_accessibility(pdf_path):
    """Check if PDF can be opened and read."""
    try:
        # Try to extract first page to verify PDF is readable
        result = subprocess.run(
            ['pdfinfo', str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "PDF is readable"
        else:
            return False, f"PDF validation failed: {result.stderr}"
    except subprocess.TimeoutExpired:
        return False, "PDF validation timed out"
    except FileNotFoundError:
        return True, "pdfinfo not available (install poppler-utils for PDF validation)"
    except Exception as e:
        return False, f"PDF validation error: {e}"

def validate_links_in_file(file_path):
    """Validate all links in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{'error': f"Could not read file: {e}"}]
    
    links = extract_links(content)
    results = []
    
    for link in links:
        url = link['url']
        text = link['text']
        link_type = link['type']
        
        # Skip mailto and other special protocols
        if url.startswith(('mailto:', 'tel:', 'javascript:')):
            results.append({
                'url': url,
                'text': text,
                'type': link_type,
                'status': 'skipped',
                'message': 'Special protocol'
            })
            continue
        
        # Validate local files
        is_valid, message = validate_local_file(url, file_path.parent)
        
        result = {
            'url': url,
            'text': text,
            'type': link_type,
            'status': 'valid' if is_valid else 'invalid',
            'message': message
        }
        
        # Additional PDF validation
        if url.endswith('.pdf') and is_valid:
            pdf_path = file_path.parent / url if not url.startswith('/') else Path(url)
            if pdf_path.exists():
                pdf_valid, pdf_message = validate_pdf_accessibility(pdf_path)
                result['pdf_status'] = 'valid' if pdf_valid else 'invalid'
                result['pdf_message'] = pdf_message
        
        results.append(result)
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Validate links in markdown documentation')
    parser.add_argument('directory', help='Directory to scan for markdown files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--pdf-only', action='store_true', help='Only validate PDF links')
    
    args = parser.parse_args()
    
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        sys.exit(1)
    
    print(f"Scanning for markdown files in: {directory}")
    md_files = find_markdown_files(directory)
    print(f"Found {len(md_files)} markdown files")
    
    total_links = 0
    invalid_links = 0
    pdf_links = 0
    invalid_pdfs = 0
    
    for md_file in md_files:
        if args.verbose:
            print(f"\nValidating: {md_file}")
        
        results = validate_links_in_file(md_file)
        file_invalid = 0
        file_pdf_invalid = 0
        
        for result in results:
            if 'error' in result:
                print(f"ERROR in {md_file}: {result['error']}")
                continue
            
            total_links += 1
            
            # Check for PDF links
            if result['url'].endswith('.pdf'):
                pdf_links += 1
                if args.pdf_only or args.verbose:
                    print(f"  PDF: {result['url']} - {result['status']}")
                    if 'pdf_status' in result:
                        print(f"    PDF Validation: {result['pdf_message']}")
                        if result['pdf_status'] == 'invalid':
                            invalid_pdfs += 1
                            file_pdf_invalid += 1
            
            if result['status'] == 'invalid':
                invalid_links += 1
                file_invalid += 1
                if not args.pdf_only:
                    print(f"  INVALID: {result['url']} - {result['message']}")
            elif args.verbose and not args.pdf_only:
                print(f"  OK: {result['url']}")
        
        if file_invalid > 0 or file_pdf_invalid > 0:
            print(f"  {md_file}: {file_invalid} invalid links, {file_pdf_invalid} invalid PDFs")
    
    print(f"\n=== Summary ===")
    print(f"Total links checked: {total_links}")
    print(f"Invalid links: {invalid_links}")
    print(f"PDF links found: {pdf_links}")
    print(f"Invalid PDFs: {invalid_pdfs}")
    
    if invalid_links > 0 or invalid_pdfs > 0:
        print(f"\n❌ Validation failed: {invalid_links + invalid_pdfs} issues found")
        sys.exit(1)
    else:
        print(f"\n✅ All links are valid!")

if __name__ == '__main__':
    main()
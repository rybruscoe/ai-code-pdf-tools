#!/usr/bin/env python3
"""
Documentation Index Generator
Creates a comprehensive index of all documentation including PDFs.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
import argparse

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    frontmatter = {}
    if content.startswith('---\n'):
        end_pos = content.find('\n---\n', 4)
        if end_pos != -1:
            fm_content = content[4:end_pos]
            # Simple YAML parsing for common fields
            for line in fm_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    return frontmatter

def extract_title_and_description(content):
    """Extract title and description from markdown content."""
    lines = content.split('\n')
    title = None
    description = None
    
    # Look for first H1 heading
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Look for first paragraph as description
    in_frontmatter = content.startswith('---\n')
    skip_lines = 0
    
    if in_frontmatter:
        end_pos = content.find('\n---\n', 4)
        if end_pos != -1:
            skip_lines = content[:end_pos + 5].count('\n')
    
    for i, line in enumerate(lines[skip_lines:], skip_lines):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('```') and len(line) > 20:
            description = line[:200] + ('...' if len(line) > 200 else '')
            break
    
    return title, description

def get_file_info(file_path):
    """Get comprehensive information about a file."""
    stat = file_path.stat()
    
    info = {
        'path': str(file_path),
        'name': file_path.name,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'type': file_path.suffix.lower()
    }
    
    if file_path.suffix.lower() == '.md':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = extract_frontmatter(content)
            title, description = extract_title_and_description(content)
            
            info.update({
                'title': frontmatter.get('title', title),
                'description': frontmatter.get('description', description),
                'tags': frontmatter.get('tags', '').split(',') if frontmatter.get('tags') else [],
                'author': frontmatter.get('author'),
                'date': frontmatter.get('date'),
                'word_count': len(content.split()),
                'headings': extract_headings(content)
            })
            
        except Exception as e:
            info['error'] = str(e)
    
    elif file_path.suffix.lower() == '.pdf':
        # Try to get PDF metadata
        try:
            import subprocess
            result = subprocess.run(
                ['pdfinfo', str(file_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                pdf_info = {}
                for line in result.stdout.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        pdf_info[key.strip().lower().replace(' ', '_')] = value.strip()
                
                info.update({
                    'title': pdf_info.get('title'),
                    'author': pdf_info.get('author'),
                    'subject': pdf_info.get('subject'),
                    'pages': pdf_info.get('pages'),
                    'creation_date': pdf_info.get('creationdate'),
                    'pdf_version': pdf_info.get('pdf_version')
                })
        except:
            pass  # PDF info extraction failed, continue without it
    
    return info

def extract_headings(content):
    """Extract all headings from markdown content."""
    headings = []
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level <= 6:  # Valid heading levels
                text = line[level:].strip()
                headings.append({
                    'level': level,
                    'text': text,
                    'anchor': text.lower().replace(' ', '-').replace('.', '').replace(',', '').replace('(', '').replace(')', '')
                })
    
    return headings

def scan_directory(directory, include_patterns=None, exclude_patterns=None):
    """Scan directory for documentation files."""
    if include_patterns is None:
        include_patterns = ['*.md', '*.pdf', '*.rst', '*.txt']
    
    if exclude_patterns is None:
        exclude_patterns = ['node_modules', '.git', '__pycache__', '.vscode', 'venv', 'env']
    
    files = []
    
    for root, dirs, filenames in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        for filename in filenames:
            file_path = Path(root) / filename
            
            # Check if file matches include patterns
            if any(file_path.match(pattern) for pattern in include_patterns):
                files.append(file_path)
    
    return files

def generate_index_markdown(files_info, output_path):
    """Generate a markdown index file."""
    content = f"""# Documentation Index

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

This index contains all documentation files in the project, including PDFs, markdown files, and other documentation formats.

## Quick Navigation

- [📚 All Documents](#all-documents)
- [📄 PDF Documents](#pdf-documents)
- [📝 Markdown Documents](#markdown-documents)
- [🏷️ By Category](#by-category)

## Statistics

"""
    
    # Calculate statistics
    total_files = len(files_info)
    pdf_files = len([f for f in files_info if f['type'] == '.pdf'])
    md_files = len([f for f in files_info if f['type'] == '.md'])
    total_size = sum(f['size'] for f in files_info)
    
    content += f"""- **Total Documents**: {total_files}
- **PDF Files**: {pdf_files}
- **Markdown Files**: {md_files}
- **Total Size**: {total_size / 1024 / 1024:.1f} MB

## All Documents

| Document | Type | Size | Modified | Description |
|----------|------|------|----------|-------------|
"""
    
    # Sort files by type, then by name
    sorted_files = sorted(files_info, key=lambda x: (x['type'], x['name']))
    
    for file_info in sorted_files:
        name = file_info['name']
        path = file_info['path']
        file_type = file_info['type'].upper()[1:]  # Remove dot and uppercase
        size = f"{file_info['size'] / 1024:.1f} KB" if file_info['size'] < 1024*1024 else f"{file_info['size'] / 1024 / 1024:.1f} MB"
        modified = datetime.fromisoformat(file_info['modified']).strftime('%Y-%m-%d')
        description = file_info.get('description', file_info.get('subject', ''))[:100] + ('...' if len(file_info.get('description', file_info.get('subject', ''))) > 100 else '') if file_info.get('description') or file_info.get('subject') else ''
        
        content += f"| [{name}]({path}) | {file_type} | {size} | {modified} | {description} |\n"
    
    # PDF Documents section
    pdf_docs = [f for f in files_info if f['type'] == '.pdf']
    if pdf_docs:
        content += f"\n## PDF Documents\n\n"
        for pdf in pdf_docs:
            title = pdf.get('title', pdf['name'])
            author = pdf.get('author', 'Unknown')
            pages = pdf.get('pages', 'Unknown')
            
            content += f"### [{title}]({pdf['path']})\n\n"
            content += f"- **Author**: {author}\n"
            content += f"- **Pages**: {pages}\n"
            content += f"- **Size**: {pdf['size'] / 1024 / 1024:.1f} MB\n"
            if pdf.get('subject'):
                content += f"- **Subject**: {pdf['subject']}\n"
            
            # Check for corresponding markdown file
            md_path = Path(pdf['path']).with_suffix('.md')
            if md_path.exists():
                content += f"- **Markdown Version**: [{md_path.name}]({md_path})\n"
            
            content += "\n"
    
    # Markdown Documents section
    md_docs = [f for f in files_info if f['type'] == '.md']
    if md_docs:
        content += f"\n## Markdown Documents\n\n"
        
        # Group by directory
        by_dir = {}
        for md in md_docs:
            dir_name = str(Path(md['path']).parent)
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(md)
        
        for dir_name, docs in sorted(by_dir.items()):
            content += f"### {dir_name}\n\n"
            for doc in sorted(docs, key=lambda x: x['name']):
                title = doc.get('title', doc['name'])
                content += f"- [{title}]({doc['path']})"
                if doc.get('description'):
                    content += f" - {doc['description'][:100]}{'...' if len(doc['description']) > 100 else ''}"
                content += "\n"
            content += "\n"
    
    # By Category section
    content += "\n## By Category\n\n"
    
    categories = {
        'Setup Guides': [f for f in files_info if 'setup' in f['name'].lower() or 'install' in f['name'].lower()],
        'Configuration': [f for f in files_info if 'config' in f['name'].lower() or 'settings' in f['name'].lower()],
        'Troubleshooting': [f for f in files_info if 'troubleshoot' in f['name'].lower() or 'debug' in f['name'].lower()],
        'Reference': [f for f in files_info if 'reference' in f['name'].lower() or 'spec' in f['name'].lower()],
        'API Documentation': [f for f in files_info if 'api' in f['name'].lower()],
    }
    
    for category, docs in categories.items():
        if docs:
            content += f"### {category}\n\n"
            for doc in docs:
                title = doc.get('title', doc['name'])
                content += f"- [{title}]({doc['path']})\n"
            content += "\n"
    
    content += """
## Usage Tips

### VS Code Integration
- Install the recommended extensions for PDF viewing
- Use `Ctrl+Shift+F` to search across all documentation
- PDF files can be viewed directly in VS Code with the PDF extension

### Command Line Tools
```bash
# Search in all documentation
grep -r "search term" docs/

# Search in PDFs
find docs/ -name "*.pdf" -exec pdfgrep "search term" {} +

# Generate updated index
python3 tools/generate_doc_index.py docs/

# Validate all links
python3 tools/validate_links.py docs/
```

### PDF Tools
```bash
# Create PDF summary
python3 tools/pdf_summary.py path/to/document.pdf

# Extract text from PDF
pdftotext document.pdf document.txt

# Get PDF information
pdfinfo document.pdf
```

---
*This index is automatically generated. To update it, run the documentation index generator.*
"""
    
    # Write the index file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Generate comprehensive documentation index')
    parser.add_argument('directory', help='Directory to scan for documentation')
    parser.add_argument('--output', '-o', help='Output file path', default='docs/INDEX.md')
    parser.add_argument('--include', nargs='+', help='File patterns to include', default=['*.md', '*.pdf', '*.rst', '*.txt'])
    parser.add_argument('--exclude', nargs='+', help='Directory patterns to exclude', default=['node_modules', '.git', '__pycache__', '.vscode', 'venv', 'env'])
    
    args = parser.parse_args()
    
    directory = Path(args.directory)
    if not directory.exists():
        print(f"Error: Directory not found: {directory}")
        return 1
    
    print(f"Scanning directory: {directory}")
    files = scan_directory(directory, args.include, args.exclude)
    print(f"Found {len(files)} documentation files")
    
    print("Extracting file information...")
    files_info = []
    for file_path in files:
        try:
            info = get_file_info(file_path)
            files_info.append(info)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating index: {output_path}")
    generate_index_markdown(files_info, output_path)
    
    print(f"Documentation index generated successfully!")
    print(f"Index contains {len(files_info)} files")
    
    return 0

if __name__ == '__main__':
    exit(main())
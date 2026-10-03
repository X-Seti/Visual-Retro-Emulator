#!/usr/bin/env python3
"""
X-Seti - May 21 2025 - Add Directory to Knowledge Base
Scans directory and creates documentation for AI knowledge base
"""

import os
import json
from pathlib import Path

def scan_directory(directory, max_files=50):
    """Scan directory and extract key information"""
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"❌ Directory not found: {directory}")
        return None
    
    knowledge_entry = {
        "directory": str(dir_path),
        "type": "code_project",
        "structure": {},
        "key_files": [],
        "patterns": [],
        "technologies": set(),
        "purpose": ""
    }
    
    file_count = 0
    
    # Walk through directory
    for root, dirs, files in os.walk(dir_path):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        rel_root = os.path.relpath(root, dir_path)
        if rel_root == '.':
            rel_root = ''
        
        # Process files
        for file in files:
            if file_count >= max_files:
                break
                
            file_path = Path(root) / file
            rel_path = str(Path(rel_root) / file) if rel_root else file
            
            # Skip binary and cache files
            if file.startswith('.') or file.endswith(('.pyc', '.pyo')):
                continue
            
            # Detect file type and importance
            file_info = analyze_file(file_path)
            if file_info:
                knowledge_entry["structure"][rel_path] = file_info
                
                # Track technologies
                knowledge_entry["technologies"].update(file_info.get("tech", []))
                
                # Mark important files
                if file_info.get("importance", 0) > 7:
                    knowledge_entry["key_files"].append(rel_path)
            
            file_count += 1
    
    # Convert set to list for JSON serialization
    knowledge_entry["technologies"] = list(knowledge_entry["technologies"])
    
    # Detect patterns
    knowledge_entry["patterns"] = detect_patterns(knowledge_entry)
    
    return knowledge_entry

def analyze_file(file_path):
    """Analyze individual file"""
    file_info = {
        "size": file_path.stat().st_size,
        "type": file_path.suffix,
        "tech": [],
        "importance": 0,
        "summary": ""
    }
    
    # Determine importance and tech stack
    if file_path.suffix == '.py':
        file_info["tech"].append("Python")
        file_info["importance"] = 6
        
        # Check for main files or special patterns
        if file_path.name in ['main.py', '__init__.py', 'app.py']:
            file_info["importance"] = 9
        elif 'test' in file_path.name.lower():
            file_info["importance"] = 4
        elif file_path.name.startswith('_'):
            file_info["importance"] = 3
            
    elif file_path.suffix in ['.js', '.ts']:
        file_info["tech"].extend(["JavaScript", "Web"])
        file_info["importance"] = 6
        
    elif file_path.suffix in ['.rs']:
        file_info["tech"].append("Rust")
        file_info["importance"] = 7
        
    elif file_path.suffix in ['.cpp', '.c', '.h']:
        file_info["tech"].append("C++")
        file_info["importance"] = 7
        
    elif file_path.suffix in ['.json', '.yaml', '.yml']:
        file_info["tech"].append("Config")
        file_info["importance"] = 5
        
    elif file_path.suffix in ['.md', '.txt']:
        file_info["tech"].append("Documentation")
        file_info["importance"] = 4
        
    elif file_path.name in ['Cargo.toml', 'package.json', 'requirements.txt']:
        file_info["importance"] = 8
        file_info["tech"].append("Dependencies")
    
    # Read first few lines for context (text files only)
    if file_path.suffix in ['.py', '.js', '.rs', '.cpp', '.md'] and file_info["size"] < 50000:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = f.read(500)
                file_info["summary"] = extract_summary(first_lines, file_path.suffix)
        except:
            pass
    
    return file_info

def extract_summary(content, file_type):
    """Extract brief summary from file content"""
    lines = content.split('\n')[:10]
    
    # Look for docstrings, comments, or obvious purpose
    for line in lines:
        line = line.strip()
        if file_type == '.py':
            if line.startswith('"""') or line.startswith("'''"):
                return line.strip('"\' ')
            elif line.startswith('#') and len(line) > 10:
                return line[1:].strip()
        elif file_type in ['.js', '.cpp']:
            if line.startswith('/*') or line.startswith('//'):
                return line.strip('/*/ ')
        elif file_type == '.rs':
            if line.startswith('//!') or line.startswith('///'):
                return line.strip('/*/ ')
        elif file_type == '.md':
            if line.startswith('#'):
                return line.strip('# ')
    
    return ""

def detect_patterns(knowledge_entry):
    """Detect common patterns in the project"""
    patterns = []
    
    structure = knowledge_entry["structure"]
    technologies = knowledge_entry["technologies"]
    
    # Architecture patterns
    if any("main" in f for f in structure.keys()):
        patterns.append("Entry Point Pattern")
    
    if any("test" in f.lower() for f in structure.keys()):
        patterns.append("Test Suite")
    
    if "components" in str(structure.keys()).lower():
        patterns.append("Component Architecture")
    
    # Technology patterns
    if "Python" in technologies:
        if any(f.endswith("requirements.txt") for f in structure.keys()):
            patterns.append("Python Package")
        if any("PyQt" in str(v) for v in structure.values()):
            patterns.append("GUI Application")
    
    if "Rust" in technologies:
        if "Cargo.toml" in structure:
            patterns.append("Rust Crate")
    
    # Size patterns
    if len(structure) > 100:
        patterns.append("Large Codebase")
    elif len(structure) < 10:
        patterns.append("Small Project")
    
    return patterns

def create_kb_document(knowledge_entry, output_file="kb_entry.md"):
    """Create markdown knowledge base entry"""
    kb_doc = f"""# {Path(knowledge_entry['directory']).name} - Project Knowledge Base Entry

## 📁 Directory Overview
- **Path**: `{knowledge_entry['directory']}`
- **Technologies**: {', '.join(knowledge_entry['technologies'])}
- **Patterns**: {', '.join(knowledge_entry['patterns'])}
- **Files Analyzed**: {len(knowledge_entry['structure'])}

## 🗂️ Key Files
{chr(10).join([f"- `{f}`" for f in knowledge_entry['key_files']])}

## 📋 File Structure Summary
"""
    
    # Group files by type
    by_type = {}
    for file_path, info in knowledge_entry['structure'].items():
        file_type = info.get('type', 'other')
        if file_type not in by_type:
            by_type[file_type] = []
        by_type[file_type].append((file_path, info))
    
    for file_type, files in sorted(by_type.items()):
        kb_doc += f"\n### {file_type.upper()} Files\n"
        
        # Sort by importance
        files.sort(key=lambda x: x[1].get('importance', 0), reverse=True)
        
        for file_path, info in files[:10]:  # Limit to top 10 per type
            summary = info.get('summary', '')
            importance = info.get('importance', 0)
            kb_doc += f"- **{file_path}** (importance: {importance})\n"
            if summary:
                kb_doc += f"  - {summary}\n"
    
    kb_doc += f"""
## 🔧 Technical Details
- **Primary Language**: {knowledge_entry['technologies'][0] if knowledge_entry['technologies'] else 'Unknown'}
- **Architecture Patterns**: {', '.join(knowledge_entry['patterns'])}

## 💡 Usage Instructions
Add this entry to your AI knowledge base by copying this document.
The AI can now understand the structure and purpose of this directory.

---
*Generated automatically by add_to_kb.py*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(kb_doc)
    
    return kb_doc

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) < 2:
        directory = input("📁 Enter directory path to add to knowledge base: ").strip()
    else:
        directory = sys.argv[1]
    
    print(f"🔍 Scanning directory: {directory}")
    
    knowledge_entry = scan_directory(directory)
    if not knowledge_entry:
        return 1
    
    # Create documentation
    kb_doc = create_kb_document(knowledge_entry)
    
    print(f"✅ Knowledge base entry created: kb_entry.md")
    print(f"📊 Analyzed {len(knowledge_entry['structure'])} files")
    print(f"🛠️ Technologies: {', '.join(knowledge_entry['technologies'])}")
    print(f"📋 Patterns: {', '.join(knowledge_entry['patterns'])}")
    
    # Also save JSON for programmatic use
    with open('kb_entry.json', 'w') as f:
        json.dump(knowledge_entry, f, indent=2)
    
    print("\n💡 Next steps:")
    print("1. Review kb_entry.md")
    print("2. Copy relevant sections to your AI knowledge base")
    print("3. Customize the summary as needed")
    
    return 0

if __name__ == "__main__":
    exit(main())

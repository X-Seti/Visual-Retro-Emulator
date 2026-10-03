#!/usr/bin/env python3
"""
X-Seti - June25 2025 - Clean Launcher
Cleans cache and runs main_app.py  
"""

import subprocess
import sys
from pathlib import Path

def clean_cache():
    """Clean Python cache"""
    print("🧹 Cleaning cache before startup...")
    
    current_dir = Path(__file__).parent
    
    # Clean __pycache__
    subprocess.run(["find", ".", "-name", "__pycache__", "-type", "d", "-exec", "rm", "-rf", "{}", "+"], 
                   cwd=current_dir, capture_output=True)
    
    # Clean .pyc files
    subprocess.run(["find", ".", "-name", "*.pyc", "-delete"], 
                   cwd=current_dir, capture_output=True)
    
    print("✅ Cache cleaned")

if __name__ == "__main__":
    clean_cache()
    
    # Run main app
    print("🚀 Starting Visual Retro Emulator...")
    subprocess.run([sys.executable, "main_app.py"])

#!/bin/bash
# Auto-generated conflict cleanup script
# Review before running!

echo "🧹 Visual Retro Emulator Conflict Cleanup"
echo "========================================="
echo "This will remove duplicate files. Press Ctrl+C to cancel."
read -p "Continue? (y/N): " confirm

if [[ $confirm != [yY] ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Backup files before removal
mkdir -p cleanup_backup

if [ -f "ui/cad_tools.py" ]; then
    echo "📦 Backing up ui/cad_tools.py"
    cp "ui/cad_tools.py" cleanup_backup/
    echo "🗑️  Removing ui/cad_tools.py"
    rm "ui/cad_tools.py"
fi
if [ -f "project_manager.py" ]; then
    echo "📦 Backing up project_manager.py"
    cp "project_manager.py" cleanup_backup/
    echo "🗑️  Removing project_manager.py"
    rm "project_manager.py"
fi
if [ -f "components/cpu/motorola_68000.py" ]; then
    echo "📦 Backing up components/cpu/motorola_68000.py"
    cp "components/cpu/motorola_68000.py" cleanup_backup/
    echo "🗑️  Removing components/cpu/motorola_68000.py"
    rm "components/cpu/motorola_68000.py"
fi

echo "✅ Cleanup complete!"
echo "📦 Backups saved in cleanup_backup/"
echo "🔧 Now update your imports to use single sources"

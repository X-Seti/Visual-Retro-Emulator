#!/usr/bin/env python3
"""
May27, 2025 X-Seti - Chip Image Generator
Generates realistic chip images for various retro computer components
"""

import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap, QColor, QFont
from pathlib import Path
#from enhanced_amiga_chips import add_enhanced_amiga_chips

# Import the fixed chip renderer
try:
    from realistic_chip_renderer import ChipPackageRenderer
except ImportError:
    print("❌ Error: realistic_chip_renderer.py not found or has errors.")
    print("Please ensure you have the fixed version of the renderer.")
    sys.exit(1)


class RetroChipGenerator:
    """Generates realistic chip images for retro computer components"""

    def __init__(self):
        """Initialize the generator"""
        self.renderer = ChipPackageRenderer()
        self.chip_definitions = []
        self.output_dir = Path("images/components")

    def add_chip(self, name, chip_id, category, description, package_types, pins=None):
        """Add a chip definition to the generator

        Args:
            name: Display name of the chip
            chip_id: Unique component ID (used for filename)
            category: Component category (CPU, GPU, Sound, etc.)
            description: Short description
            package_types: List of package types (e.g. ['DIP-40', 'QFP-44'])
            pins: List of pin dictionaries (optional)
        """
        # Create a default pins list if not provided
        if pins is None:
            pins = []
            # Add default pins based on largest package
            max_pins = 0
            for pkg in package_types:
                try:
                    pin_count = int(pkg.split('-')[1])
                    max_pins = max(max_pins, pin_count)
                except (IndexError, ValueError):
                    continue

            # Generate generic pin names
            for i in range(1, max_pins + 1):
                pins.append({'name': f'P{i}'})

        # Add to our chip definitions
        self.chip_definitions.append({
            'name': name,
            'id': chip_id,
            'category': category,
            'description': description,
            'packages': package_types,
            'pins': pins
        })

        return self  # Allow chaining

    def generate_images(self):
        """Generate images for all defined chips"""
        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True, parents=True)

        # Create a dummy component definition class
        class ComponentDef:
            def __init__(self, name, comp_id, category, pins):
                self.name = name
                self.component_id = comp_id
                self.category = category
                self.pins = pins

        # Initialize QApplication if needed
        if not QApplication.instance():
            app = QApplication([])

        print(f"🎨 Generating realistic chip images for {len(self.chip_definitions)} components...")

        for chip in self.chip_definitions:
            print(f"  🔧 Creating images for {chip['name']}...")

            comp_def = ComponentDef(
                chip['name'],
                chip['id'],
                chip['category'],
                chip['pins']
            )

            for package in chip['packages']:
                print(f"    📦 Package: {package}")

                # Generate image
                pixmap = self.renderer.create_chip_image(comp_def, package, 400)

                # Save image
                filename = f"{self.output_dir}/{chip['id']}_{package.lower().replace('-', '_')}.png"
                pixmap.save(filename)
                print(f"      💾 Saved: {filename}")

        print("✅ All chip images generated!")
        print(f"📁 Images saved in: {self.output_dir}/")

        return True

    def get_component_definitions(self):
        """Get component definitions that can be used for creating component files"""
        component_templates = []

        for chip in self.chip_definitions:
            template = f'''"""
{chip['name']} - {chip['description']}
Generated component definition
"""

def create_component():
    comp = ComponentDefinition(
        "{chip['id']}",
        "{chip['name']}",
        "{chip['category']}",
        "{chip['description']}",
        width=200,
        height=50
    )

    # Package type (supports multiple variants)
    comp.package_type = "{chip['packages'][0]}"  # Default package

    # Add pins
    pin_list = {str([p['name'] for p in chip['pins']]).replace("'", '"')}
    for i, pin_name in enumerate(pin_list):
        comp.add_pin(i+1, pin_name)

    # Add variants
    {self._generate_variants_code(chip)}

    return comp
'''
            component_templates.append((chip['id'], template))

        return component_templates

    def _generate_variants_code(self, chip):
        """Generate code for package variants"""
        if len(chip['packages']) <= 1:
            return "# No variants"

        variants_code = []
        for pkg in chip['packages'][1:]:
            variant_id = f"{chip['id']}_{pkg.lower().replace('-', '_')}"
            variant_name = f"{chip['name']} ({pkg})"
            variants_code.append(f'comp.add_variant("{variant_id}", "{variant_name}", "{pkg}")')

        return "\n    ".join(variants_code)

    def create_component_files(self, base_dir="components"):
        """Create component definition files in the appropriate directories"""
        print(f"📝 Creating component definition files...")

        component_defs = self.get_component_definitions()
        created_files = []

        for comp_id, template in component_defs:
            # Determine the appropriate directory based on ID prefix
            directory = None

            if comp_id.startswith("amiga_"):
                directory = Path(base_dir) / "amiga"
            elif comp_id.startswith("c64_"):
                directory = Path(base_dir) / "commodore"
            else:
                directory = Path(base_dir) / "custom"

            # Ensure directory exists
            directory.mkdir(exist_ok=True, parents=True)

            # Create filename
            filename = directory / f"{comp_id}.py"

            # Write file
            with open(filename, "w") as f:
                f.write(template)

            created_files.append(str(filename))
            print(f"  ✅ Created: {filename}")

        print(f"📁 Created {len(created_files)} component definition files")
        return created_files


def main():
    """Main function"""
    print("🖥️  Retro Chip Image Generator")
    print("=" * 60)

    # Create generator
    generator = RetroChipGenerator()

    # Add chip definitions for various systems
    print("🔍 Adding chip definitions...")

    # Only use the methods that are known to work

    # Generate images
    print("\n🎨 Generating images...")
    generator.generate_images()

    # Create component definition files
    print("\n📄 Creating component definition files...")
    generator.create_component_files()

    print("\n🎉 All done! Your retro chip collection is ready.")
    print("=" * 60)
    print("💡 TIP: Add these components to your projects to use the realistic chip images.")

    return 0


if __name__ == "__main__":
    sys.exit(main())





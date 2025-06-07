"""
May26, 2025 X-Seti - Manufacturing Export Utilities
Handles export of Gerber files, drill files, and pick & place data
"""

import os
import csv
import json
from datetime import datetime
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QMessageBox, QProgressDialog, QApplication
from enhanced_rendering import EnhancedHardwareComponent, ICPackage
from enhanced_connection_system import EnhancedConnection


class GerberExporter:
    """Exports Gerber files for PCB manufacturing"""
    
    def __init__(self):
        self.units = "mm"  # or "inch"
        self.precision = 6  # decimal places
    
    def export_gerber_files(self, scene, output_dir, board_params=None):
        """Export complete set of Gerber files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Default board parameters
        if board_params is None:
            board_params = {
                "width": 100,  # mm
                "height": 80,   # mm
                "layers": 2,
                "thickness": 1.6  # mm
            }
        
        # Collect components and connections
        components = [item for item in scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        connections = [item for item in scene.items() 
                      if isinstance(item, EnhancedConnection)]
        
        files_created = []
        
        try:
            # Create progress dialog
            progress = QProgressDialog("Exporting Gerber files...", "Cancel", 0, 7)
            progress.setWindowTitle("Gerber Export")
            progress.show()
            QApplication.processEvents()
            
            # Export top copper layer
            progress.setLabelText("Exporting top copper layer...")
            progress.setValue(1)
            QApplication.processEvents()
            top_copper_file = os.path.join(output_dir, "PCB-F.Cu.gbr")
            self._export_copper_layer(components, connections, top_copper_file, "top")
            files_created.append(top_copper_file)
            
            # Export bottom copper layer (if multi-layer)
            if board_params["layers"] > 1:
                progress.setLabelText("Exporting bottom copper layer...")
                progress.setValue(2)
                QApplication.processEvents()
                bottom_copper_file = os.path.join(output_dir, "PCB-B.Cu.gbr")
                self._export_copper_layer(components, connections, bottom_copper_file, "bottom")
                files_created.append(bottom_copper_file)
            
            # Export top solder mask
            progress.setLabelText("Exporting top solder mask...")
            progress.setValue(3)
            QApplication.processEvents()
            top_mask_file = os.path.join(output_dir, "PCB-F.Mask.gbr")
            self._export_solder_mask(components, top_mask_file, "top")
            files_created.append(top_mask_file)
            
            # Export bottom solder mask
            progress.setLabelText("Exporting bottom solder mask...")
            progress.setValue(4)
            QApplication.processEvents()
            bottom_mask_file = os.path.join(output_dir, "PCB-B.Mask.gbr")
            self._export_solder_mask(components, bottom_mask_file, "bottom")
            files_created.append(bottom_mask_file)
            
            # Export top silkscreen
            progress.setLabelText("Exporting top silkscreen...")
            progress.setValue(5)
            QApplication.processEvents()
            top_silk_file = os.path.join(output_dir, "PCB-F.SilkS.gbr")
            self._export_silkscreen(components, top_silk_file, "top")
            files_created.append(top_silk_file)
            
            # Export board outline
            progress.setLabelText("Exporting board outline...")
            progress.setValue(6)
            QApplication.processEvents()
            outline_file = os.path.join(output_dir, "PCB-Edge.Cuts.gbr")
            self._export_board_outline(board_params, outline_file)
            files_created.append(outline_file)
            
            # Create job file
            progress.setLabelText("Creating job file...")
            progress.setValue(7)
            QApplication.processEvents()
            job_file = os.path.join(output_dir, "PCB-job.gbrjob")
            self._create_job_file(board_params, files_created, job_file)
            files_created.append(job_file)
            
            progress.close()
            return files_created
            
        except Exception as e:
            if 'progress' in locals():
                progress.close()
            raise Exception(f"Gerber export failed: {str(e)}")
    
    def _export_copper_layer(self, components, connections, filename, layer):
        """Export copper layer (traces and pads)"""
        with open(filename, 'w') as f:
            # Gerber header
            f.write("G04 #@! TF.GenerationSoftware,Visual Retro System Emulator Builder*\n")
            f.write(f"G04 #@! TF.CreationDate,{datetime.now().isoformat()}*\n")
            f.write(f"G04 #@! TF.FileFunction,Copper,L1,{layer.title()}*\n")
            f.write("G04 #@! TF.FilePolarity,Positive*\n")
            f.write("%FSLAX36Y36*%\n")  # Format specification
            f.write("%MOMM*%\n")  # Units in millimeters
            
            # Define apertures
            f.write("%ADD10C,0.8*%\n")  # Circle 0.8mm for pads
            f.write("%ADD11C,0.4*%\n")  # Circle 0.4mm for vias
            f.write("%ADD12C,0.2*%\n")  # Circle 0.2mm for traces
            
            # Draw component pads
            for component in components:
                if hasattr(component, 'pin_points'):
                    for pin_name, pin in component.pin_points.items():
                        pos = pin.get_scene_pos()
                        x_coord = int(pos.x() * 1000000)  # Convert to Gerber units
                        y_coord = int(pos.y() * 1000000)
                        
                        f.write("D10*\n")  # Select pad aperture
                        f.write(f"X{x_coord:08d}Y{y_coord:08d}D03*\n")  # Flash pad
            
            # Draw traces (connections)
            for connection in connections:
                source_pos = connection.source_pin.get_scene_pos()
                target_pos = connection.target_pin.get_scene_pos()
                
                x1 = int(source_pos.x() * 1000000)
                y1 = int(source_pos.y() * 1000000)
                x2 = int(target_pos.x() * 1000000)
                y2 = int(target_pos.y() * 1000000)
                
                f.write("D12*\n")  # Select trace aperture
                f.write(f"G01X{x1:08d}Y{y1:08d}D02*\n")  # Move to start
                f.write(f"X{x2:08d}Y{y2:08d}D01*\n")  # Draw line
            
            # Gerber footer
            f.write("M02*\n")  # End of file
    
    def _export_solder_mask(self, components, filename, layer):
        """Export solder mask layer"""
        with open(filename, 'w') as f:
            # Gerber header
            f.write("G04 #@! TF.GenerationSoftware,Visual Retro System Emulator Builder*\n")
            f.write(f"G04 #@! TF.CreationDate,{datetime.now().isoformat()}*\n")
            f.write(f"G04 #@! TF.FileFunction,Soldermask,{layer.title()}*\n")
            f.write("G04 #@! TF.FilePolarity,Negative*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOMM*%\n")
            
            # Define apertures (slightly larger than pads for mask opening)
            f.write("%ADD10C,1.0*%\n")  # Circle 1.0mm for pad openings
            
            # Create mask openings for component pads
            for component in components:
                if hasattr(component, 'pin_points'):
                    for pin_name, pin in component.pin_points.items():
                        pos = pin.get_scene_pos()
                        x_coord = int(pos.x() * 1000000)
                        y_coord = int(pos.y() * 1000000)
                        
                        f.write("D10*\n")
                        f.write(f"X{x_coord:08d}Y{y_coord:08d}D03*\n")
            
            f.write("M02*\n")
    
    def _export_silkscreen(self, components, filename, layer):
        """Export silkscreen layer (component outlines and text)"""
        with open(filename, 'w') as f:
            # Gerber header
            f.write("G04 #@! TF.GenerationSoftware,Visual Retro System Emulator Builder*\n")
            f.write(f"G04 #@! TF.CreationDate,{datetime.now().isoformat()}*\n")
            f.write(f"G04 #@! TF.FileFunction,Legend,{layer.title()}*\n")
            f.write("G04 #@! TF.FilePolarity,Positive*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOMM*%\n")
            
            # Define apertures for silkscreen
            f.write("%ADD10C,0.15*%\n")  # Thin line for outlines
            f.write("%ADD11R,0.4X0.4*%\n")  # Rectangle for text
            
            # Draw component outlines and labels
            f.write("D10*\n")  # Select outline aperture
            
            for component in components:
                # Draw component outline
                pos = component.pos()
                width = component.rect().width()
                height = component.rect().height()
                
                # Convert to Gerber coordinates
                x1 = int(pos.x() * 1000000)
                y1 = int(pos.y() * 1000000)
                x2 = int((pos.x() + width) * 1000000)
                y2 = int((pos.y() + height) * 1000000)
                
                # Draw rectangle outline
                f.write(f"G01X{x1:08d}Y{y1:08d}D02*\n")  # Move to corner
                f.write(f"X{x2:08d}Y{y1:08d}D01*\n")     # Draw top
                f.write(f"X{x2:08d}Y{y2:08d}D01*\n")     # Draw right
                f.write(f"X{x1:08d}Y{y2:08d}D01*\n")     # Draw bottom
                f.write(f"X{x1:08d}Y{y1:08d}D01*\n")     # Draw left
                
                # Add reference designator text (simplified)
                ref_des = getattr(component, 'reference_designator', 'U?')
                text_x = int((pos.x() + width/2) * 1000000)
                text_y = int((pos.y() + height/2) * 1000000)
                
                # Simple text representation (would need proper text rendering)
                f.write(f"G04 Text: {ref_des} at X{text_x:08d}Y{text_y:08d}*\n")
            
            f.write("M02*\n")
    
    def _export_board_outline(self, board_params, filename):
        """Export board outline/edge cuts"""
        with open(filename, 'w') as f:
            # Gerber header
            f.write("G04 #@! TF.GenerationSoftware,Visual Retro System Emulator Builder*\n")
            f.write(f"G04 #@! TF.CreationDate,{datetime.now().isoformat()}*\n")
            f.write("G04 #@! TF.FileFunction,Profile,NP*\n")
            f.write("%FSLAX36Y36*%\n")
            f.write("%MOMM*%\n")
            
            # Define aperture for board outline
            f.write("%ADD10C,0.1*%\n")  # Thin line for outline
            
            # Draw board outline
            width = board_params["width"]
            height = board_params["height"]
            
            # Convert to Gerber coordinates
            x1, y1 = 0, 0
            x2 = int(width * 1000000)
            y2 = int(height * 1000000)
            
            f.write("D10*\n")  # Select aperture
            f.write(f"G01X{x1:08d}Y{y1:08d}D02*\n")  # Move to origin
            f.write(f"X{x2:08d}Y{y1:08d}D01*\n")     # Draw top
            f.write(f"X{x2:08d}Y{y2:08d}D01*\n")     # Draw right
            f.write(f"X{x1:08d}Y{y2:08d}D01*\n")     # Draw bottom
            f.write(f"X{x1:08d}Y{y1:08d}D01*\n")     # Draw left
            
            f.write("M02*\n")
    
    def _create_job_file(self, board_params, file_list, filename):
        """Create Gerber job file (JSON format)"""
        job_data = {
            "Header": {
                "GenerationSoftware": {
                    "Vendor": "Visual Retro System Emulator Builder",
                    "Application": "Enhanced PCB Designer",
                    "Version": "1.0"
                },
                "CreationDate": datetime.now().isoformat()
            },
            "GeneralSpecs": {
                "ProjectId": {
                    "Name": "RetroSystem",
                    "GUID": "12345678-1234-1234-1234-123456789012"
                },
                "Size": {
                    "X": board_params["width"],
                    "Y": board_params["height"]
                },
                "LayerNumber": board_params["layers"],
                "BoardThickness": board_params.get("thickness", 1.6),
                "Finish": "HAL"
            },
            "FilesAttributes": [
                {
                    "Path": os.path.basename(f),
                    "FileFunction": self._get_file_function(f),
                    "FilePolarity": "Positive"
                } for f in file_list if f.endswith('.gbr')
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(job_data, f, indent=2)
    
    def _get_file_function(self, filename):
        """Determine file function from filename"""
        basename = os.path.basename(filename)
        if "F.Cu" in basename:
            return "Copper,L1,Top"
        elif "B.Cu" in basename:
            return "Copper,L2,Bot"
        elif "F.Mask" in basename:
            return "Soldermask,Top"
        elif "B.Mask" in basename:
            return "Soldermask,Bot"
        elif "F.SilkS" in basename:
            return "Legend,Top"
        elif "Edge.Cuts" in basename:
            return "Profile,NP"
        else:
            return "Other"


class DrillExporter:
    """Exports drill files for PCB manufacturing"""
    
    def export_drill_file(self, scene, filename, drill_params=None):
        """Export drill file in Excellon format"""
        if drill_params is None:
            drill_params = {
                "drill_size": 0.8,  # mm
                "via_size": 0.4     # mm
            }
        
        components = [item for item in scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        
        with open(filename, 'w') as f:
            # Excellon header
            f.write("M48\n")  # Beginning of header
            f.write("METRIC,TZ\n")  # Metric units, trailing zeros
            f.write("FMAT,2\n")  # Format
            f.write("ICI,OFF\n")  # Incremental coordinate input off
            
            # Tool definitions
            f.write("T01C0.8\n")  # Tool 1: 0.8mm for component holes
            f.write("T02C0.4\n")  # Tool 2: 0.4mm for vias
            f.write("%\n")        # End of header
            
            # Drill data
            f.write("T01\n")      # Select tool 1
            
            # Drill holes for component pins
            for component in components:
                if hasattr(component, 'pin_points'):
                    package_type = getattr(component.component_def, 'package_type', 'DIP-40')
                    
                    # Only drill holes for through-hole components
                    if not package_type.startswith(('SOIC', 'QFP', 'BGA', 'PLCC')):
                        for pin_name, pin in component.pin_points.items():
                            pos = pin.get_scene_pos()
                            x_coord = pos.x() * 1000  # Convert to microns
                            y_coord = pos.y() * 1000
                            
                            f.write(f"X{x_coord:06.0f}Y{y_coord:06.0f}\n")
            
            # Add any vias (if implemented)
            # f.write("T02\n")  # Select tool 2 for vias
            # ... via drilling code would go here
            
            f.write("M30\n")  # End of program
        
        return filename


class PickPlaceExporter:
    """Exports pick and place files for automated assembly"""
    
    def export_pick_place(self, scene, filename, side="top"):
        """Export pick and place file in CSV format"""
        components = [item for item in scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # CSV header
            writer.writerow([
                'Designator',
                'Val',
                'Package',
                'Mid X',
                'Mid Y',
                'Rotation',
                'Layer'
            ])
            
            # Component data
            for i, component in enumerate(components, 1):
                # Get component position (center)
                pos = component.pos()
                center_x = pos.x() + component.rect().width() / 2
                center_y = pos.y() + component.rect().height() / 2
                
                # Get component properties
                ref_des = getattr(component, 'reference_designator', f'U{i}')
                value = getattr(component, 'value', component.name)
                package_type = getattr(component.component_def, 'package_type', 'DIP-40')
                rotation = component.rotation()
                
                # Determine if component should be on this side
                mount_type = "Through-hole"
                if package_type.startswith(('SOIC', 'QFP', 'BGA', 'PLCC')):
                    mount_type = "Surface Mount"
                
                # Only include surface mount components for pick & place
                if mount_type == "Surface Mount":
                    writer.writerow([
                        ref_des,
                        value,
                        package_type,
                        f"{center_x:.3f}mm",
                        f"{center_y:.3f}mm",
                        f"{rotation:.1f}",
                        side.title()
                    ])
        
        return filename


class BOMExporter:
    """Exports Bill of Materials in various formats"""
    
    def export_bom_csv(self, scene, filename):
        """Export BOM as CSV file"""
        components = [item for item in scene.items() 
                     if isinstance(item, EnhancedHardwareComponent)]
        
        # Count components by type
        component_counts = {}
        for component in components:
            key = (
                component.name,
                getattr(component.component_def, 'package_type', 'DIP-40'),
                getattr(component, 'value', '')
            )
            
            if key not in component_counts:
                component_counts[key] = {
                    'count': 0,
                    'designators': [],
                    'component': component
                }
            
            component_counts[key]['count'] += 1
            ref_des = getattr(component, 'reference_designator', f'U{len(component_counts[key]["designators"])+1}')
            component_counts[key]['designators'].append(ref_des)
        
        # Write CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow([
                'Item',
                'Quantity',
                'Designators',
                'Part Number',
                'Description',
                'Package',
                'Value',
                'Manufacturer',
                'Unit Cost',
                'Total Cost'
            ])
            
            # Data rows
            total_cost = 0.0
            for i, ((name, package, value), data) in enumerate(component_counts.items(), 1):
                component = data['component']
                quantity = data['count']
                designators = ', '.join(data['designators'])
                
                # Get additional properties if available
                manufacturer = getattr(component, 'manufacturer', '')
                part_number = getattr(component, 'part_number', '')
                unit_cost = getattr(component, 'unit_cost', 0.0)
                line_cost = quantity * unit_cost
                total_cost += line_cost
                
                writer.writerow([
                    i,
                    quantity,
                    designators,
                    part_number,
                    name,
                    package,
                    value,
                    manufacturer,
                    f"${unit_cost:.2f}" if unit_cost > 0 else "",
                    f"${line_cost:.2f}" if line_cost > 0 else ""
                ])
            
            # Total row
            writer.writerow([])
            writer.writerow(['', '', '', '', '', '', '', 'TOTAL:', '', f"${total_cost:.2f}"])
        
        return filename, total_cost
    
    def export_bom_html(self, scene, filename):
        """Export BOM as HTML file with enhanced formatting"""
        csv_filename = filename.replace('.html', '.csv')
        csv_file, total_cost = self.export_bom_csv(scene, csv_filename)
        
        # Generate HTML from CSV data
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Bill of Materials</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        .total {{ background-color: #e8f4fd; font-weight: bold; }}
        .header {{ margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Bill of Materials</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Components: {len([item for item in scene.items() if isinstance(item, EnhancedHardwareComponent)])}</p>
        <p><strong>Total Cost: ${total_cost:.2f}</strong></p>
    </div>
"""
        
        # Read CSV and convert to HTML table
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            html_content += "<table>\n"
            
            for i, row in enumerate(csv_reader):
                if i == 0:  # Header row
                    html_content += "<tr>"
                    for cell in row:
                        html_content += f"<th>{cell}</th>"
                    html_content += "</tr>\n"
                elif len(row) > 0 and row[0]:  # Data rows
                    css_class = "total" if "TOTAL" in str(row) else ""
                    html_content += f"<tr class='{css_class}'>"
                    for cell in row:
                        html_content += f"<td>{cell}</td>"
                    html_content += "</tr>\n"
            
            html_content += "</table>\n</body>\n</html>"
        
        # Write HTML file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Clean up temporary CSV file
        os.remove(csv_filename)
        
        return filename


class ManufacturingExportManager:
    """Manages all manufacturing exports"""
    
    def __init__(self):
        self.gerber_exporter = GerberExporter()
        self.drill_exporter = DrillExporter()
        self.pickplace_exporter = PickPlaceExporter()
        self.bom_exporter = BOMExporter()
    
    def export_complete_manufacturing_package(self, scene, output_dir, board_params=None):
        """Export complete manufacturing package"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        exported_files = []
        
        try:
            # Export Gerber files
            gerber_files = self.gerber_exporter.export_gerber_files(scene, output_dir, board_params)
            exported_files.extend(gerber_files)
            
            # Export drill file
            drill_file = os.path.join(output_dir, "PCB-PTH.drl")
            self.drill_exporter.export_drill_file(scene, drill_file)
            exported_files.append(drill_file)
            
            # Export pick & place files
            pnp_top_file = os.path.join(output_dir, "PCB-top-pos.csv")
            self.pickplace_exporter.export_pick_place(scene, pnp_top_file, "top")
            exported_files.append(pnp_top_file)
            
            pnp_bottom_file = os.path.join(output_dir, "PCB-bottom-pos.csv")
            self.pickplace_exporter.export_pick_place(scene, pnp_bottom_file, "bottom")
            exported_files.append(pnp_bottom_file)
            
            # Export BOM
            bom_csv_file = os.path.join(output_dir, "PCB-BOM.csv")
            bom_html_file = os.path.join(output_dir, "PCB-BOM.html")
            self.bom_exporter.export_bom_csv(scene, bom_csv_file)
            self.bom_exporter.export_bom_html(scene, bom_html_file)
            exported_files.extend([bom_csv_file, bom_html_file])
            
            # Create README file
            readme_file = os.path.join(output_dir, "README.txt")
            self._create_readme_file(exported_files, readme_file, board_params)
            exported_files.append(readme_file)
            
            return exported_files
            
        except Exception as e:
            raise Exception(f"Manufacturing export failed: {str(e)}")
    
    def _create_readme_file(self, file_list, readme_file, board_params):
        """Create README file explaining the manufacturing package"""
        with open(readme_file, 'w') as f:
            f.write("MANUFACTURING PACKAGE\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Software: Visual Retro System Emulator Builder - Enhanced\n\n")
            
            if board_params:
                f.write("BOARD SPECIFICATIONS:\n")
                f.write("-" * 20 + "\n")
                f.write(f"Size: {board_params.get('width', 100)} x {board_params.get('height', 80)} mm\n")
                f.write(f"Layers: {board_params.get('layers', 2)}\n")
                f.write(f"Thickness: {board_params.get('thickness', 1.6)} mm\n\n")
            
            f.write("INCLUDED FILES:\n")
            f.write("-" * 15 + "\n")
            
            for file_path in file_list:
                filename = os.path.basename(file_path)
                if filename.endswith('.gbr'):
                    f.write(f"{filename:<25} - Gerber file\n")
                elif filename.endswith('.drl'):
                    f.write(f"{filename:<25} - Drill file\n")
                elif filename.endswith('-pos.csv'):
                    f.write(f"{filename:<25} - Pick & place file\n")
                elif filename.endswith('BOM.csv'):
                    f.write(f"{filename:<25} - Bill of materials (CSV)\n")
                elif filename.endswith('BOM.html'):
                    f.write(f"{filename:<25} - Bill of materials (HTML)\n")
                elif filename.endswith('.gbrjob'):
                    f.write(f"{filename:<25} - Gerber job file\n")
            
            f.write("\nMANUFACTURING NOTES:\n")
            f.write("-" * 18 + "\n")
            f.write("- All Gerber files are in RS-274X format\n")
            f.write("- Drill file is in Excellon format\n")
            f.write("- Coordinates are in millimeters\n")
            f.write("- Board finish: HASL (Hot Air Solder Leveling)\n")
            f.write("- Solder mask: Green\n")
            f.write("- Silkscreen: White\n\n")
            
            f.write("For questions about this design, please contact the designer.\n")

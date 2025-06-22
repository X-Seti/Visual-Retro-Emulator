
    def _apply_dark_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QDockWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                color: #ffffff;
                titlebar-close-icon: url();
                titlebar-normal-icon: url();
            }
            QDockWidget::title {
                background-color: #3a3a3a;
                color: #ffffff;
                padding: 5px;
                border: 1px solid #555555;
            }
            QTreeWidget {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                selection-background-color: #0078d4;
            }
            QPushButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #606060;
            }
            QPushButton:checked {
                background-color: #0078d4;
            }
            QComboBox {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 3px;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #666666;
                background-color: #404040;
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
            }
            QRadioButton {
                color: #ffffff;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #666666;
                background-color: #404040;
                border-radius: 8px;
            }
            QRadioButton::indicator:checked {
                background-color: #0078d4;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #666666;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QSlider {
                background-color: transparent;
            }
            QSlider::groove:horizontal {
                border: 1px solid #666666;
                height: 8px;
                background-color: #404040;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background-color: #0078d4;
                border: 1px solid #666666;
                width: 16px;
                height: 16px;
                border-radius: 8px;
                margin: -4px 0;
            }
            QSpinBox {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 3px;
                border-radius: 3px;
            }
            QMenuBar {
                background-color: #3a3a3a;
                color: #ffffff;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #0078d4;
            }
            QMenu {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0078d4;
            }
            QToolBar {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                spacing: 3px;
            }
            QToolButton {
                background-color: #404040;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 3px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #505050;
            }
            QToolButton:pressed {
                background-color: #606060;
            }
            QToolButton:checked {
                background-color: #0078d4;
            }
            QStatusBar {
                background-color: #3a3a3a;
                color: #ffffff;
                border-top: 1px solid #555555;
            }
            QProgressBar {
                border: 1px solid #666666;
                border-radius: 3px;
                text-align: center;
                background-color: #404040;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
            QTextEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2a2a2a;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 5px 10px;
                border: 1px solid #666666;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
        """)

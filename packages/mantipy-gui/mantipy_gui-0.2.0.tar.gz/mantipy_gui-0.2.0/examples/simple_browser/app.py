#!/usr/bin/env python3
"""
Simple browser example using mantipy-gui

This example demonstrates a basic web browser with tabs using mantipy-gui.
"""

import sys
import os

# Fix QtWebEngine initialization
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
if not QApplication.instance():
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    # Force import of QtWebEngineWidgets
    from PyQt5 import QtWebEngineWidgets

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mantipy_gui import Window, BrowserView, Console
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget


def main():
    """Run the simple browser example"""
    # Create a window
    app = Window(title="Simple Browser", width=1200, height=800)
    
    # Apply Material Design theme
    app._apply_theme("material")
    
    # Create a console for logging
    console = Console(height=100)
    
    # Create a browser view
    browser = BrowserView(home_url="https://google.com")
    
    # Create an address bar widget
    address_widget = QWidget()
    address_widget.setObjectName("addressBar")
    address_layout = QHBoxLayout()
    address_layout.setContentsMargins(8, 8, 8, 8)
    address_layout.setSpacing(8)
    address_widget.setLayout(address_layout)
    
    # Create an address bar
    address_bar = QLineEdit()
    address_bar.setPlaceholderText("Enter URL...")
    address_bar.returnPressed.connect(lambda: load_url(address_bar.text()))
    address_bar.setObjectName("urlInput")
    
    # Create a go button
    go_button = QPushButton("Go")
    go_button.setObjectName("goButton")
    go_button.clicked.connect(lambda: load_url(address_bar.text()))
    
    # Add to address layout
    address_layout.addWidget(address_bar)
    address_layout.addWidget(go_button)
    
    # Add custom styling for address bar
    address_widget.setStyleSheet("""
        #addressBar {
            background: white;
            border-bottom: 1px solid #E0E0E0;
        }
        #urlInput {
            font-size: 14px;
        }
        #goButton {
            min-width: 80px;
        }
    """)
    
    # Add address bar to window
    app.central_layout.insertWidget(0, address_widget)
    
    # Function to load URLs
    def load_url(url):
        """Load a URL in the browser"""
        browser.load(url)
        console.log(f"Loading URL: {url}")
        
    # Function to update address bar when URL changes
    def update_address(url):
        """Update the address bar when the URL changes"""
        address_bar.setText(url)
        console.log(f"URL changed to: {url}")
        
    # Connect URL changed signal
    browser.current_tab().urlChanged.connect(update_address)
    
    # Add views to the window
    app.add_view(browser, "central")
    app.add_view(console, "bottom")
    
    # Set initial status
    app.set_status("Ready")
    console.log("Simple Browser initialized")
    
    # Run the application
    app.window.show()
    return 0


if __name__ == "__main__":
    # Create QApplication instance if running as main script
    if not QApplication.instance():
        app = QApplication(sys.argv)
        sys.exit(main())
    else:
        main() 
#!/usr/bin/env python3
"""
IPFS browser example using mantipy-gui

This example demonstrates a browser that can resolve ipfs:// URLs.
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

from mantipy_gui import Window, BrowserView, Console, SidePanel


def main():
    """Run the IPFS browser example"""
    # Create a window
    app = Window(title="IPFS Browser", width=1200, height=800)
    
    # Apply Material Design theme
    app._apply_theme("material")
    
    # Create a browser view
    browser = BrowserView(home_url="about:blank")
    
    # Register IPFS resolver
    @browser.resolver("ipfs://")
    def resolve_ipfs(url):
        # Extract IPFS hash
        hash_part = url.replace("ipfs://", "")
        gateway_url = f"https://ipfs.io/ipfs/{hash_part}"
        console.log(f"IPFS URL {url} -> {gateway_url}")
        return gateway_url
    
    # Create a console for logging
    console = Console(height=150)
    
    # Create a side panel for IPFS hashes
    sidebar = SidePanel(title="IPFS Examples", width=280)
    sidebar.widget.setObjectName("ipfsSidebar")
    
    # Add some example IPFS hashes
    from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QFrame
    
    # Add header with Material Design styling
    header = QLabel("Browse IPFS Content")
    header.setObjectName("sidebarHeader")
    header.setStyleSheet("""
        #sidebarHeader {
            font-size: 20px;
            font-weight: 500;
            color: #1976D2;
            padding: 16px;
            border-bottom: 1px solid #E0E0E0;
        }
    """)
    sidebar.add_widget(header)
    
    # Add IPFS hash input with Material Design styling
    input_container = QWidget()
    input_container.setObjectName("inputContainer")
    input_layout = QHBoxLayout()
    input_layout.setContentsMargins(16, 16, 16, 16)
    input_layout.setSpacing(8)
    input_container.setLayout(input_layout)
    
    hash_input = QLineEdit()
    hash_input.setObjectName("hashInput")
    hash_input.setPlaceholderText("Enter IPFS hash...")
    
    go_btn = QPushButton("Go")
    go_btn.setObjectName("goButton")
    go_btn.clicked.connect(lambda: (
        browser.load(f"ipfs://{hash_input.text().strip()}"),
        console.log(f"Loading IPFS hash: {hash_input.text().strip()}")
    ))
    
    input_layout.addWidget(hash_input)
    input_layout.addWidget(go_btn)
    
    # Style the input container
    input_container.setStyleSheet("""
        #inputContainer {
            background: white;
            border-radius: 8px;
            margin: 8px;
        }
        #hashInput {
            font-size: 14px;
        }
        #goButton {
            min-width: 80px;
        }
    """)
    
    sidebar.add_widget(input_container)
    
    # Add divider
    divider = QFrame()
    divider.setFrameShape(QFrame.HLine)
    divider.setObjectName("divider")
    divider.setStyleSheet("""
        #divider {
            background: #E0E0E0;
            margin: 8px 16px;
        }
    """)
    sidebar.add_widget(divider)
    
    # Add example heading
    example_header = QLabel("Example IPFS Content")
    example_header.setObjectName("exampleHeader")
    example_header.setStyleSheet("""
        #exampleHeader {
            font-size: 16px;
            font-weight: 500;
            color: #424242;
            padding: 16px;
        }
    """)
    sidebar.add_widget(example_header)
    
    # Add some example IPFS hashes with Material Design styling
    example_hashes = [
        ("HTML Example", "QmYKnSuZPz3K3qj9Nh9yYwns5qWKWzGXsVZjLYqPNrZ5Pe"),
        ("Image Example", "QmRFDCmFxnuXRSyD2KRZbz57XgqL9hZhH7KDJbPKVWHxcQ"),
        ("Text Example", "QmXV2R4mfHDYbx54XJZZDHzGcg7EjT4cMRzANz8NqwjcLY"),
    ]
    
    for name, hash_value in example_hashes:
        btn = QPushButton(name)
        btn.setObjectName("exampleButton")
        btn.setStyleSheet("""
            #exampleButton {
                text-align: left;
                padding: 12px 16px;
                margin: 4px 16px;
                border-radius: 4px;
                background: white;
                color: #1976D2;
                border: 1px solid #E0E0E0;
            }
            #exampleButton:hover {
                background: #E3F2FD;
                border-color: #2196F3;
            }
        """)
        btn.clicked.connect(lambda _, h=hash_value: (
            browser.load(f"ipfs://{h}"),
            console.log(f"Loading IPFS hash: {h}")
        ))
        sidebar.add_widget(btn)
    
    # Add explanation with Material Design styling
    note = QLabel(
        "This browser can load content from IPFS using the ipfs:// protocol. "
        "It resolves IPFS hashes to the IPFS.io gateway. "
        "Enter an IPFS hash above or click one of the examples."
    )
    note.setObjectName("explanationText")
    note.setWordWrap(True)
    note.setStyleSheet("""
        #explanationText {
            color: #757575;
            padding: 16px;
            font-size: 14px;
            line-height: 1.5;
        }
    """)
    sidebar.add_widget(note)
    
    # Style the sidebar
    sidebar.widget.setStyleSheet("""
        #ipfsSidebar {
            background: #FAFAFA;
            border-right: 1px solid #E0E0E0;
        }
    """)
    
    # Add URL changed handler
    def log_url_changed(url):
        console.log(f"Loaded URL: {url}")
        app.set_status(f"Current URL: {url}")
    
    browser.current_tab().urlChanged.connect(log_url_changed)
    
    # Add views to the window
    app.add_view(browser, "central")
    app.add_view(console, "bottom")
    app.add_view(sidebar, "left")
    
    # Set initial status
    app.set_status("Ready")
    console.log("IPFS Browser initialized")
    
    # Load welcome page with Material Design styling
    welcome_html = """
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #FAFAFA;
                color: #212121;
            }
            .container { 
                max-width: 800px;
                margin: 0 auto;
                padding: 32px;
            }
            h1 { 
                color: #1976D2;
                font-size: 32px;
                font-weight: 500;
                margin-bottom: 24px;
            }
            .card { 
                background: white;
                border-radius: 8px;
                padding: 24px;
                margin: 16px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h2 { 
                color: #1976D2;
                font-size: 24px;
                font-weight: 500;
                margin-top: 0;
            }
            p { 
                color: #424242;
                line-height: 1.6;
                margin: 16px 0;
            }
            .highlight {
                background: #E3F2FD;
                color: #1976D2;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the IPFS Browser</h1>
            <div class="card">
                <h2>IPFS Integration</h2>
                <p>This browser can load content from the InterPlanetary File System (IPFS) using the <span class="highlight">ipfs://</span> protocol.</p>
                <p>The IPFS protocol allows content-addressed storage and retrieval, where files are identified by their content rather than location.</p>
            </div>
            <div class="card">
                <h2>How to Use</h2>
                <p>1. Enter an IPFS hash in the sidebar</p>
                <p>2. Click Go or try one of the example hashes</p>
                <p>3. Content will be loaded from the IPFS.io gateway</p>
            </div>
        </div>
    </body>
    </html>
    """
    browser.load_html(welcome_html)
    
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
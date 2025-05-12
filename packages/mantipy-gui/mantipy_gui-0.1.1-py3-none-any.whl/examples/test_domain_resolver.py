#!/usr/bin/env python3
"""
Test script to verify domain resolution fixes
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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mantipy_gui import Window, BrowserView, Console, SidePanel
from evrmore_rpc import EvrmoreClient


def resolve_evr_domain(domain):
    """Resolve an EVR domain to a URL using the Evrmore RPC client"""
    print(f"Resolving domain: {domain} (original format)")
    
    # Handle http:// format
    if domain.startswith('http://'):
        domain = domain.replace('http://', '').rstrip('/')
        print(f"  Converted to: {domain}")
    
    # Extract the asset name from the domain
    asset_name = domain.upper().replace(".EVR", "")
    print(f"  Asset name: {asset_name}")
    
    try:
        # Use the Evrmore client to get asset data
        client = EvrmoreClient()
        asset_data = client.getassetdata(asset_name)
        
        # Check if we have an IPFS hash
        if asset_data and 'ipfs_hash' in asset_data and asset_data['ipfs_hash']:
            ipfs_hash = asset_data['ipfs_hash']
            print(f"  Found IPFS hash: {ipfs_hash}")
            return f"https://ipfs.io/ipfs/{ipfs_hash}"
        else:
            print(f"  No IPFS hash found")
            return f"about:blank?error=no_ipfs_hash&domain={domain}"
    except Exception as e:
        print(f"  Error resolving: {e}")
        return f"about:blank?error={str(e)}&domain={domain}"


def main():
    """Run the domain resolver test"""
    # Create a window
    app = Window(title="Domain Resolver Test", width=1200, height=800)
    
    # Create a browser view
    browser = BrowserView(home_url="about:blank")
    
    # Register EVR resolver for both formats
    @browser.resolver(".evr")
    def resolve_evr(domain):
        print(f"TLD Resolver called with: {domain}")
        return resolve_evr_domain(domain)
    
    @browser.resolver("http://")
    def resolve_http(url):
        if url.lower().endswith('.evr/') or url.lower().endswith('.evr'):
            print(f"HTTP Resolver called with: {url}")
            return resolve_evr_domain(url)
        return url
    
    # Create a console for logging
    console = Console(height=300)
    
    # Create a side panel for test cases
    sidebar = SidePanel(title="Test Cases", width=250)
    
    # Add test buttons
    from PyQt5.QtWidgets import QPushButton, QLabel
    
    header = QLabel("Domain Resolution Test")
    header.setStyleSheet("font-weight: bold; font-size: 16px;")
    sidebar.add_widget(header)
    
    # Add test cases
    test_cases = [
        ("Standard Format", "chess.evr"),
        ("URL Format", "http://chess.evr"),
        ("URL Format with Slash", "http://chess.evr/"),
        ("Mixed Case", "CHess.EVR"),
        ("Custom Domain", "manticore.evr"),
    ]
    
    for name, domain in test_cases:
        btn = QPushButton(name)
        btn.clicked.connect(lambda _, d=domain: (
            browser.load(d),
            console.log(f"Testing domain: {d}")
        ))
        sidebar.add_widget(btn)
    
    # Add direct input
    from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QWidget
    
    input_container = QWidget()
    input_layout = QHBoxLayout()
    input_container.setLayout(input_layout)
    
    domain_input = QLineEdit()
    domain_input.setPlaceholderText("Enter domain to test...")
    
    test_btn = QPushButton("Test")
    test_btn.clicked.connect(lambda: (
        browser.load(domain_input.text().strip()),
        console.log(f"Testing custom input: {domain_input.text().strip()}")
    ))
    
    input_layout.addWidget(domain_input)
    input_layout.addWidget(test_btn)
    
    sidebar.add_widget(input_container)
    
    # Add explanation
    note = QLabel(
        "This test app verifies that domain resolution works properly with "
        "different formats. It should handle both 'domain.evr' and "
        "'http://domain.evr' formats correctly."
    )
    note.setWordWrap(True)
    sidebar.add_widget(note)
    
    # Add views to the window
    app.add_view(browser, "central")
    app.add_view(console, "bottom")
    app.add_view(sidebar, "left")
    
    # Set initial status
    app.set_status("Ready")
    console.log("Domain Resolver Test initialized")
    
    # Create initial HTML
    welcome_html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; color: #333; }
            h1 { color: #5c2b8a; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #f5f5f5; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Domain Resolver Test</h1>
            <div class="card">
                <h2>Test Instructions</h2>
                <p>Click on a test case in the sidebar to verify domain resolution.</p>
                <p>The console will show detailed information about the resolution process.</p>
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
    if not QApplication.instance():
        app = QApplication(sys.argv)
        sys.exit(main())
    else:
        main() 
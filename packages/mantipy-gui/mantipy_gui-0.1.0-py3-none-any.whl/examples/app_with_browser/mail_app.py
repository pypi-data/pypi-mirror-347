#!/usr/bin/env python3
"""
EvrMail app example with hidden browser feature
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
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QStackedWidget, QLineEdit, QFrame, QSplitter, QTreeWidget, QTreeWidgetItem
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize

# Import evrmore_rpc for domain resolution
from evrmore_rpc import EvrmoreClient

# Import the server module
from . import server


class EvrMailApp:
    """EvrMail application with integrated browser capabilities"""
    
    def __init__(self):
        # Start the local server for serving web content
        self.local_server = server.start_server()
        
        # Create the main application window
        self.app_window = Window(title="EvrMail", width=1000, height=700)
        
        # Create main layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        
        # Create different pages
        self.home_widget = self.create_home_widget()
        self.inbox_widget = self.create_inbox_widget()
        self.compose_widget = self.create_compose_widget()
        
        # Create browser (hidden)
        self.browser_container = QWidget()
        self.browser_layout = QVBoxLayout()
        self.browser_container.setLayout(self.browser_layout)
        self.browser = BrowserView(home_url="about:blank")
        self.browser_layout.addWidget(self.browser.widget)
        
        # Add all pages to stacked widget
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.inbox_widget)
        self.stacked_widget.addWidget(self.compose_widget)
        self.stacked_widget.addWidget(self.browser_container)
        
        # Create console for logging (hidden by default)
        self.console = Console(height=100)
        self.console.widget.setVisible(False)
        
        # Create right panel
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_panel.setLayout(self.right_layout)
        self.right_layout.addWidget(self.stacked_widget)
        self.right_layout.addWidget(self.console.widget)
        
        # Add widgets to main layout
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.right_panel)
        
        # Set sidebar width
        self.sidebar.setFixedWidth(200)
        
        # Add main widget to window
        self.app_window.central_layout.addWidget(self.main_widget)
        
        # Initialize Evrmore client
        self.evrmore_client = EvrmoreClient()
        
        # Log startup
        self.console.log("EvrMail initialized")
        self.console.log(f"Local server running at http://localhost:{server.PORT}")
        self.console.log("Evrmore client initialized for .evr domain resolution")
        
        # Register custom domain resolver for .evr domains
        @self.browser.resolver(".evr")
        def resolve_evr(domain):
            # Extract the asset name from the domain
            asset_name = domain.upper().replace(".EVR", "")
            self.console.log(f"Resolving EVR domain: {domain} (Asset: {asset_name})")
            
            try:
                # Handle special case for our local mail demo
                if asset_name == "MAIL":
                    return f"http://localhost:{server.PORT}/index.html"
                
                # Get the asset data using evrmore_rpc
                asset_data = self.evrmore_client.getassetdata(asset_name)
                
                # Check if we have an IPFS hash and return it
                if asset_data and 'ipfs_hash' in asset_data and asset_data['ipfs_hash']:
                    ipfs_hash = asset_data['ipfs_hash']
                    self.console.log(f"Found IPFS hash for {asset_name}: {ipfs_hash}")
                    return f"https://ipfs.io/ipfs/{ipfs_hash}"
                else:
                    self.console.log(f"No IPFS hash found for {asset_name}")
                    return f"about:blank?error=no_ipfs_hash&domain={domain}"
            except Exception as e:
                self.console.log(f"Error resolving {domain}: {str(e)}")
                return f"about:blank?error={str(e)}&domain={domain}"
        
        # Also register http://domain.evr format
        @self.browser.resolver("http://")
        def resolve_http(url):
            if url.lower().endswith('.evr/') or url.lower().endswith('.evr'):
                # Extract domain part from URL
                domain = url.replace('http://', '').rstrip('/')
                self.console.log(f"Converting URL format: {url} to domain: {domain}")
                # Extract the asset name from the domain
                asset_name = domain.upper().replace(".EVR", "")
                
                try:
                    # Handle special case for our local mail demo
                    if asset_name == "MAIL":
                        return f"http://localhost:{server.PORT}/index.html"
                    
                    # Get the asset data using evrmore_rpc
                    asset_data = self.evrmore_client.getassetdata(asset_name)
                    
                    # Check if we have an IPFS hash and return it
                    if asset_data and 'ipfs_hash' in asset_data and asset_data['ipfs_hash']:
                        ipfs_hash = asset_data['ipfs_hash']
                        self.console.log(f"Found IPFS hash for {asset_name}: {ipfs_hash}")
                        return f"https://ipfs.io/ipfs/{ipfs_hash}"
                    else:
                        self.console.log(f"No IPFS hash found for {asset_name}")
                        return f"about:blank?error=no_ipfs_hash&domain={domain}"
                except Exception as e:
                    self.console.log(f"Error resolving {domain}: {str(e)}")
                    return f"about:blank?error={str(e)}&domain={domain}"
            return url  # Not an EVR domain, return as is
        
    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        layout = QVBoxLayout()
        sidebar.setLayout(layout)
        
        # Add app logo/title
        logo_container = QWidget()
        logo_layout = QHBoxLayout()
        logo_container.setLayout(logo_layout)
        
        logo_label = QLabel("✉️")
        logo_label.setFont(QFont("Arial", 24))
        
        app_name = QLabel("EvrMail")
        app_name.setFont(QFont("Arial", 18, QFont.Bold))
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(app_name)
        logo_layout.addStretch()
        
        layout.addWidget(logo_container)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Add navigation buttons
        nav_buttons = [
            ("🏠 Home", lambda: self.show_page(0)),
            ("📥 Inbox", lambda: self.show_page(1)),
            ("✏️ Compose", lambda: self.show_page(2)),
            ("👤 Contacts", lambda: self.console.log("Contacts clicked")),
            ("💰 Wallet", lambda: self.console.log("Wallet clicked")),
            ("🌐 Browser", lambda: self.open_browser("mail.evr")),
            ("⚙️ Settings", lambda: self.console.log("Settings clicked")),
        ]
        
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        # Add EVR domain browse section
        browse_label = QLabel("Browse EVR domains:")
        browse_label.setStyleSheet("margin-top: 20px;")
        layout.addWidget(browse_label)
        
        # Domain input
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("domain.evr")
        layout.addWidget(self.domain_input)
        
        # Go button
        go_btn = QPushButton("Go")
        go_btn.clicked.connect(self.browse_evr_domain)
        layout.addWidget(go_btn)
        
        layout.addStretch()
        
        # Toggle console button
        debug_btn = QPushButton("🛠️ Toggle Logs")
        debug_btn.clicked.connect(self.toggle_console)
        layout.addWidget(debug_btn)
        
        # Add version at bottom
        version_label = QLabel("v0.1.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Style the sidebar
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: #1a1a2e;
                color: white;
                border-right: 1px solid #333;
            }
            QPushButton {
                text-align: left;
                padding: 8px;
                border: none;
                border-radius: 3px;
                background-color: transparent;
                color: white;
            }
            QPushButton:hover {
                background-color: #16213e;
            }
            QLabel {
                color: white;
            }
            QFrame {
                background-color: #333;
                height: 1px;
            }
            QLineEdit {
                background-color: #2a2a4a;
                color: white;
                border: 1px solid #444;
                border-radius: 3px;
                padding: 5px;
            }
        """)
        
        return sidebar
    
    def browse_evr_domain(self):
        """Browse to an EVR domain from the input field"""
        domain = self.domain_input.text().strip()
        if not domain:
            return
            
        # Add .evr extension if not present
        if not domain.lower().endswith('.evr'):
            domain = f"{domain}.evr"
            
        self.open_browser(domain)
        
    def create_home_widget(self):
        """Create the home page widget"""
        home = QWidget()
        layout = QVBoxLayout()
        home.setLayout(layout)
        
        # Add welcome heading
        welcome = QLabel("<h1>Welcome to EvrMail</h1>")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        # Add app description
        description = QLabel(
            "<p>Secure Email on Everchain</p>"
            "<p>EvrMail provides decentralized, secure email using blockchain technology.</p>"
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add the logo
        logo = QLabel("✉️")
        logo.setFont(QFont("Arial", 72))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # Add a status message
        status = QLabel("Loading application...")
        status.setAlignment(Qt.AlignCenter)
        layout.addWidget(status)
        
        layout.addStretch()
        
        return home
    
    def create_inbox_widget(self):
        """Create the inbox widget"""
        inbox = QWidget()
        layout = QVBoxLayout()
        inbox.setLayout(layout)
        
        # Add inbox header
        header = QLabel("<h2>Inbox</h2>")
        layout.addWidget(header)
        
        # Create mock email list
        emails = QTreeWidget()
        emails.setHeaderLabels(["From", "Subject", "Date"])
        emails.setColumnWidth(0, 200)
        emails.setColumnWidth(1, 400)
        
        # Add some example emails
        sample_emails = [
            ("alice@evr", "Welcome to EvrMail", "Today"),
            ("bob@evr", "Meeting tomorrow?", "Yesterday"),
            ("charlie@evr", "Project update", "2 days ago"),
            ("dao@evr", "Governance proposal", "3 days ago"),
            ("newsletter@evr", "Weekly blockchain news", "1 week ago"),
        ]
        
        for sender, subject, date in sample_emails:
            item = QTreeWidgetItem([sender, subject, date])
            emails.addTopLevelItem(item)
        
        layout.addWidget(emails)
        
        return inbox
    
    def create_compose_widget(self):
        """Create the compose email widget"""
        compose = QWidget()
        layout = QVBoxLayout()
        compose.setLayout(layout)
        
        # Add compose header
        header = QLabel("<h2>Compose Message</h2>")
        layout.addWidget(header)
        
        # Add form fields
        form_layout = QVBoxLayout()
        
        # To field
        to_layout = QHBoxLayout()
        to_label = QLabel("To:")
        to_label.setFixedWidth(80)
        to_input = QLineEdit()
        to_layout.addWidget(to_label)
        to_layout.addWidget(to_input)
        
        # Subject field
        subject_layout = QHBoxLayout()
        subject_label = QLabel("Subject:")
        subject_label.setFixedWidth(80)
        subject_input = QLineEdit()
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(subject_input)
        
        # Message body
        body_layout = QVBoxLayout()
        body_label = QLabel("Message:")
        body_input = QLineEdit()
        body_input.setFixedHeight(200)
        body_layout.addWidget(body_label)
        body_layout.addWidget(body_input)
        
        # Add all form sections
        form_layout.addLayout(to_layout)
        form_layout.addLayout(subject_layout)
        form_layout.addLayout(body_layout)
        
        # Add send button
        send_btn = QPushButton("Send Message")
        send_btn.clicked.connect(lambda: self.console.log("Message sent (mock)"))
        
        layout.addLayout(form_layout)
        layout.addWidget(send_btn)
        layout.addStretch()
        
        return compose
    
    def show_page(self, index):
        """Show a specific page in the stacked widget"""
        self.stacked_widget.setCurrentIndex(index)
        self.console.log(f"Showing page {index}")
    
    def open_browser(self, url):
        """Open the browser with a specific URL"""
        self.stacked_widget.setCurrentIndex(3)  # Switch to browser page
        self.browser.load(url)
        self.console.log(f"Opening URL in browser: {url}")
    
    def toggle_console(self):
        """Toggle console visibility"""
        current = self.console.widget.isVisible()
        self.console.widget.setVisible(not current)
        self.console.log("Console visibility toggled")


def main():
    """Run the EvrMail app example"""
    # Create the application
    app = EvrMailApp()
    
    # Show the window
    app.app_window.window.show()
    
    # Return success code
    return 0


if __name__ == "__main__":
    # Create QApplication instance if running as main script
    if not QApplication.instance():
        app = QApplication(sys.argv)
        sys.exit(main())
    else:
        main() 
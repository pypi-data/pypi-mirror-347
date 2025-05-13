#!/usr/bin/env python3
"""
App with integrated browser example using mantipy-gui
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
    QStackedWidget, QLineEdit, QFrame, QSplitter
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize


class AppWithBrowser:
    """An application with an integrated browser that is hidden initially"""
    
    def __init__(self, app_name="EvrApp"):
        # Create the main application window
        self.app_window = Window(title=f"{app_name}", width=1000, height=700)
        
        # Create main layout
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_widget.setLayout(self.main_layout)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.home_widget = self.create_home_widget()
        self.browser_container = QWidget()
        self.browser_layout = QVBoxLayout()
        self.browser_container.setLayout(self.browser_layout)
        
        # Create browser (but don't show it yet)
        self.browser = BrowserView(home_url="about:blank")
        self.browser_layout.addWidget(self.browser.widget)
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.home_widget)
        self.stacked_widget.addWidget(self.browser_container)
        
        # Create console for logging
        self.console = Console(height=100)
        
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
        
        # Log startup
        self.console.log(f"{app_name} initialized")
        
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
        
        logo_label = QLabel("🌐")
        logo_label.setFont(QFont("Arial", 24))
        
        app_name = QLabel("EvrApp")
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
            ("🌐 Browser", lambda: self.show_page(1)),
            ("✉️ Messages", lambda: self.console.log("Messages clicked")),
            ("👤 Contacts", lambda: self.console.log("Contacts clicked")),
            ("💰 Wallet", lambda: self.console.log("Wallet clicked")),
            ("⚙️ Settings", lambda: self.console.log("Settings clicked")),
        ]
        
        for text, callback in nav_buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        
        layout.addStretch()
        
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
        """)
        
        return sidebar
        
    def create_home_widget(self):
        """Create the home page widget"""
        home = QWidget()
        layout = QVBoxLayout()
        home.setLayout(layout)
        
        # Add welcome heading
        welcome = QLabel("<h1>Welcome to EvrApp</h1>")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        # Add app description
        description = QLabel(
            "<p>This is a demo application that integrates a web browser.</p>"
            "<p>Click the Browser button in the sidebar to access the browser.</p>"
        )
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Add quick links section
        links_container = QWidget()
        links_layout = QHBoxLayout()
        links_container.setLayout(links_layout)
        
        # Create some quick link cards
        cards = [
            ("🔍 Search", "Go to Google", "https://google.com"),
            ("💻 Development", "Go to GitHub", "https://github.com"),
            ("🐍 Python", "Visit Python.org", "https://python.org"),
        ]
        
        for icon, title, url in cards:
            card = self.create_card(icon, title, url)
            links_layout.addWidget(card)
        
        layout.addWidget(links_container)
        layout.addStretch()
        
        return home
    
    def create_card(self, icon, title, url):
        """Create a card widget for the home screen"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setFrameShadow(QFrame.Raised)
        
        layout = QVBoxLayout()
        card.setLayout(layout)
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 24))
        icon_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        btn = QPushButton("Open")
        btn.clicked.connect(lambda: self.open_browser_url(url))
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(btn)
        
        # Style the card
        card.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 10px;
                min-height: 180px;
                min-width: 150px;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #5c2b8a;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #7c3aaa;
            }
        """)
        
        return card
    
    def show_page(self, index):
        """Show a specific page in the stacked widget"""
        self.stacked_widget.setCurrentIndex(index)
        if index == 1:  # Browser page
            self.console.log("Browser opened")
    
    def open_browser_url(self, url):
        """Open a URL in the browser and switch to browser page"""
        self.show_page(1)  # Switch to browser page
        self.browser.load(url)
        self.console.log(f"Loading URL: {url}")


def main():
    """Run the app with browser example"""
    # Create the application
    app = AppWithBrowser(app_name="EvrApp")
    
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
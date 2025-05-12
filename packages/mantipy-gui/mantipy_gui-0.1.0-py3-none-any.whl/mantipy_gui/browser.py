"""
Browser components for mantipy-gui
"""

import os
from typing import Optional, Callable, Dict, List, Any, Union

# Fix QtWebEngine initialization
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLineEdit, QPushButton, QToolBar, QStyle, QStyleFactory
)

# Ensure QtWebEngine is properly initialized
if not QApplication.instance():
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Import WebEngine components - this must happen after the QApplication.setAttribute
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from .resolvers import ResolverRegistry
from .themes.material import COLORS, TYPOGRAPHY, ELEVATION


class BrowserTab(QWidget):
    """
    A browser tab widget for mantipy-gui
    
    This represents a single web browser tab with navigation controls.
    """
    
    urlChanged = pyqtSignal(str)
    titleChanged = pyqtSignal(str)
    
    def __init__(self, url=None, parent=None, browser=None):
        """Initialize a browser tab with a QWebEngineView"""
        super().__init__(parent)
        
        self.browser = browser
        self.init_ui()
        
        if url:
            self.load(url)
            
    def init_ui(self):
        """Initialize the browser tab UI"""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add toolbar with URL field
        self.toolbar = QToolBar()
        self.toolbar.setStyleSheet(f"""
            QToolBar {{
                background: {COLORS['grey']['50']};
                border-bottom: 1px solid {COLORS['grey']['300']};
                spacing: 4px;
                padding: 4px;
            }}
            QToolBar QPushButton {{
                min-width: 36px;
                min-height: 36px;
                border-radius: 4px;
                padding: 4px;
                margin: 0 2px;
            }}
            QToolBar QPushButton:hover {{
                background: {COLORS['grey']['200']};
            }}
            QToolBar QLineEdit {{
                min-height: 36px;
                padding: 4px 8px;
                border-radius: 4px;
                border: 1px solid {COLORS['grey']['300']};
                background: white;
                margin: 0 4px;
            }}
            QToolBar QLineEdit:focus {{
                border: 2px solid {COLORS['primary']['500']};
            }}
        """)
        
        # Create URL bar with Material Design styling
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or search...")
        self.url_bar.returnPressed.connect(self.load_url)
        
        # Create navigation buttons with Material Design icons
        self.back_btn = QPushButton("←")
        self.back_btn.setToolTip("Go back")
        self.back_btn.clicked.connect(lambda: self.webview.back())
        
        self.forward_btn = QPushButton("→")
        self.forward_btn.setToolTip("Go forward")
        self.forward_btn.clicked.connect(lambda: self.webview.forward())
        
        self.reload_btn = QPushButton("↻")
        self.reload_btn.setToolTip("Reload page")
        self.reload_btn.clicked.connect(lambda: self.webview.reload())
        
        # Add buttons and URL bar to toolbar
        self.toolbar.addWidget(self.back_btn)
        self.toolbar.addWidget(self.forward_btn)
        self.toolbar.addWidget(self.reload_btn)
        self.toolbar.addWidget(self.url_bar)
        
        # Create web view with Material Design styling
        self.webview = QWebEngineView()
        self.webview.setStyleSheet(f"""
            QWebEngineView {{
                background: white;
                border: none;
            }}
        """)
        self.webview.loadFinished.connect(self.update_url)
        self.webview.titleChanged.connect(self.update_title)
        
        # Add to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.webview)
        
    def update_title(self, title):
        """Handle title changes from the web page"""
        self.titleChanged.emit(title)
        
    def update_url(self):
        """Update the address bar with the current URL"""
        current_url = self.webview.url().toString()
        
        # If current URL bar contains an EVR domain, preserve it
        if hasattr(self, 'url_bar'):
            current_text = self.url_bar.text()
            if '.evr' in current_text.lower():
                print(f"[BrowserTab] Preserving EVR domain in URL bar: {current_text}")
                # Keep the EVR domain visible
                return
                
        # For regular URLs, update the address bar
        if hasattr(self, 'url_bar'):
            self.url_bar.setText(current_url)
        
    def load(self, url):
        """Load a URL in the browser view"""
        print(f"[BrowserTab] Loading URL: {url}")
        
        # Ensure we have a string URL
        if isinstance(url, QUrl):
            url_str = url.toString()
        else:
            url_str = url
            
        # Save original URL for display in address bar
        original_url = url_str
        print(f"[BrowserTab] Original URL (for display): {original_url}")
        
        # Direct handling for IPFS URLs (convert to gateway)
        if url_str.startswith('ipfs://'):
            ipfs_hash = url_str.replace('ipfs://', '')
            gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
            print(f"[BrowserTab] Converting IPFS URL to gateway: {gateway_url}")
            self.webview.setUrl(QUrl(gateway_url))
            if hasattr(self, 'url_bar'):
                self.url_bar.setText(original_url)  # Show the original ipfs:// URL
            return
            
        # Normalize the URL
        if not url_str.startswith(('http://', 'https://', 'file://', 'data:', 'about:', 'ipfs://')):
            url_str = f"http://{url_str}"
            original_url = url_str  # Update original after normalization
        
        print(f"[BrowserTab] Normalized URL: {url_str}")
        
        # Try to resolve the URL using registered resolvers
        if hasattr(self.browser, 'resolvers'):
            resolved_url = self.browser.resolvers.resolve(url_str)
            print(f"[BrowserTab] Resolved URL: {resolved_url}")
            
            # If the URL was resolved to something different, use that
            if resolved_url != url_str:
                print(f"[BrowserTab] Using resolved URL: {resolved_url}")
                
                # Handle IPFS URLs from resolvers
                if resolved_url.startswith('ipfs://'):
                    ipfs_hash = resolved_url.replace('ipfs://', '')
                    gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
                    print(f"[BrowserTab] Converting resolved IPFS URL to gateway: {gateway_url}")
                    self.webview.setUrl(QUrl(gateway_url))
                else:
                    # Load the resolved URL into the web view
                    self.webview.setUrl(QUrl(resolved_url))
                    
                # Update the address bar with the original URL (for user experience)
                if hasattr(self, 'url_bar'):
                    # Check if this is an EVR domain and keep it in the URL bar
                    if '.evr' in original_url.lower():
                        print(f"[BrowserTab] Keeping EVR domain in URL bar: {original_url}")
                        self.url_bar.setText(original_url)
                    else:
                        # For non-EVR domains, show the resolved URL
                        self.url_bar.setText(resolved_url)
                return
        
        # If we didn't resolve to a different URL, load the original
        self.webview.setUrl(QUrl(url_str))
        if hasattr(self, 'url_bar'):
            self.url_bar.setText(original_url)
        
    def load_url(self):
        """Load the URL from the address bar"""
        url = self.url_bar.text()
        self.load(url)
        
    def load_html(self, html: str, base_url: str = ""):
        """Load HTML content directly"""
        self.webview.setHtml(html, QUrl(base_url))
        
    def execute_js(self, script: str, callback: Optional[Callable] = None):
        """Execute JavaScript in the page"""
        if callback:
            self.webview.page().runJavaScript(script, callback)
        else:
            self.webview.page().runJavaScript(script)
            
    def stop_loading(self):
        """Stop loading the current page"""
        self.webview.stop()


class BrowserView(QWidget):
    """A browser view with tabs"""
    
    def __init__(self, home_url="about:blank", parent=None):
        """Initialize a browser view with tabs"""
        super().__init__(parent)
        
        # Initialize resolver registry
        from mantipy_gui.resolvers.base import ResolverRegistry
        self.resolvers = ResolverRegistry()
        self.resolver_registry = self.resolvers  # For backwards compatibility
        
        # For backwards compatibility (self.widget refers to self)
        self.widget = self
        
        # Initialize UI
        self.init_ui()
        
        # Create first tab with home URL
        self.add_tab(home_url)
        
    def init_ui(self):
        """Initialize the browser view UI"""
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget with Material Design styling
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background: white;
            }}
            QTabBar::tab {{
                background: {COLORS['grey']['200']};
                color: {COLORS['grey']['700']};
                padding: 8px 16px;
                border-radius: 4px 4px 0 0;
                margin: 2px 2px 0 2px;
                min-height: 36px;
                font-size: {TYPOGRAPHY['font_sizes']['button']};
            }}
            QTabBar::tab:selected {{
                background: {COLORS['primary']['500']};
                color: white;
                box-shadow: {ELEVATION['2']};
            }}
            QTabBar::tab:hover:!selected {{
                background: {COLORS['grey']['300']};
            }}
            QTabBar::close-button {{
                image: url(close.png);
                subcontrol-position: right;
                margin: 4px;
            }}
            QTabBar::close-button:hover {{
                background: {COLORS['grey']['400']};
                border-radius: 2px;
            }}
        """)
        
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Add new tab button with Material Design styling
        new_tab_btn = self._create_new_tab_button()
        new_tab_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']['500']};
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 24px;
                min-height: 24px;
                font-size: 16px;
                font-weight: bold;
                margin: 4px;
            }}
            QPushButton:hover {{
                background: {COLORS['primary']['600']};
            }}
        """)
        self.tabs.setCornerWidget(new_tab_btn)
        
        # Add to layout
        layout.addWidget(self.tabs)
        
    def _create_new_tab_button(self):
        """Create a new tab button for the tab corner"""
        btn = QPushButton("+")
        btn.setMaximumSize(24, 24)
        btn.clicked.connect(lambda: self.add_tab())
        return btn
        
    def add_tab(self, url=None):
        """Add a new browser tab"""
        # Create the tab
        tab = BrowserTab(url=url, parent=self, browser=self)
        
        # Add to tab widget
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        # Connect signals
        tab.titleChanged.connect(lambda title: self._update_tab_title(tab, title))
        
        return tab
        
    def close_tab(self, index):
        """Close a browser tab"""
        # Get the tab widget
        tab = self.tabs.widget(index)
        
        # Remove from tab widget
        self.tabs.removeTab(index)
        
        # Delete the tab
        if tab:
            tab.deleteLater()
            
        # If no tabs left, close the window
        if self.tabs.count() == 0:
            self.add_tab()
            
    def _update_tab_title(self, tab, title):
        """Update the title of a tab"""
        index = self.tabs.indexOf(tab)
        if index >= 0:
            # Use a shortened title or fallback
            short_title = title[:20] + "..." if len(title) > 20 else title
            self.tabs.setTabText(index, short_title or "New Tab")
            
    def current_tab(self):
        """Get the current browser tab"""
        return self.tabs.currentWidget()
        
    def load(self, url):
        """Load a URL in the current tab"""
        tab = self.current_tab()
        if tab:
            tab.load(url)
            
    def load_html(self, html, base_url=""):
        """Load HTML in the current tab"""
        tab = self.current_tab()
        if tab:
            tab.load_html(html, base_url)
            
    def register_resolver(self, domain, resolver):
        """Register a domain resolver"""
        self.resolvers.register(domain, resolver)
        print(f"[BrowserView] Registered resolver for {domain}")
        
    def resolver(self, tld):
        """
        Decorator for registering domain resolvers
        
        Example:
            @browser.resolver(".evr")
            def resolve_evr(domain):
                return f"https://ipfs.io/ipfs/your-hash"
        """
        def decorator(func):
            self.resolver_registry.register_function(tld, func)
            return func
        return decorator 
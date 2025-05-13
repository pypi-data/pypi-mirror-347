#!/usr/bin/env python3
"""
EVR browser example using mantipy-gui - Electron-style UI
"""

import sys
import os

# Fix QtWebEngine initialization
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QLabel, QSizePolicy, QSpacerItem
if not QApplication.instance():
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    # Force import of QtWebEngineWidgets
    from PyQt5 import QtWebEngineWidgets

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mantipy_gui import Window, BrowserView, Console, SidePanel
from mantipy_gui.resolvers.resolver import EvrmoreResolver

# Import evrmore_rpc for EVR resolution
from evrmore_rpc import EvrmoreClient


# Define app theme colors
THEME = {
    "primary": "#5865F2",     # Discord-like blue
    "secondary": "#4752C4",   # Slightly darker blue
    "accent": "#EB459E",      # Pink accent
    "background": "#36393F",  # Dark background
    "surface": "#2F3136",     # Slightly lighter panels
    "text": "#FFFFFF",        # White text
    "text_secondary": "#B9BBBE", # Secondary text
    "divider": "#42464D",     # Divider color
    "hover": "#42464D",       # Hover state
    "active": "#393C43",      # Active state
}


def resolve_evr_domain(domain):
    """
    Resolve an EVR domain to a URL using the Evrmore RPC client
    """
    print(f"[EVR Resolver] Called with: {domain}")
    
    # Clean the domain name if it starts with http:// or https://
    if domain.startswith('http://'):
        domain = domain.replace('http://', '')
    elif domain.startswith('https://'):
        domain = domain.replace('https://', '')
    
    domain = domain.rstrip('/')
    
    # Extract the asset name from the domain
    asset_name = domain.upper().replace(".EVR", "")
    print(f"[EVR Resolver] Asset name: {asset_name}")
    
    # FOR TESTING - Use predefined test assets
    test_assets = {
        "CHESS": {
            "site_pubkey": "02b679f444cf89171eab391f5deb59910c5aa087327e0ff69421dbc44f5ec336ec",
            "site_title": "Chess",
            "site_description": "Peer to Peer chess with client side cryptographic anti-cheat!",
            "site_version": "1.0",
            "admin_asset": "CHESS",
            "content_type": "text/html",
            "content_ipns": "k51qzi5uqu5dit4twu44an063vqc3slwewu9f7qtksj6y4s0y37230njljean4"
        },
        "MANTICORE": {
            "site_title": "Manticore Technologies",
            "site_description": "Open source blockchain technologies",
            "content_ipfs": "QmVbpCdhSMoMjmKfNL3VjkkbrJgEAoE4TQfWqWdEqr7Nuu"
        },
        "TEST": {
            "content_ipfs": "QmYKnSuZPz3K3qj9Nh9yYwns5qWKWzGXsVZjLYqPNrZ5Pe"
        },
        "PYTHON": {
            "content_ipfs": "QmYvZpYtELyTBK4o1nKbvwsA8pJxYES3WgFpHEJEF5CP4J"
        }
    }
    
    try:
        # First check for test assets
        asset_data = None
        if asset_name in test_assets:
            asset_data = test_assets[asset_name]
            print(f"[EVR Resolver] Using test asset data for {asset_name}")
        else:
            # Otherwise, fetch from chain
            client = EvrmoreClient()
            print(f"[EVR Resolver] Fetching data for: {asset_name}")
            asset_data = client.getassetdata(asset_name)
        
        # Check if we got any data
        if not asset_data:
            error_msg = f"No asset data found for {asset_name}"
            print(f"[EVR Resolver] Error: {error_msg}")
            return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p></body></html>"
        
        print(f"[EVR Resolver] Asset data: {asset_data}")
        
        # Check if the data contains IPNS
        if "content_ipns" in asset_data:
            ipns_key = asset_data["content_ipns"]
            gateway_url = f"https://ipfs.io/ipns/{ipns_key}"
            print(f"[EVR Resolver] Found IPNS key: {ipns_key}")
            print(f"[EVR Resolver] Returning IPNS URL: {gateway_url}")
            return gateway_url
            
        # Check if the data contains IPFS
        elif "content_ipfs" in asset_data:
            ipfs_hash = asset_data["content_ipfs"]
            gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
            print(f"[EVR Resolver] Found IPFS hash: {ipfs_hash}")
            print(f"[EVR Resolver] Returning IPFS URL: {gateway_url}")
            return gateway_url
            
        # Check for legacy ipfs_hash field
        elif "ipfs_hash" in asset_data:
            ipfs_hash = asset_data["ipfs_hash"]
            gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
            print(f"[EVR Resolver] Found legacy IPFS hash: {ipfs_hash}")
            print(f"[EVR Resolver] Returning IPFS URL: {gateway_url}")
            return gateway_url
            
        # No IPFS/IPNS content found
        else:
            error_msg = f"No IPFS or IPNS content found for asset {asset_name}"
            print(f"[EVR Resolver] Error: {error_msg}")
            return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p><p>Asset data: {asset_data}</p></body></html>"
            
    except Exception as e:
        print(f"[EVR Resolver] Error: {e}")
        return f"data:text/html,<html><body><h1>Error resolving {domain}</h1><p>{str(e)}</p></body></html>"


def create_custom_title_bar(app):
    """Create a custom title bar for Electron-like appearance"""
    from PyQt5.QtWidgets import QHBoxLayout, QWidget, QPushButton
    
    title_bar = QWidget()
    title_bar.setFixedHeight(38)
    title_bar.setStyleSheet(f"""
        QWidget {{
            background-color: {THEME['surface']};
            border-bottom: 1px solid {THEME['divider']};
        }}
        QPushButton {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            color: {THEME['text_secondary']};
            padding: 8px;
            font-size: 16px;
        }}
        QPushButton:hover {{
            background-color: {THEME['hover']};
            color: {THEME['text']};
        }}
    """)
    
    layout = QHBoxLayout(title_bar)
    layout.setContentsMargins(8, 0, 8, 0)
    
    # App icon and title
    icon_label = QLabel("🌐")
    icon_label.setStyleSheet(f"font-size: 20px; color: {THEME['primary']};")
    
    title_label = QLabel("EVR Browser")
    title_label.setStyleSheet(f"color: {THEME['text']}; font-weight: bold; font-size: 14px;")
    
    # Add stretches and window controls
    layout.addWidget(icon_label)
    layout.addWidget(title_label)
    layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    
    # Window controls
    min_btn = QPushButton("🗕")
    min_btn.setToolTip("Minimize")
    min_btn.clicked.connect(lambda: app.window.showMinimized())
    
    max_btn = QPushButton("🗖")
    max_btn.setToolTip("Maximize")
    max_btn.clicked.connect(lambda: app.window.showMaximized() if not app.window.isMaximized() else app.window.showNormal())
    
    close_btn = QPushButton("✕")
    close_btn.setStyleSheet("""
        QPushButton:hover {
            background-color: #E81123;
            color: white;
        }
    """)
    close_btn.setToolTip("Close")
    close_btn.clicked.connect(lambda: app.window.close())
    
    layout.addWidget(min_btn)
    layout.addWidget(max_btn)
    layout.addWidget(close_btn)
    
    return title_bar


def main():
    """Run the EVR browser example"""
    # Create a window with electron-like styling
    app = Window(title="🌐 EVR Browser", width=1200, height=800)
    
    # Style the app with electron-like appearance
    app.window.setStyleSheet(f"""
        QMainWindow {{
            background-color: {THEME['background']};
            border: 1px solid {THEME['divider']};
            border-radius: 8px;
        }}
        QStatusBar {{
            background-color: {THEME['surface']};
            color: {THEME['text_secondary']};
            border-top: 1px solid {THEME['divider']};
            padding: 4px;
        }}
        QTabWidget::pane {{
            border: none;
        }}
        QTabBar::tab {{
            background: {THEME['surface']};
            color: {THEME['text_secondary']};
            padding: 8px 16px;
            border-radius: 4px 4px 0 0;
            margin: 2px 2px 0 2px;
        }}
        QTabBar::tab:selected {{
            background: {THEME['primary']};
            color: {THEME['text']};
        }}
        QTabBar::tab:hover:!selected {{
            background: {THEME['hover']};
            color: {THEME['text']};
        }}
        QTabBar::close-button {{
            margin: 2px;
        }}
        QTabBar::close-button:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
        }}
    """)
    
    # Make window frameless for electron-like appearance
    app.window.setWindowFlags(app.window.windowFlags() | Qt.FramelessWindowHint)
    
    # Create a custom title bar and add to window
    title_bar = create_custom_title_bar(app)
    # Add title bar to the central layout at the top position (index 0)
    app.central_layout.insertWidget(0, title_bar)
    
    # Create a browser view with custom styling
    browser = BrowserView(home_url="about:blank")
    
    # Additional browser styling
    browser.widget.setStyleSheet(f"""
        QWidget {{
            background-color: {THEME['background']};
        }}
    """)
    
    browser.tabs.setStyleSheet(f"""
        QTabWidget::pane {{
            border: none;
            background-color: {THEME['background']};
        }}
        QTabBar::tab {{
            background-color: {THEME['surface']};
            color: {THEME['text_secondary']};
            padding: 8px 16px;
            border-radius: 4px 4px 0 0;
            margin: 2px 2px 0 2px;
            min-height: 30px;
            font-size: 13px;
        }}
        QTabBar::tab:selected {{
            background-color: {THEME['primary']};
            color: {THEME['text']};
        }}
        QTabBar::tab:hover:!selected {{
            background-color: {THEME['hover']};
            color: {THEME['text']};
        }}
        QTabBar::close-button {{
            image: url(close.png);
            subcontrol-position: right;
            margin: 4px;
        }}
        QTabBar::close-button:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
        }}
    """)
    
    # Style each browser tab with Electron-like UI
    for i in range(browser.tabs.count()):
        tab = browser.tabs.widget(i)
        if tab:
            tab.toolbar.setStyleSheet(f"""
                QToolBar {{
                    background-color: {THEME['surface']};
                    border-bottom: 1px solid {THEME['divider']};
                    spacing: 4px;
                    padding: 8px;
                }}
                QToolBar QPushButton {{
                    min-width: 32px;
                    min-height: 32px;
                    border-radius: 4px;
                    padding: 6px;
                    margin: 0 2px;
                    color: {THEME['text']};
                    background-color: transparent;
                }}
                QToolBar QPushButton:hover {{
                    background-color: {THEME['hover']};
                }}
                QToolBar QLineEdit {{
                    min-height: 32px;
                    padding: 4px 12px;
                    border-radius: 16px;
                    border: 1px solid {THEME['divider']};
                    background-color: {THEME['background']};
                    color: {THEME['text']};
                    selection-background-color: {THEME['primary']};
                }}
                QToolBar QLineEdit:focus {{
                    border: 1px solid {THEME['primary']};
                }}
            """)
            
            # Also style the webview
            tab.webview.setStyleSheet(f"""
                QWebEngineView {{
                    background-color: white;
                    border: none;
                }}
            """)
    
    # Register domain resolvers
    @browser.resolver(".evr")
    def resolve_evr(domain):
        print(f"[.evr resolver] Called with: {domain}")
        result = resolve_evr_domain(domain)
        print(f"[.evr resolver] Result: {result}")
        console.log(f"Resolved {domain} → {result}")
        
        # Set the tab URL display to show the original domain
        tab = browser.current_tab()
        if tab and hasattr(tab, 'url_bar'):
            # Store the original domain to display in URL bar
            tab.original_domain = domain
            
        return result
    
    # Also register http://domain.evr format
    @browser.resolver("http://")
    def resolve_http(url):
        # Check if this is an EVR domain
        if not url.lower().endswith('.evr') and not url.lower().endswith('.evr/'):
            return url
            
        print(f"[HTTP Resolver] Handling EVR domain: {url}")
        
        # Extract domain part from URL
        domain = url.replace("http://", "").rstrip("/")
            
        # Store the original URL to display in URL bar
        tab = browser.current_tab()
        if tab and hasattr(tab, 'url_bar'):
            tab.original_domain = url
            
        # Just defer to the main resolver function for consistency
        result = resolve_evr_domain(domain)
        print(f"[HTTP Resolver] Result from EVR resolver: {result}")
        console.log(f"Resolved {url} → {result}")
        return result
    
    # Add resolver for https:// too
    @browser.resolver("https://")
    def resolve_https(url):
        # Check if this is an EVR domain
        if not url.lower().endswith('.evr') and not url.lower().endswith('.evr/'):
            return url
            
        print(f"[HTTPS Resolver] Handling EVR domain: {url}")
        
        # Extract domain part from URL
        domain = url.replace("https://", "").rstrip("/")
            
        # Store the original URL to display in URL bar
        tab = browser.current_tab()
        if tab and hasattr(tab, 'url_bar'):
            tab.original_domain = url
            
        # Defer to the main resolver function
        result = resolve_evr_domain(domain)
        print(f"[HTTPS Resolver] Result from EVR resolver: {result}")
        console.log(f"Resolved {url} → {result}")
        return result
    
    # Create a console for logging with electron-like styling
    console = Console(height=150)
    console.widget.setStyleSheet(f"""
        QFrame {{
            background-color: {THEME['surface']};
            border: none;
            border-top: 1px solid {THEME['divider']};
        }}
    """)
    console.text_edit.setStyleSheet(f"""
        QTextEdit {{
            background-color: {THEME['surface']};
            color: {THEME['text']};
            border: none;
            padding: 8px;
            font-family: "Consolas", "Monaco", monospace;
            font-size: 12px;
        }}
    """)
    
    # Create a side panel for EVR domains with electron-like styling
    sidebar = SidePanel(title="EVR Domains", width=250)
    sidebar.widget.setStyleSheet(f"""
        QWidget {{
            background-color: {THEME['surface']};
            color: {THEME['text']};
        }}
        QLabel {{
            color: {THEME['text']};
            padding: 4px;
        }}
        QPushButton {{
            background-color: {THEME['background']};
            color: {THEME['text']};
            border: none;
            border-radius: 4px;
            padding: 10px;
            margin: 4px 8px;
            text-align: left;
        }}
        QPushButton:hover {{
            background-color: {THEME['hover']};
        }}
        QPushButton:pressed {{
            background-color: {THEME['active']};
        }}
        QLineEdit {{
            background-color: {THEME['background']};
            color: {THEME['text']};
            border: 1px solid {THEME['divider']};
            border-radius: 4px;
            padding: 8px;
            margin: 4px;
        }}
        QLineEdit:focus {{
            border: 1px solid {THEME['primary']};
        }}
    """)
    
    # Add some example EVR domains
    from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
    
    # Add header with custom styling
    header = QLabel("Browse EVR Domains")
    header.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {THEME['text']}; padding: 16px 12px 8px 12px;")
    sidebar.add_widget(header)
    
    # Add domain input
    input_container = QWidget()
    input_layout = QHBoxLayout()
    input_layout.setContentsMargins(8, 4, 8, 4)
    input_container.setLayout(input_layout)
    
    domain_input = QLineEdit()
    domain_input.setPlaceholderText("Enter domain (e.g., asset)")
    
    go_btn = QPushButton("Go")
    go_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {THEME['primary']};
            color: {THEME['text']};
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            margin: 4px 0px;
            text-align: center;
            min-width: 40px;
        }}
        QPushButton:hover {{
            background-color: {THEME['secondary']};
        }}
    """)
    go_btn.clicked.connect(lambda: (
        # Prepare the domain
        domain_input.text().strip() if domain_input.text().strip().lower().endswith('.evr') 
        else f"{domain_input.text().strip()}.evr",
        # Set the original domain and load
        setattr(browser.current_tab(), 'original_domain', 
                domain_input.text().strip() if domain_input.text().strip().lower().endswith('.evr') 
                else f"{domain_input.text().strip()}.evr"),
        browser.load(
            domain_input.text().strip() if domain_input.text().strip().lower().endswith('.evr') 
            else f"{domain_input.text().strip()}.evr"
        ),
        console.log(f"Resolving {domain_input.text().strip()}")
    ))
    
    input_layout.addWidget(domain_input)
    input_layout.addWidget(go_btn)
    
    sidebar.add_widget(input_container)
    
    # Add divider
    divider = QFrame()
    divider.setFrameShape(QFrame.HLine)
    divider.setFrameShadow(QFrame.Sunken)
    divider.setStyleSheet(f"background-color: {THEME['divider']}; border: none; max-height: 1px; margin: 8px 12px;")
    sidebar.add_widget(divider)
    
    # Add example heading
    example_header = QLabel("Example .evr domains:")
    example_header.setStyleSheet(f"font-weight: bold; color: {THEME['text']}; padding: 8px 12px;")
    sidebar.add_widget(example_header)
    
    # Add some example EVR assets that might exist with modern styling
    domains = [
        "MANTICORE.evr",
        "PYTHON.evr", 
        "CHESS.evr",
        "TEST.evr",
    ]
    
    for domain in domains:
        btn = QPushButton(domain)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['background']};
                color: {THEME['text']};
                border: none;
                border-radius: 4px;
                padding: 12px;
                margin: 4px 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {THEME['hover']};
            }}
            QPushButton:pressed {{
                background-color: {THEME['active']};
            }}
        """)
        # Use direct lambda for each button to avoid reference issues
        btn.clicked.connect(lambda checked=False, d=domain: (
            console.log(f"Resolving domain: {d}"),
            # Set the original domain
            setattr(browser.current_tab(), 'original_domain', d),
            browser.load(d)
        ))
        sidebar.add_widget(btn)
    
    # Add explanation with modern styling
    note = QLabel(
        "This browser resolves .evr domains by looking up the asset on "
        "the Evrmore blockchain and loading content from the IPFS hash "
        "found in the asset data."
    )
    note.setWordWrap(True)
    note.setStyleSheet(f"""
        color: {THEME['text_secondary']}; 
        padding: 12px; 
        margin: 8px 12px; 
        font-size: 12px;
        background-color: {THEME['background']};
        border-radius: 4px;
    """)
    sidebar.add_widget(note)
    
    # Log event handler
    def log_url_changed(url):
        tab = browser.current_tab()
        display_url = url
        
        # If we have an original domain, use that for display
        if hasattr(tab, 'original_domain') and tab.original_domain and '.evr' in tab.original_domain.lower():
            display_url = tab.original_domain
            console.log(f"Loaded: {tab.original_domain} (resolved to {url})")
        else:
            console.log(f"Loaded: {url}")
            
        app.set_status(f"Current URL: {display_url}")
        
    # Connect signals
    browser.current_tab().urlChanged.connect(log_url_changed)
    
    # Add views to the window
    app.add_view(browser, "central")
    app.add_view(console, "bottom")
    app.add_view(sidebar, "left")
    
    # Set initial status
    app.set_status("Ready")
    console.log("EVR Browser initialized")
    console.log("Using Evrmore blockchain for .evr domain resolution")
    
    # Load a welcome page with electron-style design
    welcome_html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                color: #e0e0e0; 
                background-color: {THEME['background']}; 
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 40px 20px; 
            }}
            h1 {{ 
                color: {THEME['primary']}; 
                font-size: 36px; 
                font-weight: 600; 
                margin-bottom: 32px;
            }}
            h2 {{ 
                color: {THEME['text']}; 
                font-size: 24px; 
                font-weight: 500; 
                margin-top: 0; 
            }}
            .card {{ 
                background: {THEME['surface']}; 
                border-radius: 8px; 
                padding: 24px; 
                margin: 24px 0; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
                border: 1px solid {THEME['divider']};
            }}
            .highlight {{ 
                background: {THEME['primary']}; 
                color: white; 
                padding: 2px 8px; 
                border-radius: 4px; 
                font-family: monospace;
            }}
            code {{ 
                background: rgba(0,0,0,0.2); 
                padding: 4px 8px; 
                border-radius: 4px; 
                font-family: monospace;
                color: {THEME['text']};
            }}
            p {{ 
                line-height: 1.6; 
                color: {THEME['text_secondary']};
                margin: 12px 0;
            }}
            .step {{
                display: flex;
                align-items: center;
                margin: 16px 0;
            }}
            .step-number {{
                background: {THEME['primary']};
                color: white;
                width: 32px;
                height: 32px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 16px;
                font-weight: bold;
            }}
            .step-text {{
                flex: 1;
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                color: {THEME['text_secondary']};
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the EVR Browser</h1>
            
            <div class="card">
                <h2>Blockchain Domain Resolution</h2>
                <p>This browser can resolve <span class="highlight">.evr</span> domains to web content stored on IPFS, using the Evrmore blockchain.</p>
                <p>Try one of the example domains from the sidebar or enter your own asset name in the address bar.</p>
            </div>
            
            <div class="card">
                <h2>How It Works</h2>
                
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-text">Enter a <span class="highlight">.evr</span> domain in the address bar</div>
                </div>
                
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-text">The resolver looks up the asset on the Evrmore blockchain</div>
                </div>
                
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-text">If an IPFS hash is found, it loads the content from IPFS</div>
                </div>
                
                <p>Example: <code>CHESS.evr</code> will look up the asset <code>CHESS</code> on the blockchain</p>
            </div>
            
            <div class="footer">
                Manticore Technologies © 2023 | EVR Browser
            </div>
        </div>
    </body>
    </html>
    """
    browser.load_html(welcome_html)
    
    # Add a debug log for the resolver registry
    print(f"[Setup] Browser resolvers initialized")
    if browser.resolver_registry:
        registered = list(browser.resolver_registry.resolvers.keys())
        print(f"[Setup] Registered resolvers: {registered}")
    else:
        print("[Setup] Warning: No resolver registry available")
    
    # Make window draggable from the title bar
    def make_window_draggable():
        from PyQt5.QtCore import QPoint
        
        # Add mouse tracking to title bar
        title_bar.mousePressEvent = lambda event: setattr(title_bar, "_drag_pos", event.globalPos() - app.window.frameGeometry().topLeft()) if event.button() == Qt.LeftButton else None
        title_bar.mouseMoveEvent = lambda event: app.window.move(event.globalPos() - getattr(title_bar, "_drag_pos", QPoint(0, 0))) if hasattr(title_bar, "_drag_pos") else None
        title_bar.mouseReleaseEvent = lambda event: delattr(title_bar, "_drag_pos") if hasattr(title_bar, "_drag_pos") else None
    
    make_window_draggable()
    
    # Override the BrowserTab's update_url method to preserve EVR domains in the URL bar
    original_update_url = browser.current_tab().update_url
    
    def custom_update_url():
        """Custom URL update method that preserves EVR domains"""
        tab = browser.current_tab()
        
        # Check if we have an original domain to display
        if hasattr(tab, 'original_domain') and tab.original_domain:
            # If this is an EVR domain, show the original domain in the URL bar
            if '.evr' in tab.original_domain.lower():
                print(f"[BrowserTab] Preserving EVR domain in URL bar: {tab.original_domain}")
                tab.url_bar.setText(tab.original_domain)
                return
        
        # Otherwise, use the default behavior
        original_update_url()
    
    # Replace the update_url method with our custom version
    browser.current_tab().update_url = custom_update_url
    
    # Run the application
    app.window.show()
    # Return success code 
    return 0


if __name__ == "__main__":
    # Create QApplication instance if running as main script
    if not QApplication.instance():
        app = QApplication(sys.argv)
        sys.exit(main())
    else:
        main() 
"""
Main window class for mantipy-gui
"""

import sys
from typing import Optional, List, Dict, Any, Union
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QSplitter, QStatusBar
)

# Ensure QtWebEngine is properly initialized
if not QApplication.instance():
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    # Import QtWebEngineWidgets to initialize it
    from PyQt5 import QtWebEngineWidgets

from .resolvers import ResolverRegistry
from .themes.material import get_theme, COLORS, TYPOGRAPHY, ELEVATION


class Window:
    """
    Main window class for mantipy-gui applications
    
    This class wraps a QMainWindow and provides a simplified API
    for creating GUI applications with mantipy-gui.
    """
    
    def __init__(self, title="Mantipy GUI Window", width=800, height=600, app=None):
        """
        Initialize the window with the given parameters
        
        Args:
            title: Window title
            width: Window width
            height: Window height
            app: QApplication to use (creates one if None)
        """
        # Use existing QApplication if available, otherwise create a new one
        from . import resolver_registry
        
        self.app = app or QApplication.instance() or QApplication(sys.argv)
        self.owns_app = app is None and not QApplication.instance()
        
        # Initialize resolvers registry
        self.resolver_registry = resolver_registry
        
        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(width, height)
        
        # Create central widget
        self.central_widget = QWidget()
        self.window.setCentralWidget(self.central_widget)
        
        # Create central layout
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        
        # Create status bar
        self.status_bar = self.window.statusBar()
        
        # Setup dock areas
        self.dock_areas = {
            "left": Qt.LeftDockWidgetArea,
            "right": Qt.RightDockWidgetArea,
            "top": Qt.TopDockWidgetArea,
            "bottom": Qt.BottomDockWidgetArea
        }
        
        # List of views
        self.views = []
        
    def _apply_theme(self, theme: str = "material", custom_style: Optional[str] = None):
        """Apply a theme to the window
        
        Args:
            theme: Theme name ('material', 'material-dark', 'light', 'dark')
            custom_style: Additional custom styles to apply
        """
        if theme in ('material', 'material-dark'):
            # Use the new Material UI theme system
            style = get_theme('dark' if theme == 'material-dark' else 'light')
        elif theme == "dark":
            style = """
                QMainWindow { background-color: #121212; color: #eee; }
                QWidget { background-color: #121212; color: #eee; }
                QTabBar::tab { background: #2e2e2e; color: #eee; padding: 6px; border-radius: 4px; margin: 2px; }
                QTabBar::tab:selected { background: #5c2b8a; color: white; }
                QLineEdit { background: #1e1e1e; color: #0ff; border: 1px solid #333; padding: 4px; }
                QPushButton { background: #444; color: #eee; border-radius: 4px; padding: 4px 8px; }
                QPushButton:hover { background: #5c2b8a; color: white; }
                QDockWidget { background: #121212; color: #eee; }
                QDockWidget::title { background: #2e2e2e; padding: 4px; }
                QStatusBar { background: #2e2e2e; color: #eee; }
            """
        elif theme == "light":
            style = """
                QMainWindow { background-color: #f5f5f5; color: #333; }
                QWidget { background-color: #f5f5f5; color: #333; }
                QTabBar::tab { background: #e0e0e0; color: #333; padding: 6px; border-radius: 4px; margin: 2px; }
                QTabBar::tab:selected { background: #8c52c6; color: white; }
                QLineEdit { background: white; color: #333; border: 1px solid #ccc; padding: 4px; }
                QPushButton { background: #e0e0e0; color: #333; border-radius: 4px; padding: 4px 8px; }
                QPushButton:hover { background: #8c52c6; color: white; }
                QDockWidget { background: #f5f5f5; color: #333; }
                QDockWidget::title { background: #e0e0e0; padding: 4px; }
                QStatusBar { background: #e0e0e0; color: #333; }
            """
        else:
            style = ""
            
        # Apply custom style if provided
        if custom_style:
            style += custom_style
            
        self.window.setStyleSheet(style)
        
    def add_view(self, view, layout_position="central"):
        """
        Add a view to the window
        
        Args:
            view: The view to add (must have a widget property)
            layout_position: Where to place the view ('central', 'left', 'right', 'top', 'bottom')
        """
        self.views.append(view)
        
        # Setup internal references between the view and window
        view.window = self
        
        if hasattr(view, 'resolver_registry') and self.resolver_registry:
            view.resolver_registry = self.resolver_registry
            
        if layout_position == "central":
            self.central_layout.addWidget(view.widget)
        else:
            # Create a dock widget
            dock = QDockWidget()
            dock.setWidget(view.widget)
            
            # Set dock properties
            area_map = {
                "left": Qt.LeftDockWidgetArea,
                "right": Qt.RightDockWidgetArea,
                "top": Qt.TopDockWidgetArea,
                "bottom": Qt.BottomDockWidgetArea,
            }
            
            self.window.addDockWidget(area_map.get(layout_position, Qt.RightDockWidgetArea), dock)
        
    def set_status(self, message: str):
        """Set status bar message"""
        self.status_bar.showMessage(message)
        
    def run(self):
        """Run the application"""
        self.window.show()
        # Only run the event loop if we created it
        if self.owns_app:
            return self.app.exec_()
        else:
            # Just return success
            return 0 
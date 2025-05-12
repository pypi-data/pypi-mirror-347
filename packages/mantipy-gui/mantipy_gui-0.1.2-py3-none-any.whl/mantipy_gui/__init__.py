"""
mantipy-gui: Python GUI framework by Manticore Technologies

A simple framework for building GUI applications with PyQt5.
"""

# Initialize QApplication early
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# Set QtWebEngine attributes before importing
if not QApplication.instance():
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Import main components
from .window import Window
from .browser import BrowserView, BrowserTab
from .custom_widgets import Console, SidePanel, FileExplorer, TabView

# Import resolvers
from .resolvers import ResolverRegistry
from .resolvers.standard import HTTPResolver, EVRResolver, IPFSResolver

# Initialize resolver registry for all components
resolver_registry = ResolverRegistry()

# Register standard resolvers
resolver_registry.register("", HTTPResolver())
resolver_registry.register("ipfs://", IPFSResolver())
resolver_registry.register(".evr", EVRResolver())

# Initialize QApplication
app = None
if not QApplication.instance():
    app = QApplication(sys.argv)

__all__ = [
    'Window', 
    'BrowserView', 
    'BrowserTab', 
    'Console', 
    'SidePanel',
    'FileExplorer',
    'TabView',
    'ResolverRegistry',
    'HTTPResolver',
    'EVRResolver',
    'IPFSResolver'
]

# Version
__version__ = '0.1.1' 
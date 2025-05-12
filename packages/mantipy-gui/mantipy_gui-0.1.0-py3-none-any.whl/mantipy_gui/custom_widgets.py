"""
Custom widgets for mantipy-gui
"""

from typing import Optional, List, Dict, Any, Callable

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QSplitter, QTreeView, QLineEdit, QMenu, QAction,
    QFrame
)
from PyQt5.QtCore import Qt, QModelIndex

from .themes.material import COLORS, TYPOGRAPHY, ELEVATION

class SidePanel:
    """
    A side panel view for mantipy-gui
    
    This can be used to create a sidebar with custom content.
    """
    
    def __init__(self, title: str = "Side Panel", width: int = 300):
        """
        Initialize a side panel
        
        Args:
            title: Title of the panel
            width: Width of the panel in pixels
        """
        self.title = title
        self.window = None
        
        # Create the widget and layout
        self.widget = QFrame()
        self.widget.setObjectName("sidePanel")
        self.widget.setStyleSheet(f"""
            QFrame#sidePanel {{
                background: white;
                border: 1px solid {COLORS['grey']['300']};
                border-radius: 4px;
                box-shadow: {ELEVATION['1']};
            }}
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)
        self.widget.setLayout(self.layout)
        
        # Set minimum width
        self.widget.setMinimumWidth(width)
        
    def add_widget(self, widget):
        """Add a widget to the panel"""
        self.layout.addWidget(widget)
        
    def clear(self):
        """Clear all widgets from the panel"""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


class Console:
    """
    A console view for mantipy-gui
    
    This can be used to display logs or interact with a command line.
    """
    
    def __init__(self, height: int = 200, read_only: bool = True):
        """
        Initialize a console widget
        
        Args:
            height: Height of the console in pixels
            read_only: Whether the console is read-only
        """
        self.window = None
        
        # Create the widget and layout
        self.widget = QFrame()
        self.widget.setObjectName("consoleFrame")
        self.widget.setStyleSheet(f"""
            QFrame#consoleFrame {{
                background: {COLORS['grey']['900']};
                border: 1px solid {COLORS['grey']['700']};
                border-radius: 4px;
                box-shadow: {ELEVATION['1']};
            }}
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(0)
        self.widget.setLayout(self.layout)
        
        # Create the text edit with Material Design styling
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("console")
        self.text_edit.setReadOnly(read_only)
        self.text_edit.setStyleSheet(f"""
            QTextEdit#console {{
                background-color: {COLORS['grey']['900']};
                color: {COLORS['grey']['100']};
                font-family: 'Roboto Mono', monospace;
                font-size: {TYPOGRAPHY['font_sizes']['body2']};
                border: none;
                border-radius: 4px;
                padding: 8px;
            }}
            QTextEdit#console:focus {{
                border: 2px solid {COLORS['primary']['500']};
            }}
        """)
        
        # Add to layout
        self.layout.addWidget(self.text_edit)
        
        # Set minimum height
        self.widget.setMinimumHeight(height)
        
    def log(self, text: str):
        """Log text to the console"""
        self.text_edit.append(text)
        
    def clear(self):
        """Clear the console"""
        self.text_edit.clear()


class StatusBar:
    """
    A status bar for mantipy-gui
    
    This provides a simple status bar that can be added to a window.
    """
    
    def __init__(self):
        """Initialize a status bar"""
        self.window = None
        
        # Create the widget and layout
        self.widget = QFrame()
        self.widget.setObjectName("statusBarFrame")
        self.widget.setStyleSheet(f"""
            QFrame#statusBarFrame {{
                background: {COLORS['grey']['100']};
                border-top: 1px solid {COLORS['grey']['300']};
                padding: 4px 8px;
            }}
        """)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8, 4, 8, 4)
        self.layout.setSpacing(8)
        self.widget.setLayout(self.layout)
        
        # Create status label with Material Design styling
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['grey']['700']};
                font-size: {TYPOGRAPHY['font_sizes']['body2']};
            }}
        """)
        
        # Add to layout
        self.layout.addWidget(self.status_label)
        
    def set_text(self, text: str):
        """Set the status text"""
        self.status_label.setText(text)


class FileExplorer:
    """
    A file explorer view for mantipy-gui
    
    This can be used to browse files and directories.
    """
    
    def __init__(self, path: str = ".", on_file_selected: Optional[Callable[[str], None]] = None):
        """
        Initialize a file explorer
        
        Args:
            path: Initial path to display
            on_file_selected: Callback when a file is selected
        """
        from PyQt5.QtWidgets import QFileSystemModel
        from PyQt5.QtCore import QDir
        
        self.window = None
        self.on_file_selected = on_file_selected
        
        # Create the widget and layout
        self.widget = QFrame()
        self.widget.setObjectName("fileExplorerFrame")
        self.widget.setStyleSheet(f"""
            QFrame#fileExplorerFrame {{
                background: white;
                border: 1px solid {COLORS['grey']['300']};
                border-radius: 4px;
                box-shadow: {ELEVATION['1']};
            }}
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(8)
        self.widget.setLayout(self.layout)
        
        # Create path input with Material Design styling
        self.path_input = QLineEdit(path)
        self.path_input.setStyleSheet(f"""
            QLineEdit {{
                background: white;
                border: 1px solid {COLORS['grey']['300']};
                border-radius: 4px;
                padding: 8px;
                min-height: 36px;
                font-size: {TYPOGRAPHY['font_sizes']['body1']};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']['500']};
            }}
        """)
        self.path_input.returnPressed.connect(self.change_path)
        
        # Create the file system model
        self.model = QFileSystemModel()
        self.model.setRootPath(path)
        
        # Create the tree view with Material Design styling
        self.tree = QTreeView()
        self.tree.setStyleSheet(f"""
            QTreeView {{
                background: white;
                border: 1px solid {COLORS['grey']['300']};
                border-radius: 4px;
            }}
            QTreeView::item {{
                padding: 4px;
                min-height: 32px;
            }}
            QTreeView::item:selected {{
                background: {COLORS['primary']['50']};
                color: {COLORS['primary']['700']};
            }}
            QTreeView::item:hover:!selected {{
                background: {COLORS['grey']['100']};
            }}
        """)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(path))
        self.tree.setSortingEnabled(True)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.doubleClicked.connect(self.item_double_clicked)
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.tree.hideColumn(i)
            
        # Add to layout
        self.layout.addWidget(self.path_input)
        self.layout.addWidget(self.tree)
        
    def change_path(self):
        """Change the current path"""
        path = self.path_input.text()
        self.tree.setRootIndex(self.model.index(path))
        
    def item_double_clicked(self, index: QModelIndex):
        """Handle item double click"""
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.tree.setRootIndex(index)
            self.path_input.setText(path)
        elif self.on_file_selected:
            self.on_file_selected(path) 
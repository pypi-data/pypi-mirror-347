"""
Custom widgets for mantipy-gui
"""

from typing import Optional, List, Dict, Any, Callable

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QLabel, QPushButton, QListWidget, QListWidgetItem,
    QSplitter, QTreeView, QLineEdit, QMenu, QAction,
    QFrame, QTabWidget
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


class TabView:
    """
    A tabbed view container for mantipy-gui
    
    This can be used to create a view with multiple tabs.
    """
    
    def __init__(self, tab_position="top", style="default", closable=True):
        """
        Initialize a tabbed view
        
        Args:
            tab_position: Position of the tabs ('top', 'bottom', 'left', 'right')
            style: Style of the tabs ('default', 'modern', 'minimal')
            closable: Whether tabs can be closed
        """
        from PyQt5.QtWidgets import QTabWidget
        
        self.window = None
        
        # Create the widget
        self.widget = QTabWidget()
        self.widget.setObjectName("tabView")
        
        # Set tab position
        positions = {
            "top": QTabWidget.North,
            "bottom": QTabWidget.South,
            "left": QTabWidget.West,
            "right": QTabWidget.East
        }
        self.widget.setTabPosition(positions.get(tab_position, QTabWidget.North))
        
        # Set whether tabs are closable
        self.widget.setTabsClosable(closable)
        if closable:
            self.widget.tabCloseRequested.connect(self.remove_tab)
        
        # Apply styling based on style parameter
        if style == "modern":
            self.widget.setStyleSheet(f"""
                QTabWidget::pane {{
                    background: {COLORS['grey']['900']};
                    border: 1px solid {COLORS['grey']['700']};
                    border-radius: 4px;
                }}
                QTabBar::tab {{
                    background: {COLORS['grey']['800']};
                    color: {COLORS['grey']['400']};
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    margin: 2px 2px 0 2px;
                }}
                QTabBar::tab:selected {{
                    background: {COLORS['primary']['700']};
                    color: white;
                }}
                QTabBar::tab:hover:!selected {{
                    background: {COLORS['grey']['700']};
                }}
                QTabBar::close-button {{
                    image: url(close.png);
                    subcontrol-position: right;
                }}
                QTabBar::close-button:hover {{
                    background: {COLORS['grey']['600']};
                    border-radius: 2px;
                }}
            """)
        elif style == "minimal":
            self.widget.setStyleSheet(f"""
                QTabWidget::pane {{
                    background: white;
                    border: none;
                    border-top: 1px solid {COLORS['grey']['300']};
                }}
                QTabBar::tab {{
                    background: transparent;
                    color: {COLORS['grey']['700']};
                    padding: 8px 16px;
                    border: none;
                    border-bottom: 2px solid transparent;
                    margin: 0;
                }}
                QTabBar::tab:selected {{
                    background: transparent;
                    color: {COLORS['primary']['500']};
                    border-bottom: 2px solid {COLORS['primary']['500']};
                }}
                QTabBar::tab:hover:!selected {{
                    background: {COLORS['grey']['100']};
                }}
                QTabBar::close-button {{
                    image: url(close.png);
                    subcontrol-position: right;
                }}
                QTabBar::close-button:hover {{
                    background: {COLORS['grey']['200']};
                    border-radius: 2px;
                }}
            """)
        else:
            # Default styling
            self.widget.setStyleSheet(f"""
                QTabWidget::pane {{
                    background: white;
                    border: 1px solid {COLORS['grey']['300']};
                    border-radius: 4px;
                    box-shadow: {ELEVATION['1']};
                }}
                QTabBar::tab {{
                    background: {COLORS['grey']['100']};
                    color: {COLORS['grey']['700']};
                    padding: 8px 16px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    margin: 2px 2px 0 2px;
                }}
                QTabBar::tab:selected {{
                    background: {COLORS['primary']['500']};
                    color: white;
                }}
                QTabBar::tab:hover:!selected {{
                    background: {COLORS['grey']['200']};
                }}
                QTabBar::close-button {{
                    image: url(close.png);
                    subcontrol-position: right;
                    margin: 4px;
                }}
                QTabBar::close-button:hover {{
                    background: {COLORS['grey']['300']};
                    border-radius: 2px;
                }}
            """)
        
    def add_tab(self, title, widget=None, view=None):
        """
        Add a tab with the given widget/view and title
        
        Args:
            title: Title of the tab
            widget: Widget to add (or None if view is provided)
            view: View to add (or None if widget is provided)
        
        Returns:
            Index of the added tab
        """
        # Handle both widget and view parameters
        if view is not None:
            return self.widget.addTab(view.widget, title)
        elif widget is not None:
            return self.widget.addTab(widget, title)
        else:
            raise ValueError("Either widget or view must be provided")
        
    def remove_tab(self, index):
        """
        Remove the tab at the given index
        
        Args:
            index: Index of the tab to remove
        """
        self.widget.removeTab(index)
        
    def current_tab(self):
        """
        Get the current tab widget
        
        Returns:
            Current tab widget
        """
        return self.widget.currentWidget()
        
    def set_current_tab(self, index):
        """
        Set the current tab
        
        Args:
            index: Index of the tab to select
        """
        self.widget.setCurrentIndex(index)
        
    def select_tab(self, index):
        """
        Select the tab at the given index (alias for set_current_tab)
        
        Args:
            index: Index of the tab to select
        """
        self.set_current_tab(index)
        
    def tab_count(self):
        """
        Get the number of tabs
        
        Returns:
            Number of tabs
        """
        return self.widget.count()


class SidebarView:
    """
    A sidebar view for mantipy-gui
    
    This is an alias for SidePanel with a more consistent naming.
    """
    
    def __init__(self, title: str = "Sidebar", width: int = 250, theme: str = "light"):
        """
        Initialize a sidebar view
        
        Args:
            title: Title of the sidebar
            width: Width of the sidebar in pixels
            theme: Theme for the sidebar ('light', 'dark')
        """
        # Create a SidePanel with the specified parameters
        self.panel = SidePanel(title=title, width=width)
        
        # Forward the widget property
        self.widget = self.panel.widget
        self.window = None
        
        # Item storage and callbacks
        self.items = {}
        self.current_selection = None
        self.selection_callback = None
        
        # Apply theme styling
        if theme == "dark":
            self.widget.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['grey']['900']};
                    color: {COLORS['grey']['100']};
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['grey']['300']};
                    border: none;
                    border-radius: 4px;
                    padding: 12px;
                    text-align: left;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['grey']['800']};
                }}
                QPushButton[selected="true"] {{
                    background-color: {COLORS['primary']['700']};
                    color: white;
                }}
                QLabel {{
                    color: {COLORS['grey']['400']};
                    padding: 8px;
                    font-size: 12px;
                }}
            """)
        else:
            # Light theme is the default
            self.widget.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['grey']['100']};
                    color: {COLORS['grey']['900']};
                    border: none;
                    border-radius: 4px;
                }}
                QPushButton {{
                    background-color: transparent;
                    color: {COLORS['grey']['700']};
                    border: none;
                    border-radius: 4px;
                    padding: 12px;
                    text-align: left;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {COLORS['grey']['200']};
                }}
                QPushButton[selected="true"] {{
                    background-color: {COLORS['primary']['500']};
                    color: white;
                }}
                QLabel {{
                    color: {COLORS['grey']['600']};
                    padding: 8px;
                    font-size: 12px;
                }}
            """)
        
    def add_widget(self, widget):
        """Add a widget to the sidebar"""
        self.panel.add_widget(widget)
        
    def add_item(self, item_id: str, label: str, icon: str = None):
        """
        Add an item to the sidebar
        
        Args:
            item_id: Unique identifier for the item
            label: Display label for the item
            icon: Optional icon (emoji or unicode character)
        """
        from PyQt5.QtWidgets import QPushButton
        
        # Create a button for the item
        button = QPushButton(f"{icon} {label}" if icon else label)
        button.setProperty("item_id", item_id)
        button.setProperty("selected", "false")
        
        # Store the button
        self.items[item_id] = button
        
        # Connect click handler
        button.clicked.connect(lambda: self._handle_item_click(item_id))
        
        # Add to layout
        self.panel.add_widget(button)
        
    def add_section(self, title: str):
        """
        Add a section header to the sidebar
        
        Args:
            title: Title of the section
        """
        from PyQt5.QtWidgets import QLabel
        
        label = QLabel(title.upper())
        label.setProperty("class", "section-header")
        
        self.panel.add_widget(label)
        
    def on_select(self, callback):
        """
        Set a callback for when an item is selected
        
        Args:
            callback: Function to call when an item is selected
            
        Returns:
            The decorator function
        """
        self.selection_callback = callback
        return callback
        
    def _handle_item_click(self, item_id):
        """Handle click on a sidebar item"""
        # Update selection state
        if self.current_selection in self.items:
            self.items[self.current_selection].setProperty("selected", "false")
            self.items[self.current_selection].style().unpolish(self.items[self.current_selection])
            self.items[self.current_selection].style().polish(self.items[self.current_selection])
            
        self.current_selection = item_id
        self.items[item_id].setProperty("selected", "true")
        self.items[item_id].style().unpolish(self.items[item_id])
        self.items[item_id].style().polish(self.items[item_id])
        
        # Call the selection callback if set
        if self.selection_callback:
            self.selection_callback(item_id)
        
    def select_item(self, item_id):
        """
        Programmatically select an item
        
        Args:
            item_id: ID of the item to select
        """
        if item_id in self.items:
            self._handle_item_click(item_id)
        
    def clear(self):
        """Clear all widgets from the sidebar"""
        self.panel.clear()
        self.items = {}


class SplitView:
    """
    A split view for mantipy-gui
    
    This can be used to create a split view with adjustable divider.
    """
    
    def __init__(self, orientation="horizontal", direction=None, sizes=None):
        """
        Initialize a split view
        
        Args:
            orientation: Orientation of the split ('horizontal' or 'vertical')
            direction: Alternative name for orientation ('horizontal' or 'vertical')
            sizes: List of initial size ratios for widgets in the splitter
        """
        self.window = None
        
        # Create the widget
        self.widget = QSplitter()
        self.widget.setObjectName("splitView")
        
        # Handle direction alias (direction takes precedence if provided)
        orientation = direction if direction is not None else orientation
        
        # Set orientation
        if orientation == "vertical":
            self.widget.setOrientation(Qt.Vertical)
        else:
            self.widget.setOrientation(Qt.Horizontal)
        
        # Apply material design styling
        self.widget.setStyleSheet(f"""
            QSplitter::handle {{
                background: {COLORS['grey']['300']};
                border-radius: 2px;
            }}
            QSplitter::handle:horizontal {{
                width: 4px;
            }}
            QSplitter::handle:vertical {{
                height: 4px;
            }}
            QSplitter::handle:hover {{
                background: {COLORS['primary']['300']};
            }}
        """)
        
        # Store sizes for when widgets are added
        self.initial_sizes = sizes
        
    def add_widget(self, widget):
        """
        Add a widget to the split view
        
        Args:
            widget: Widget to add
        """
        self.widget.addWidget(widget)
        
        # Apply initial sizes if all widgets are added
        if self.initial_sizes is not None and self.widget.count() == len(self.initial_sizes):
            self.set_sizes(self.initial_sizes)
            
    def add_view(self, view):
        """
        Add a view to the split view (alternative to add_widget, handles view.widget)
        
        Args:
            view: View to add
        """
        self.add_widget(view.widget)
    
    def set_sizes(self, sizes: List[int]):
        """
        Set the sizes of the widgets
        
        Args:
            sizes: List of sizes for each widget
        """
        self.widget.setSizes(sizes)
        
    def set_stretch_factors(self, factors: List[int]):
        """
        Set the stretch factors of the widgets
        
        Args:
            factors: List of stretch factors for each widget
        """
        for i, factor in enumerate(factors):
            self.widget.setStretchFactor(i, factor) 
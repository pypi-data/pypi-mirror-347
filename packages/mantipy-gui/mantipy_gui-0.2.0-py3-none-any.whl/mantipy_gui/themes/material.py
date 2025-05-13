"""
Material UI theme support for mantipy-gui

This module provides Material Design styling for mantipy-gui components.
"""

# Material Design color palette
COLORS = {
    'primary': {
        '50': '#E3F2FD',
        '100': '#BBDEFB',
        '200': '#90CAF9',
        '300': '#64B5F6',
        '400': '#42A5F5',
        '500': '#2196F3',  # Primary color
        '600': '#1E88E5',
        '700': '#1976D2',
        '800': '#1565C0',
        '900': '#0D47A1',
    },
    'accent': {
        '50': '#FFF3E0',
        '100': '#FFE0B2',
        '200': '#FFCC80',
        '300': '#FFB74D',
        '400': '#FFA726',
        '500': '#FF9800',  # Accent color
        '600': '#FB8C00',
        '700': '#F57C00',
        '800': '#EF6C00',
        '900': '#E65100',
    },
    'grey': {
        '50': '#FAFAFA',
        '100': '#F5F5F5',
        '200': '#EEEEEE',
        '300': '#E0E0E0',
        '400': '#BDBDBD',
        '500': '#9E9E9E',
        '600': '#757575',
        '700': '#616161',
        '800': '#424242',
        '900': '#212121',
    },
    'error': '#B00020',
    'success': '#4CAF50',
    'warning': '#FFC107',
    'info': '#2196F3',
}

# Material Design typography
TYPOGRAPHY = {
    'font_family': "'Roboto', 'Segoe UI', sans-serif",
    'font_sizes': {
        'h1': '96px',
        'h2': '60px',
        'h3': '48px',
        'h4': '34px',
        'h5': '24px',
        'h6': '20px',
        'subtitle1': '16px',
        'subtitle2': '14px',
        'body1': '16px',
        'body2': '14px',
        'button': '14px',
        'caption': '12px',
        'overline': '10px',
    },
    'font_weights': {
        'light': '300',
        'regular': '400',
        'medium': '500',
        'bold': '700',
    }
}

# Material Design elevation (shadows)
ELEVATION = {
    '0': 'none',
    '1': '0 2px 1px -1px rgba(0,0,0,0.2), 0 1px 1px 0 rgba(0,0,0,0.14), 0 1px 3px 0 rgba(0,0,0,0.12)',
    '2': '0 3px 1px -2px rgba(0,0,0,0.2), 0 2px 2px 0 rgba(0,0,0,0.14), 0 1px 5px 0 rgba(0,0,0,0.12)',
    '3': '0 3px 3px -2px rgba(0,0,0,0.2), 0 3px 4px 0 rgba(0,0,0,0.14), 0 1px 8px 0 rgba(0,0,0,0.12)',
    '4': '0 2px 4px -1px rgba(0,0,0,0.2), 0 4px 5px 0 rgba(0,0,0,0.14), 0 1px 10px 0 rgba(0,0,0,0.12)',
    '6': '0 3px 5px -1px rgba(0,0,0,0.2), 0 6px 10px 0 rgba(0,0,0,0.14), 0 1px 18px 0 rgba(0,0,0,0.12)',
    '8': '0 5px 5px -3px rgba(0,0,0,0.2), 0 8px 10px 1px rgba(0,0,0,0.14), 0 3px 14px 2px rgba(0,0,0,0.12)',
    '12': '0 7px 8px -4px rgba(0,0,0,0.2), 0 12px 17px 2px rgba(0,0,0,0.14), 0 5px 22px 4px rgba(0,0,0,0.12)',
    '16': '0 8px 10px -5px rgba(0,0,0,0.2), 0 16px 24px 2px rgba(0,0,0,0.14), 0 6px 30px 5px rgba(0,0,0,0.12)',
    '24': '0 11px 15px -7px rgba(0,0,0,0.2), 0 24px 38px 3px rgba(0,0,0,0.14), 0 9px 46px 8px rgba(0,0,0,0.12)',
}

def get_light_theme():
    """Get the light Material Design theme stylesheet"""
    return f"""
        /* Material Design Light Theme */
        QMainWindow, QWidget {{ 
            background-color: {COLORS['grey']['50']}; 
            color: {COLORS['grey']['900']};
            font-family: {TYPOGRAPHY['font_family']};
        }}
        
        /* Material Design Buttons */
        QPushButton {{
            background-color: {COLORS['primary']['500']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
            font-size: {TYPOGRAPHY['font_sizes']['button']};
            min-height: 36px;
            box-shadow: {ELEVATION['2']};
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']['600']};
            box-shadow: {ELEVATION['4']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary']['700']};
            box-shadow: {ELEVATION['8']};
        }}
        QPushButton:disabled {{
            background-color: {COLORS['grey']['300']};
            color: {COLORS['grey']['500']};
            box-shadow: none;
        }}
        
        /* Material Design Input Fields */
        QLineEdit {{
            background-color: white;
            border: 1px solid {COLORS['grey']['300']};
            border-radius: 4px;
            padding: 8px;
            min-height: 36px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
            box-shadow: {ELEVATION['1']};
        }}
        QLineEdit:focus {{
            border: 2px solid {COLORS['primary']['500']};
            box-shadow: {ELEVATION['2']};
        }}
        QLineEdit:disabled {{
            background-color: {COLORS['grey']['100']};
            color: {COLORS['grey']['500']};
            border-color: {COLORS['grey']['300']};
        }}
        
        /* Material Design Tabs */
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
        
        /* Material Design Dock Widgets */
        QDockWidget {{
            background: {COLORS['grey']['50']};
            color: {COLORS['grey']['900']};
            border: 1px solid {COLORS['grey']['300']};
            box-shadow: {ELEVATION['1']};
        }}
        QDockWidget::title {{
            background: {COLORS['grey']['100']};
            padding: 8px;
            border-bottom: 1px solid {COLORS['grey']['300']};
            font-size: {TYPOGRAPHY['font_sizes']['subtitle1']};
        }}
        
        /* Material Design Status Bar */
        QStatusBar {{
            background: {COLORS['grey']['100']};
            color: {COLORS['grey']['700']};
            border-top: 1px solid {COLORS['grey']['300']};
            font-size: {TYPOGRAPHY['font_sizes']['body2']};
        }}
        
        /* Material Design Cards */
        QFrame[frameShape="4"] {{  /* StyledPanel */
            background: white;
            border-radius: 8px;
            border: 1px solid {COLORS['grey']['300']};
            box-shadow: {ELEVATION['1']};
        }}
        
        /* Material Design Lists */
        QTreeWidget, QListWidget {{
            background: white;
            border: 1px solid {COLORS['grey']['300']};
            border-radius: 4px;
            box-shadow: {ELEVATION['1']};
        }}
        QTreeWidget::item, QListWidget::item {{
            padding: 8px;
            min-height: 36px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
        }}
        QTreeWidget::item:selected, QListWidget::item:selected {{
            background: {COLORS['primary']['50']};
            color: {COLORS['primary']['700']};
        }}
        QTreeWidget::item:hover:!selected, QListWidget::item:hover:!selected {{
            background: {COLORS['grey']['100']};
        }}
        
        /* Material Design Scrollbars */
        QScrollBar:vertical {{
            border: none;
            background: {COLORS['grey']['100']};
            width: 12px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['grey']['400']};
            border-radius: 6px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {COLORS['grey']['500']};
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background: {COLORS['grey']['100']};
            height: 12px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {COLORS['grey']['400']};
            border-radius: 6px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {COLORS['grey']['500']};
        }}
        
        /* Material Design Tooltips */
        QToolTip {{
            background-color: {COLORS['grey']['800']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: {TYPOGRAPHY['font_sizes']['caption']};
        }}
        
        /* Material Design Menu */
        QMenu {{
            background-color: white;
            border: 1px solid {COLORS['grey']['300']};
            border-radius: 4px;
            padding: 4px 0;
            box-shadow: {ELEVATION['4']};
        }}
        QMenu::item {{
            padding: 8px 24px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
        }}
        QMenu::item:selected {{
            background-color: {COLORS['primary']['50']};
            color: {COLORS['primary']['700']};
        }}
        
        /* Material Design Browser Components */
        QToolBar {{
            background: {COLORS['grey']['50']};
            border-bottom: 1px solid {COLORS['grey']['300']};
            spacing: 4px;
            padding: 4px;
        }}
        
        /* Material Design Console */
        QTextEdit#console {{
            background-color: {COLORS['grey']['900']};
            color: {COLORS['grey']['100']};
            font-family: 'Roboto Mono', monospace;
            font-size: {TYPOGRAPHY['font_sizes']['body2']};
            border: none;
            border-radius: 4px;
            padding: 8px;
        }}
    """

def get_dark_theme():
    """Get the dark Material Design theme stylesheet"""
    return f"""
        /* Material Design Dark Theme */
        QMainWindow, QWidget {{ 
            background-color: {COLORS['grey']['900']}; 
            color: {COLORS['grey']['100']};
            font-family: {TYPOGRAPHY['font_family']};
        }}
        
        /* Material Design Buttons */
        QPushButton {{
            background-color: {COLORS['primary']['500']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: {TYPOGRAPHY['font_weights']['medium']};
            font-size: {TYPOGRAPHY['font_sizes']['button']};
            min-height: 36px;
            box-shadow: {ELEVATION['2']};
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary']['400']};
            box-shadow: {ELEVATION['4']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary']['300']};
            box-shadow: {ELEVATION['8']};
        }}
        QPushButton:disabled {{
            background-color: {COLORS['grey']['700']};
            color: {COLORS['grey']['500']};
            box-shadow: none;
        }}
        
        /* Material Design Input Fields */
        QLineEdit {{
            background-color: {COLORS['grey']['800']};
            color: {COLORS['grey']['100']};
            border: 1px solid {COLORS['grey']['700']};
            border-radius: 4px;
            padding: 8px;
            min-height: 36px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
            box-shadow: {ELEVATION['1']};
        }}
        QLineEdit:focus {{
            border: 2px solid {COLORS['primary']['500']};
            box-shadow: {ELEVATION['2']};
        }}
        QLineEdit:disabled {{
            background-color: {COLORS['grey']['900']};
            color: {COLORS['grey']['600']};
            border-color: {COLORS['grey']['700']};
        }}
        
        /* Material Design Tabs */
        QTabBar::tab {{
            background: {COLORS['grey']['800']};
            color: {COLORS['grey']['300']};
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
            background: {COLORS['grey']['700']};
        }}
        
        /* Material Design Dock Widgets */
        QDockWidget {{
            background: {COLORS['grey']['900']};
            color: {COLORS['grey']['100']};
            border: 1px solid {COLORS['grey']['700']};
            box-shadow: {ELEVATION['1']};
        }}
        QDockWidget::title {{
            background: {COLORS['grey']['800']};
            padding: 8px;
            border-bottom: 1px solid {COLORS['grey']['700']};
            font-size: {TYPOGRAPHY['font_sizes']['subtitle1']};
        }}
        
        /* Material Design Status Bar */
        QStatusBar {{
            background: {COLORS['grey']['800']};
            color: {COLORS['grey']['300']};
            border-top: 1px solid {COLORS['grey']['700']};
            font-size: {TYPOGRAPHY['font_sizes']['body2']};
        }}
        
        /* Material Design Cards */
        QFrame[frameShape="4"] {{  /* StyledPanel */
            background: {COLORS['grey']['800']};
            border-radius: 8px;
            border: 1px solid {COLORS['grey']['700']};
            box-shadow: {ELEVATION['1']};
        }}
        
        /* Material Design Lists */
        QTreeWidget, QListWidget {{
            background: {COLORS['grey']['800']};
            border: 1px solid {COLORS['grey']['700']};
            border-radius: 4px;
            box-shadow: {ELEVATION['1']};
        }}
        QTreeWidget::item, QListWidget::item {{
            padding: 8px;
            min-height: 36px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
        }}
        QTreeWidget::item:selected, QListWidget::item:selected {{
            background: {COLORS['primary']['900']};
            color: {COLORS['primary']['100']};
        }}
        QTreeWidget::item:hover:!selected, QListWidget::item:hover:!selected {{
            background: {COLORS['grey']['700']};
        }}
        
        /* Material Design Scrollbars */
        QScrollBar:vertical {{
            border: none;
            background: {COLORS['grey']['800']};
            width: 12px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {COLORS['grey']['600']};
            border-radius: 6px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {COLORS['grey']['500']};
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background: {COLORS['grey']['800']};
            height: 12px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {COLORS['grey']['600']};
            border-radius: 6px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {COLORS['grey']['500']};
        }}
        
        /* Material Design Tooltips */
        QToolTip {{
            background-color: {COLORS['grey']['700']};
            color: {COLORS['grey']['100']};
            border: none;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: {TYPOGRAPHY['font_sizes']['caption']};
        }}
        
        /* Material Design Menu */
        QMenu {{
            background-color: {COLORS['grey']['800']};
            border: 1px solid {COLORS['grey']['700']};
            border-radius: 4px;
            padding: 4px 0;
            box-shadow: {ELEVATION['4']};
        }}
        QMenu::item {{
            padding: 8px 24px;
            font-size: {TYPOGRAPHY['font_sizes']['body1']};
        }}
        QMenu::item:selected {{
            background-color: {COLORS['primary']['900']};
            color: {COLORS['primary']['100']};
        }}
        
        /* Material Design Browser Components */
        QToolBar {{
            background: {COLORS['grey']['900']};
            border-bottom: 1px solid {COLORS['grey']['700']};
            spacing: 4px;
            padding: 4px;
        }}
        
        /* Material Design Console */
        QTextEdit#console {{
            background-color: {COLORS['grey']['900']};
            color: {COLORS['grey']['100']};
            font-family: 'Roboto Mono', monospace;
            font-size: {TYPOGRAPHY['font_sizes']['body2']};
            border: none;
            border-radius: 4px;
            padding: 8px;
        }}
    """

def get_theme(theme_name: str = 'light') -> str:
    """Get the Material Design theme stylesheet by name"""
    themes = {
        'light': get_light_theme,
        'dark': get_dark_theme,
    }
    return themes.get(theme_name.lower(), get_light_theme)() 
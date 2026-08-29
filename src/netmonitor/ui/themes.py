class ThemePalette:
    DARK = {
        "bg_main": "#1e222b",
        "bg_sidebar": "#161920",
        "bg_card": "#242936",
        "bg_hover": "#2d3446",
        "text_primary": "#e3e8f0",
        "text_secondary": "#94a3b8",
        "border": "#2d3139",
        "primary": "#3b82f6",
        "primary_hover": "#60a5fa",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "card_shadow": "rgba(0, 0, 0, 0.2)",
    }

    LIGHT = {
        "bg_main": "#f8fafc",
        "bg_sidebar": "#f1f5f9",
        "bg_card": "#ffffff",
        "bg_hover": "#e2e8f0",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "border": "#e2e8f0",
        "primary": "#2563eb",
        "primary_hover": "#1d4ed8",
        "success": "#10b981",
        "warning": "#d97706",
        "danger": "#dc2626",
        "card_shadow": "rgba(0, 0, 0, 0.05)",
    }

def get_theme_qss(theme_name: str) -> str:
    palette = ThemePalette.DARK if theme_name == "dark" else ThemePalette.LIGHT
    return f"""
        QMainWindow {{
            background-color: {palette["bg_main"]};
            color: {palette["text_primary"]};
        }}
        QWidget {{
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
            font-size: 13px;
            color: {palette["text_primary"]};
        }}
        QFrame#Sidebar {{
            background-color: {palette["bg_sidebar"]};
            border-right: 1px solid {palette["border"]};
        }}
        QPushButton#SidebarButton {{
            background-color: transparent;
            color: {palette["text_secondary"]};
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            text-align: left;
            font-weight: 500;
        }}
        QPushButton#SidebarButton:hover {{
            background-color: {palette["bg_hover"]};
            color: {palette["text_primary"]};
        }}
        QPushButton#SidebarButton:checked {{
            background-color: {palette["primary"]};
            color: #ffffff;
        }}
        QPushButton {{
            background-color: {palette["bg_card"]};
            color: {palette["text_primary"]};
            border: 1px solid {palette["border"]};
            border-radius: 4px;
            padding: 6px 12px;
        }}
        QPushButton:hover {{
            background-color: {palette["bg_hover"]};
        }}
        QPushButton:pressed {{
            background-color: {palette["border"]};
        }}
        QPushButton#ToggleMonitorButton {{
            background-color: {palette["primary"]};
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton#ToggleMonitorButton:hover {{
            background-color: {palette["primary_hover"]};
        }}
        QFrame#ViewContainer {{
            background-color: {palette["bg_main"]};
            border: none;
        }}
        QFrame#Card {{
            background-color: {palette["bg_card"]};
            border: 1px solid {palette["border"]};
            border-radius: 6px;
        }}
        QLabel#CardTitle {{
            color: {palette["text_secondary"]};
            font-size: 12px;
            font-weight: 600;
        }}
        QLabel#CardValue {{
            color: {palette["text_primary"]};
            font-size: 20px;
            font-weight: bold;
        }}
        QLabel#CardUnit {{
            color: {palette["text_secondary"]};
            font-size: 12px;
        }}
        QListWidget {{
            background-color: {palette["bg_card"]};
            border: 1px solid {palette["border"]};
            border-radius: 4px;
            color: {palette["text_primary"]};
        }}
        QListWidget::item {{
            padding: 8px;
            color: {palette["text_primary"]};
        }}
        QListWidget::item:hover {{
            background-color: {palette["bg_hover"]};
        }}
        QListWidget::item:selected {{
            background-color: {palette["primary"]};
            color: #ffffff;
        }}
        QTableWidget {{
            background-color: {palette["bg_card"]};
            border: 1px solid {palette["border"]};
            gridline-color: {palette["border"]};
            border-radius: 4px;
        }}
        QTableWidget QTableCornerButton::section {{
            background-color: {palette["bg_sidebar"]};
            border: 1px solid {palette["border"]};
        }}
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {palette["border"]};
        }}
        QTableWidget::item:selected {{
            background-color: {palette["primary"]};
            color: #ffffff;
        }}
        QHeaderView {{
            background-color: {palette["bg_sidebar"]};
        }}
        QHeaderView::section {{
            background-color: {palette["bg_sidebar"]};
            color: {palette["text_primary"]};
            padding: 6px;
            font-weight: 600;
            border: 1px solid {palette["border"]};
        }}
        QLineEdit {{
            background-color: {palette["bg_card"]};
            border: 1px solid {palette["border"]};
            border-radius: 4px;
            padding: 6px 12px;
            color: {palette["text_primary"]};
        }}
        QLineEdit:focus {{
            border: 1px solid {palette["primary"]};
        }}
        QComboBox {{
            background-color: {palette["bg_card"]};
            border: 1px solid {palette["border"]};
            border-radius: 4px;
            padding: 5px 10px;
            color: {palette["text_primary"]};
        }}
        QComboBox:focus {{
            border: 1px solid {palette["primary"]};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {palette["bg_sidebar"]};
            width: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {palette["border"]};
            min-height: 20px;
            border-radius: 5px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {palette["text_secondary"]};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        QScrollBar:horizontal {{
            border: none;
            background: {palette["bg_sidebar"]};
            height: 10px;
            margin: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {palette["border"]};
            min-width: 20px;
            border-radius: 5px;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: none;
            background: none;
        }}
        QTabWidget::pane {{
            border: 1px solid {palette["border"]};
            background-color: {palette["bg_card"]};
            border-radius: 4px;
        }}
        QTabBar::tab {{
            background-color: {palette["bg_sidebar"]};
            border: 1px solid {palette["border"]};
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        QTabBar::tab:selected {{
            background-color: {palette["bg_card"]};
            border-bottom-color: transparent;
        }}
        QGroupBox {{
            font-weight: bold;
            border: 1px solid {palette["border"]};
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 12px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 5px;
        }}
        QCheckBox {{
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
        }}
    """

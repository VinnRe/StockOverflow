"""
Application configuration module
"""

class AppConfig:
    # App color scheme
    PRIMARY_COLOR = "#2E7D32"  # Dark green
    SECONDARY_COLOR = "#C62828"  # Dark red
    BG_COLOR = "#F5F5F5"  # Light grey
    LIGHTY_COLOR = "#f5f5d5" # Light Yellow
    ORANGE_COLOR = "#FFA500" # Orange
    TEXT_COLOR = "#212121"  # Dark grey
    
    # App name
    APP_NAME = "StockOverflow"
    
    # Data directory
    DATA_DIR = "data"
    
    # User roles
    ROLES = ["Admin", "Staff"]
    
    # Button styles
    BUTTON_STYLES = {
        "primary": {
            "bg": PRIMARY_COLOR,
            "fg": "white",
            "activebackground": "#388E3C",
            "activeforeground": "white",
            "relief": "raised",
            "border": 0,
            "padx": 10,
            "pady": 5,
            "font": ("Helvetica", 10, "bold")
        },
        "secondary": {
            "bg": SECONDARY_COLOR,
            "fg": "white",
            "activebackground": "#D32F2F",
            "activeforeground": "white",
            "relief": "raised",
            "border": 0,
            "padx": 10,
            "pady": 5,
            "font": ("Helvetica", 10, "bold")
        }
    }
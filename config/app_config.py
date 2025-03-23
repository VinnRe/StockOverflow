class AppConfig:
    # App name
    APP_NAME = "Stock Overflow"
    
    # Colors
    BG_COLOR = "#f5f5f5"
    TEXT_COLOR = "#333333"
    PRIMARY_COLOR = "#4CAF50"  # Green
    SECONDARY_COLOR = "#F44336"  # Red
    LIGHTY_COLOR = "#2196F3"  # Blue for low stock
    ORANGE_COLOR = "#FF9800"  # Orange for near expiry
    
    # Button styles
    BUTTON_STYLES = {
        "primary": {
            "bg": PRIMARY_COLOR,
            "fg": "white",
            "font": ("Helvetica", 12, "bold"),
            "relief": "raised",
            "bd": 1,
            "padx": 10,
            "pady": 5,
            "cursor": "hand2"
        },
        "secondary": {
            "bg": SECONDARY_COLOR,
            "fg": "white",
            "font": ("Helvetica", 12, "bold"),
            "relief": "raised",
            "bd": 1,
            "padx": 10,
            "pady": 5,
            "cursor": "hand2"
        }
    }
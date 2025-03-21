#!/usr/bin/env python3
"""
StockOverflow - Restaurant Inventory Management System
Main entry point of the application
"""

import os
import sys
from config.app_config import AppConfig
from models.database import Database
from ui.app import StockOverflowApp

def main():
    """Main function to run the app"""
    app = StockOverflowApp()
    app.mainloop()


if __name__ == "__main__":
    main()
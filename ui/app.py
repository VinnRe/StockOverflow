import tkinter as tk
from tkinter import ttk, messagebox, font
import os
from PIL import Image, ImageTk
import json
from datetime import datetime, timedelta

from config.app_config import AppConfig
from models.database import Database
from ui.inventory_page import InventoryPage
from ui.recipe_page import RecipePage
from ui.order_page import OrderPage
from ui.analytics_page import AnalyticsPage

class StockOverflowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # App configuration
        self.config = AppConfig()
        
        # Database connection
        self.db = Database()
        
        # Main app setup
        self.title(self.config.APP_NAME)
        self.geometry("900x700")
        self.configure(bg=self.config.BG_COLOR)
        
        # Current user (mock for now)
        self.current_user = {"username": "admin", "role": "Admin"}
        
        # Initialize UI components
        self.create_custom_fonts()
        self.create_ui()
        
    def create_custom_fonts(self):
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=10)
        self.button_font = font.Font(family="Helvetica", size=10, weight="bold")
    
    def create_ui(self):
        # Create main container frame
        self.main_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create navigation bar
        self.create_navbar()
        
        # Create content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.config.BG_COLOR, bd=2, relief=tk.GROOVE)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Default to showing inventory
        self.show_inventory()
    
    def create_navbar(self):
        navbar = tk.Frame(self.main_frame, bg=self.config.BG_COLOR, bd=2, relief=tk.GROOVE)
        navbar.pack(fill=tk.X, pady=5)
        
        # Create a frame for the navigation buttons to ensure even spacing
        nav_buttons_frame = tk.Frame(navbar, bg=self.config.BG_COLOR)
        nav_buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Configure the grid to have 4 equal columns
        for i in range(4):
            nav_buttons_frame.columnconfigure(i, weight=1)
        
        # Custom button style with rounded corners and green outline for navigation buttons
        green_button_style = {
            "bg": AppConfig.PRIMARY_COLOR,
            "fg": "white",
            "font": self.button_font,
            "relief": tk.GROOVE,
            "bd": 2,
            "padx": 20,
            "pady": 10,
            "width": 12,
            "highlightbackground": "green",
            "highlightcolor": "green",
            "highlightthickness": 2
        }
        
        # Red button style for Switch Profile
        red_button_style = {
            "bg": AppConfig.SECONDARY_COLOR,
            "fg": "white",
            "font": self.button_font,
            "relief": tk.GROOVE,
            "bd": 2,
            "padx": 20,
            "pady": 10,
            "width": 12,
            "highlightbackground": "darkred",
            "highlightcolor": "darkred",
            "highlightthickness": 2
        }
        
        # Inventory button
        self.inventory_btn = tk.Button(
            nav_buttons_frame, 
            text="Inventory",
            command=self.show_inventory,
            **green_button_style
        )
        self.inventory_btn.grid(row=0, column=0, padx=5)
        
        # Recipes button
        self.recipes_btn = tk.Button(
            nav_buttons_frame, 
            text="Recipes",
            command=self.show_recipes,
            **green_button_style
        )
        self.recipes_btn.grid(row=0, column=1, padx=5)
        
        # Orders button
        self.orders_btn = tk.Button(
            nav_buttons_frame, 
            text="Orders",
            command=self.show_orders,
            **green_button_style
        )
        self.orders_btn.grid(row=0, column=2, padx=5)
        
        # # Analytics button
        # self.analytics_btn = tk.Button(
        #     nav_buttons_frame, 
        #     text="Analytics",
        #     command=self.show_analytics,
        #     **green_button_style
        # )
        # self.analytics_btn.grid(row=0, column=3, padx=5)
        
        # Profile button (Switch Profile) - with red outline
        self.profile_btn = tk.Button(
            nav_buttons_frame, 
            text="Switch Profile",
            command=self.switch_profile,
            **red_button_style
        )
        self.profile_btn.grid(row=0, column=3, padx=5)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_inventory(self):
        self.clear_content()
        inventory_page = InventoryPage(
            self.content_frame, 
            self.db, 
            self.config, 
            self.current_user,
            self.title_font,
            self.header_font,
            self.normal_font
        )
        inventory_page.pack(fill=tk.BOTH, expand=True)
    
    def show_recipes(self):
        self.clear_content()
        recipe_page = RecipePage(
            self.content_frame, 
            self.db, 
            self.config, 
            self.current_user,
            self.title_font,
            self.header_font,
            self.normal_font
        )
        recipe_page.pack(fill=tk.BOTH, expand=True)
    
    def show_orders(self):
        self.clear_content()
        order_page = OrderPage(
            self.content_frame, 
            self.db, 
            self.config, 
            self.current_user,
            self.title_font,
            self.header_font,
            self.normal_font
        )
        order_page.pack(fill=tk.BOTH, expand=True)
    
    # def show_analytics(self):
    #     self.clear_content()
    #     analytics_page = AnalyticsPage(
    #         self.content_frame, 
    #         self.db, 
    #         self.config, 
    #         self.current_user,
    #         self.title_font,
    #         self.header_font,
    #         self.normal_font
    #     )
    #     analytics_page.pack(fill=tk.BOTH, expand=True)
    
    def switch_profile(self):
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Switch User Profile")
        dialog.geometry("300x200")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 300, 200)
        
        # Add profile selection options
        tk.Label(
            dialog, 
            text="Select User Profile:",
            font=self.header_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(pady=10)
        
        # Role selection
        role_var = tk.StringVar(value=self.current_user["role"])
        tk.Radiobutton(
            dialog, 
            text="Admin", 
            variable=role_var, 
            value="Admin",
            bg=self.config.BG_COLOR
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        tk.Radiobutton(
            dialog, 
            text="Staff", 
            variable=role_var, 
            value="Staff",
            bg=self.config.BG_COLOR
        ).pack(anchor=tk.W, padx=20, pady=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Switch button
        switch_btn = tk.Button(
            button_frame, 
            text="Switch Profile",
            command=lambda: self.change_user_profile(role_var.get(), dialog),
            **self.config.BUTTON_STYLES["primary"]
        )
        switch_btn.pack(side=tk.LEFT, padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10)
    
    def change_user_profile(self, role, dialog):

        self.current_user["role"] = role
        
        messagebox.showinfo("Profile Changed", f"User profile changed to: {role}")
        
        dialog.destroy()
        
        if self.content_frame.winfo_children():
            current_page = self.content_frame.winfo_children()[0].winfo_children()[0].cget("text")
            if "Inventory" in current_page:
                self.show_inventory()
            elif "Recipe" in current_page:
                self.show_recipes()
            elif "Order" in current_page:
                self.show_orders()
            elif "Analytics" in current_page:
                self.show_analytics()
    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime, timedelta

from config.app_config import AppConfig
from models.database import Database
from ui.inventory_page import InventoryPage
from ui.recipe_page import RecipePage
from ui.order_page import OrderPage
from models.user import Admin

class StockOverflowApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.navbar = None
        
        # App configuration
        self.config = AppConfig()
        
        # Database connection
        self.db = Database()
        
        # Main app setup
        self.title(self.config.APP_NAME)
        self.geometry("900x700")
        self.configure(bg=self.config.BG_COLOR)
        
        # Current user (mock for now)
        self.current_user = {"username": "staff", "role": "Staff"}
        
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
        
        # Default to showing recipes
        self.show_recipes()
    
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

        # Recipes button
        self.recipes_btn = tk.Button(
            nav_buttons_frame, 
            text="Recipes",
            command=self.show_recipes,
            **green_button_style
        )
        self.recipes_btn.grid(row=0, column=0, padx=5)
        
        # Inventory button
        self.inventory_btn = tk.Button(
            nav_buttons_frame, 
            text="Inventory",
            command=self.show_inventory,
            **green_button_style
        )
        self.inventory_btn.grid(row=0, column=1, padx=5)
        
        # Orders button
        self.orders_btn = tk.Button(
            nav_buttons_frame, 
            text="Orders",
            command=self.show_orders,
            **green_button_style
        )
        self.orders_btn.grid(row=0, column=2, padx=5)

        button_text = "Logout" if self.current_user.get("role") == "Admin" else "Admin Access"
        button_command = self.handle_logout if self.current_user.get("role") == "Admin" else self.switch_profile

        self.profile_btn = tk.Button(
            nav_buttons_frame, text=button_text, command=button_command, **red_button_style
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
    
    def switch_profile(self):
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Switch User Profile")
        dialog.geometry("300x250")  # Increased height to accommodate login fields
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        # Create an instance of Admin
        self.admin = Admin()

        # Center the dialog on the screen
        self.center_window(dialog, 300, 250)

        # Add username label and entry field
        tk.Label(
            dialog,
            text="Username:",
            font=self.header_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(pady=(10, 0))
        
        username_entry = tk.Entry(dialog)
        username_entry.pack(pady=(0, 10))

        # Add password label and entry field
        tk.Label(
            dialog,
            text="Password:",
            font=self.header_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack()
        
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack(pady=(0, 10))

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=20)

        # Login button
        login_btn = tk.Button(
            button_frame, 
            text="Login",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get(), dialog),
            **self.config.BUTTON_STYLES["primary"]
        )
        login_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10)

    def handle_login(self, username, password, dialog):
        if self.admin.login(username, password):
            messagebox.showinfo("Success", "Login successful!")

            self.current_user = {"username": username, "role": "Admin"}
            dialog.destroy()

            # Update navbar button without recreating the whole navbar
            self.profile_btn.config(text="Logout", command=self.handle_logout)

            self.update_idletasks()
        else:
            messagebox.showwarning("Error", "Invalid username or password.")

    def handle_logout(self):
        if self.current_user.get("role") == "Admin":
            self.admin.logout()
            self.current_user = {"username": "staff", "role": "Staff"}
            messagebox.showinfo("Success", "Logged out successfully.")

            # Update navbar button dynamically
            self.profile_btn.config(text="Admin Access", command=self.switch_profile)

            self.update_idletasks()
        else:
            messagebox.showwarning("Error", "You are not logged in.")
    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
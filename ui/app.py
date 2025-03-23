import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

from config.app_config import AppConfig
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
        # Load environment variables
        load_dotenv()
        DB_URL = os.getenv("DB_URL")

        # Initialize Firebase Admin SDK (Make sure your .env has DB_URL set)
        cred = credentials.Certificate("key.json")  # Update path
        db = firebase_admin.initialize_app(cred, {"databaseURL": DB_URL})

        icon_path = os.path.join(os.path.dirname(__file__), "so_ico.png")
        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        # Main app setup
        self.title(self.config.APP_NAME)
        self.geometry("1000x750")  # Increased window size for better visibility
        self.configure(bg=self.config.BG_COLOR)
        
        # Current user (mock for now)
        self.current_user = {"username": "Staff", "role": "Staff"}
        
        # Initialize UI components
        self.create_custom_fonts()
        self.create_ui()

        # Define style
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 16, "bold"))
        
        # Center the window on screen
        self.center_window(self, 1000, 750)
        
    def create_custom_fonts(self):
        self.title_font = font.Font(family="Helvetica", size=30, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=28, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=20)
        self.button_font = font.Font(family="Helvetica", size=20, weight="bold")
    
    def create_ui(self):
        # Create app header with logo/title
        self.create_app_header()
        
        # Create main container frame
        self.main_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Create navigation bar
        self.create_navbar()
        
        # Create content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.config.BG_COLOR, bd=2, relief=tk.GROOVE)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create status bar
        self.create_status_bar()
        
        # Default to showing recipes
        self.show_recipes()
    
    def create_app_header(self):
        """Create an app header with logo and title"""
        header_frame = tk.Frame(self, bg=self.config.PRIMARY_COLOR, height=60)
        header_frame.pack(fill=tk.X)
        
        # App title
        app_title = tk.Label(
            header_frame,
            text=self.config.APP_NAME,
            font=("Helvetica", 24, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        app_title.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Current user display
        self.user_label = tk.Label(
            header_frame,
            text=f"User: {self.current_user['username']} ({self.current_user['role']})",
            font=("Helvetica", 12),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        self.user_label.pack(side=tk.RIGHT, padx=20, pady=10)
    
    def create_navbar(self):
        navbar = tk.Frame(self.main_frame, bg=self.config.BG_COLOR, bd=2, relief=tk.GROOVE)
        navbar.pack(fill=tk.X, pady=5)
        
        nav_buttons_frame = tk.Frame(navbar, bg=self.config.BG_COLOR)
        nav_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        for i in range(4):
            nav_buttons_frame.columnconfigure(i, weight=1)
        
        self.green_button_style = {
            "bg": AppConfig.PRIMARY_COLOR,
            "fg": "white",
            "font": self.button_font,
            "relief": tk.RAISED,
            "bd": 2,
            "padx": 20,
            "pady": 10,
            "width": 12,
            "highlightbackground": "green",
            "highlightcolor": "green",
            "highlightthickness": 2,
            "cursor": "hand2" 
        }
        
        self.red_button_style = {
            "bg": AppConfig.SECONDARY_COLOR,
            "fg": "white",
            "font": self.button_font,
            "relief": tk.RAISED,
            "bd": 2,
            "padx": 20,
            "pady": 10,
            "width": 12,
            "highlightbackground": "darkred",
            "highlightcolor": "darkred",
            "highlightthickness": 2,
            "cursor": "hand2"
        }

        self.recipes_btn = tk.Button(
            nav_buttons_frame, 
            text="Recipes",
            command=self.show_recipes,
            **self.green_button_style
        )
        self.recipes_btn.grid(row=0, column=0, padx=10)

        # Initialize inventory and orders buttons as None
        self.inventory_btn = None
        self.orders_btn = None

        # Conditionally create the inventory and orders buttons
        if self.current_user.get("role") == "Admin":
            self.inventory_btn = tk.Button(
                nav_buttons_frame, 
                text="Inventory",
                command=self.show_inventory,
                **self.green_button_style
            )
            self.inventory_btn.grid(row=0, column=1, padx=10)

            self.orders_btn = tk.Button(
                nav_buttons_frame, 
                text="Orders",
                command=self.show_orders,
                **self.green_button_style
            )
            self.orders_btn.grid(row=0, column=2, padx=10)

        button_text = "Logout" if self.current_user.get("role") == "Admin" else "Admin Access"
        button_command = self.handle_logout if self.current_user.get("role") == "Admin" else self.switch_profile

        self.profile_btn = tk.Button(
            nav_buttons_frame, text=button_text, command=button_command, **self.red_button_style
        )
        self.profile_btn.grid(row=0, column=3, padx=10)
    
    def create_status_bar(self):
        """Create a status bar at the bottom of the app"""
        status_frame = tk.Frame(self, bg="#f0f0f0", height=25)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text = f"Stock Overflow System | Current Time: {current_time}"
        
        status_label = tk.Label(
            status_frame,
            text=status_text,
            font=("Helvetica", 10),
            bg="#f0f0f0",
            fg="#333333"
        )
        status_label.pack(side=tk.LEFT, padx=10, pady=3)

    def handle_login(self, username, password, dialog):
        if self.admin.login(username, password):
            messagebox.showinfo("Success", "Login successful!")

            self.current_user = {"username": username, "role": "Admin"}
            dialog.destroy()

            # Update navbar button without recreating the whole navbar
            self.profile_btn.config(text="Logout", command=self.handle_logout)
            
            # Update user label in header
            self.user_label.config(text=f"User: {username} (Admin)")

            # Add Inventory and Orders buttons if they don't exist
            if not self.inventory_btn:
                nav_buttons_frame = self.profile_btn.master #get the parent frame 
                nav_buttons_frame = self.profile_btn.master #get the parent frame
                self.inventory_btn = tk.Button(
                    nav_buttons_frame, 
                    text="Inventory",
                    command=self.show_inventory,
                    **self.green_button_style
                )
                self.inventory_btn.grid(row=0, column=1, padx=10)

            if not self.orders_btn:
                nav_buttons_frame = self.profile_btn.master
                self.orders_btn = tk.Button(
                    nav_buttons_frame, 
                    text="Orders",
                    command=self.show_orders,
                    **self.green_button_style
                )
                self.orders_btn.grid(row=0, column=2, padx=10)

            self.update_idletasks()
        else:
            messagebox.showwarning("Error", "Invalid username or password.")

    def handle_logout(self):
        if self.current_user.get("role") == "Admin":
            self.admin.logout()
            self.current_user = {"username": "staff", "role": "Staff"}
            messagebox.showinfo("Success", "Logged out successfully.")

            self.profile_btn.config(text="Admin Access", command=self.switch_profile)
            
            # Update user label in header
            self.user_label.config(text=f"User: staff (Staff)")

            if self.inventory_btn:
                self.inventory_btn.destroy()
                self.inventory_btn = None
            if self.orders_btn:
                self.orders_btn.destroy()
                self.orders_btn = None

            self.show_recipes()

            self.update_idletasks()
        else:
            messagebox.showwarning("Error", "You are not logged in.")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_inventory(self):
        self.clear_content()
        inventory_page = InventoryPage(
            self.content_frame, 
            db, 
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
            "test", 
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
            "test", 
            self.config, 
            self.current_user,
            self.title_font,
            self.header_font,
            self.normal_font
        )
        order_page.pack(fill=tk.BOTH, expand=True)
    
    def switch_profile(self):
        # Create a dialog window with improved styling
        dialog = tk.Toplevel(self)
        dialog.title("Admin Access")
        dialog.geometry("400x350")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()

        self.admin = Admin()

        self.center_window(dialog, 400, 350)
        
        # Add header
        header_frame = tk.Frame(dialog, bg=self.config.PRIMARY_COLOR, height=40)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Admin Login", 
            font=("Helvetica", 16, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        header_label.pack(pady=8)
        
        # Content frame
        content_frame = tk.Frame(dialog, bg=self.config.BG_COLOR, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Add username label and entry field
        tk.Label(
            content_frame,
            text="Username:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        username_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        username_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)
        username_entry.focus_set()

        # Add password label and entry field
        tk.Label(
            content_frame,
            text="Password:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        password_entry = tk.Entry(content_frame, show="*", font=("Helvetica", 12), width=30)
        password_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        button_frame = tk.Frame(content_frame, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=20)

        login_btn = tk.Button(
            button_frame, 
            text="Login",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get(), dialog),
            **self.config.BUTTON_STYLES["primary"]
        )
        login_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=10)
        
        dialog.bind('<Return>', lambda event: self.handle_login(username_entry.get(), password_entry.get(), dialog))
    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
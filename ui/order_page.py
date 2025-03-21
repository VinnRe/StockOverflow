import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class OrderPage(tk.Frame):
    
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)
        
        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font
        
        # Create UI components
        self.create_ui()
        
    def create_ui(self):
        # Create header
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(
            header, 
            text="Order Management",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Add order button
        add_btn = tk.Button(
            header, 
            text="New Order",
            command=self.create_new_order,
            **self.config.BUTTON_STYLES["primary"]
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create orders table
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a treeview for the orders
        columns = ("ID", "Date", "Items", "Total", "Status", "Actions")
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        self.orders_tree.heading("ID", text="ID")
        self.orders_tree.heading("Date", text="Date")
        self.orders_tree.heading("Items", text="Items")
        self.orders_tree.heading("Total", text="Total")
        self.orders_tree.heading("Status", text="Status")
        self.orders_tree.heading("Actions", text="Actions")
        
        # Configure column widths
        self.orders_tree.column("ID", width=50)
        self.orders_tree.column("Date", width=100)
        self.orders_tree.column("Items", width=200)
        self.orders_tree.column("Total", width=100)
        self.orders_tree.column("Status", width=100)
        self.orders_tree.column("Actions", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.orders_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_new_order(self):
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Create New Order")
        dialog.geometry("400x300")  # Increased height to fit additional fields
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 400, 300)

        # Name
        tk.Label(dialog, text="Name:", bg=self.config.BG_COLOR, font=self.normal_font).pack(anchor="w", padx=10, pady=(10, 0))
        name_entry = tk.Entry(dialog)
        name_entry.pack(fill=tk.X, padx=10, pady=2)

        # Quantity
        tk.Label(dialog, text="Quantity:", bg=self.config.BG_COLOR, font=self.normal_font).pack(anchor="w", padx=10, pady=(10, 0))
        quantity_entry = tk.Spinbox(dialog, from_=1, to=100, width=5)
        quantity_entry.pack(fill=tk.X, padx=10, pady=2)

        # Unit of Measurement
        tk.Label(dialog, text="Unit of Measurement:", bg=self.config.BG_COLOR, font=self.normal_font).pack(anchor="w", padx=10, pady=(10, 0))
        unit_entry = tk.Entry(dialog)
        unit_entry.pack(fill=tk.X, padx=10, pady=2)

        # Category
        tk.Label(dialog, text="Category:", bg=self.config.BG_COLOR, font=self.normal_font).pack(anchor="w", padx=10, pady=(10, 0))
        category_entry = tk.Entry(dialog)
        category_entry.pack(fill=tk.X, padx=10, pady=2)

        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)

        # Create order button
        create_btn = tk.Button(
            button_frame, 
            text="Create Order",
            command=lambda: self.process_new_order(name_entry.get(), quantity_entry.get(), unit_entry.get(), category_entry.get(), dialog),
            **self.config.BUTTON_STYLES["primary"]
        )
        create_btn.pack(side=tk.LEFT, padx=5)

        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

    def process_new_order(self, name, quantity, unit, category, dialog):
        if not name or not unit or not category:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        messagebox.showinfo("Order Created", f"Order: {name}, Quantity: {quantity} {unit}, Category: {category}")
        dialog.destroy()

    def show_items(self):
        # ADD ITEMS THAT HAS A RECEIVE BUTTON THAT WILL DESTROY THE RECIEVED ITEM BUT THEN ADD QUANTITY TO THE DB
        pass

    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
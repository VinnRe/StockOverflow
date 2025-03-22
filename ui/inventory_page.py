import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from controllers.food_inventory_controller import FoodInventory

class InventoryPage(tk.Frame):
    
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)
        
        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font
        
        self.inventory_data = FoodInventory().displayItems()

        # Create UI components
        self.create_ui()
        
        # Load inventory data
        self.load_inventory_data()
    
    def create_ui(self):
        # Create header
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(
            header, 
            text="Inventory Management",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Add item button (only for Admin)
        if self.current_user["role"] == "Admin":
            add_btn = tk.Button(
                header, 
                text="Add Item",
                command=self.add_inventory_item,
                **self.config.BUTTON_STYLES["primary"]
            )
            add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create table
        self.tree = ttk.Treeview(table_frame, columns=("itemName", "stock", "totalQuantity"), show='headings')
        self.tree.heading("itemName", text="Item Name")
        self.tree.heading("stock", text="Expiry Date")
        self.tree.heading("totalQuantity", text="Quantity")
        
        self.tree.column("itemName", width=150, anchor="center")
        self.tree.column("stock", width=120, anchor="center")
        self.tree.column("totalQuantity", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def load_inventory_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if self.inventory_data:
            for item_dict in self.inventory_data:
                for item_id, item_details in item_dict.items():
                    item_name = item_details.get("itemName", "N/A")
                    stock = item_details.get("stock", {})
                    total_quantity = item_details.get("totalQuantity", "0")

                    expiry_dates = ", ".join(stock.keys()) if stock else "N/A"

                    self.tree.insert("", "end", values=(item_name, expiry_dates, total_quantity))
        else:
            print("No inventory data found.")

    
    def add_inventory_item(self):
        messagebox.showinfo("Add Item", "Feature not implemented yet!")
    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")

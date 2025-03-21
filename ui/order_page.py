"""
Order management UI for StockOverflow
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class OrderPage(tk.Frame):
    """Order management page"""
    
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
        """Create the order page UI"""
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
        
        # Bind double-click event
        self.orders_tree.bind("<Double-1>", self.on_order_select)
        
        # Load order data
        self.load_order_data()
    
    def load_order_data(self):
        """Load order data into the treeview"""
        # Clear existing items
        for i in self.orders_tree.get_children():
            self.orders_tree.delete(i)
        
        # Get order data
        orders = self.db.get_orders()
        recipes = self.db.get_recipes()
        
        # Add items to treeview
        for order in orders:
            # Get recipe names for items
            items_text = ""
            for item in order["items"]:
                recipe = next((r for r in recipes if r["id"] == item["recipe_id"]), None)
                if recipe:
                    items_text += f"{recipe['name']} (x{item['quantity']}), "
            
            # Remove trailing comma
            if items_text:
                items_text = items_text[:-2]
            
            order_values = (
                order["id"],
                order["date"],
                items_text,
                f"${order['total']:.2f}",
                order["status"],
                "View/Edit"
            )
            
            # Add order to treeview
            item_id = self.orders_tree.insert("", tk.END, values=order_values)
            
            # Highlight in-progress orders
            if order["status"] == "In Progress":
                self.orders_tree.item(item_id, tags=("in_progress",))
        
        # Configure tag colors
        self.orders_tree.tag_configure("in_progress", background="#E3F2FD")  # Light blue
    
    def on_order_select(self, event):
        """Handle order selection (double-click)"""
        # Get the selected item
        selection = self.orders_tree.selection()
        if not selection:
            return
        
        # Get the item values
        item_values = self.orders_ 
        return
        
        # Get the item values
        item_values = self.orders_tree.item(selection[0], "values")
        order_id = int(item_values[0])
        
        # Show order details in a dialog
        self.show_order_details(order_id)
    
    def show_order_details(self, order_id):
        """Show order details in a dialog"""
        # Get order data
        orders = self.db.get_orders()
        recipes = self.db.get_recipes()
        
        # Find the order
        order = next((o for o in orders if o["id"] == order_id), None)
        if not order:
            messagebox.showerror("Error", f"Order with ID {order_id} not found")
            return
        
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title(f"Order Details: #{order['id']}")
        dialog.geometry("500x400")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 500, 400)
        
        # Add order details
        details_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Order ID and date
        tk.Label(details_frame, text=f"Order #{order['id']} - {order['date']}", font=self.title_font, bg=self.config.BG_COLOR).pack(anchor=tk.W, pady=5)
        
        # Order status
        status_frame = tk.Frame(details_frame, bg=self.config.BG_COLOR)
        status_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(status_frame, text="Status:", font=self.header_font, bg=self.config.BG_COLOR).pack(side=tk.LEFT, padx=5)
        
        status_var = tk.StringVar(value=order["status"])
        status_options = ["In Progress", "Completed", "Cancelled"]
        status_menu = tk.OptionMenu(status_frame, status_var, *status_options)
        status_menu.pack(side=tk.LEFT, padx=5)
        
        # Update status button
        update_status_btn = tk.Button(
            status_frame, 
            text="Update Status",
            command=lambda: self.update_order_status(order_id, status_var.get(), dialog),
            **self.config.BUTTON_STYLES["primary"]
        )
        update_status_btn.pack(side=tk.LEFT, padx=10)
        
        # Order items
        tk.Label(details_frame, text="Order Items:", font=self.header_font, bg=self.config.BG_COLOR).pack(anchor=tk.W, pady=5)
        
        # Items list
        items_frame = tk.Frame(details_frame, bg=self.config.BG_COLOR)
        items_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a treeview for the items
        columns = ("Item", "Quantity", "Price", "Subtotal")
        items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=5)
        
        # Configure columns
        items_tree.heading("Item", text="Item")
        items_tree.heading("Quantity", text="Quantity")
        items_tree.heading("Price", text="Price")
        items_tree.heading("Subtotal", text="Subtotal")
        
        # Configure column widths
        items_tree.column("Item", width=200)
        items_tree.column("Quantity", width=70)
        items_tree.column("Price", width=70)
        items_tree.column("Subtotal", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(items_frame, orient=tk.VERTICAL, command=items_tree.yview)
        items_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        items_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add items to treeview
        total = 0
        for item in order["items"]:
            recipe = next((r for r in recipes if r["id"] == item["recipe_id"]), None)
            if recipe:
                subtotal = recipe["cost"] * item["quantity"]
                total += subtotal
                item_values = (
                    recipe["name"],
                    item["quantity"],
                    f"${recipe['cost']:.2f}",
                    f"${subtotal:.2f}"
                )
                items_tree.insert("", tk.END, values=item_values)
        
        # Total
        total_frame = tk.Frame(details_frame, bg=self.config.BG_COLOR)
        total_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(total_frame, text="Total:", font=self.header_font, bg=self.config.BG_COLOR).pack(side=tk.LEFT, padx=5)
        tk.Label(total_frame, text=f"${order['total']:.2f}", font=self.header_font, bg=self.config.BG_COLOR).pack(side=tk.LEFT, padx=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Close button
        close_btn = tk.Button(
            button_frame, 
            text="Close",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_order_status(self, order_id, status, dialog):
        """Update an order's status"""
        # Update the order
        success = self.db.update_order_status(order_id, status)
        
        if success:
            messagebox.showinfo("Success", f"Order #{order_id} status updated to {status}")
            dialog.destroy()
            # Refresh order data
            self.load_order_data()
        else:
            messagebox.showerror("Error", "Failed to update order status")
    
    def create_new_order(self):
        """Create a new order"""
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Create New Order")
        dialog.geometry("600x500")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 600, 500)
        
        # Get recipes
        recipes = self.db.get_recipes()
        
        # Add order form
        form_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Available recipes
        tk.Label(form_frame, text="Available Recipes:", font=self.header_font, bg=self.config.BG_COLOR).pack(anchor=tk.W, pady=5)
        
        # Recipes list
        recipes_frame = tk.Frame(form_frame, bg=self.config.BG_COLOR)
        recipes_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create a treeview for the recipes
        columns = ("ID", "Name", "Category", "Price", "Add")
        recipes_tree = ttk.Treeview(recipes_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        recipes_tree.heading("ID", text="ID")
        recipes_tree.heading("Name", text="Name")
        recipes_tree.heading("Category", text="Category")
        recipes_tree.heading("Price", text="Price")
        recipes_tree.heading("Add", text="Add")
        
        # Configure column widths
        recipes_tree.column("ID", width=50)
        recipes_tree.column("Name", width=200)
        recipes_tree.column("Category", width=150)
        recipes_tree.column("Price", width=70)
        recipes_tree.column("Add", width=70)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(recipes_frame, orient=tk.VERTICAL, command=recipes_tree.yview)
        recipes_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        recipes_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add recipes to treeview
        for recipe in recipes:
            recipe_values = (
                recipe["id"],
                recipe["name"],
                recipe["category"],
                f"${recipe['cost']:.2f}",
                "Add"
            )
            recipes_tree.insert("", tk.END, values=recipe_values)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Create order button
        create_btn = tk.Button(
            button_frame, 
            text="Create Order",
            command=lambda: messagebox.showinfo("Not Implemented", "Create order functionality not fully implemented in this demo"),
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
    
    def center_window(self, window, width, height):
        """Center a window on the screen"""
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
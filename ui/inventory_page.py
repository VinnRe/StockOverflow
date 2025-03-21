import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class InventoryPage(tk.Frame):
    
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
        
        # Create inventory table
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a treeview for the inventory
        columns = ("ID", "Name", "Quantity", "Unit", "Expiry", "Category", "Actions")
        self.inventory_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        self.inventory_tree.heading("ID", text="ID")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Unit", text="Unit")
        self.inventory_tree.heading("Expiry", text="Expiry Date")
        self.inventory_tree.heading("Category", text="Category")
        self.inventory_tree.heading("Actions", text="Actions")
        
        # Configure column widths
        self.inventory_tree.column("ID", width=50)
        self.inventory_tree.column("Name", width=150)
        self.inventory_tree.column("Quantity", width=100)
        self.inventory_tree.column("Unit", width=70)
        self.inventory_tree.column("Expiry", width=120)
        self.inventory_tree.column("Category", width=120)
        self.inventory_tree.column("Actions", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event
        self.inventory_tree.bind("<Double-1>", self.on_inventory_item_select)
        
        # Load inventory data
        self.load_inventory_data()
    
    def load_inventory_data(self):
        # Clear existing items
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)
        
        # Get inventory data
        inventory = self.db.get_inventory()
        
        # Add items to treeview
        for item in inventory:
            # Check if item is low in stock (example: less than 10)
            item_values = (
                item["id"],
                item["name"],
                item["quantity"],
                item["unit"],
                item["expiry"],
                item["category"],
                "Edit/Delete"
            )
            
            # Add item to treeview
            item_id = self.inventory_tree.insert("", tk.END, values=item_values)
            
            # Highlight items that are low in stock or expiring soon
            if item["quantity"] < 10:
                self.inventory_tree.item(item_id, tags=("low_stock",))
            
            # Check if item is expiring soon (within 7 days)
            try:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d")
                if (expiry_date - datetime.now()).days < 7:
                    self.inventory_tree.item(item_id, tags=("expiring_soon",))
            except:
                pass
        
        # Configure tag colors
        self.inventory_tree.tag_configure("low_stock", background="#FFF9C4")  # Light yellow
        self.inventory_tree.tag_configure("expiring_soon", background="#FFCDD2")  # Light red
    
    def on_inventory_item_select(self, event):
        # Get the selected item
        selection = self.inventory_tree.selection()
        if not selection:
            return
        
        # Get the item values
        item_values = self.inventory_tree.item(selection[0], "values")
        item_id = int(item_values[0])
        
        # Show item details in a dialog
        self.show_item_details(item_id)
    
    def show_item_details(self, item_id):
        # Get inventory data
        inventory = self.db.get_inventory()
        
        # Find the item
        item = next((i for i in inventory if i["id"] == item_id), None)
        if not item:
            messagebox.showerror("Error", f"Item with ID {item_id} not found")
            return
        
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title(f"Item Details: {item['name']}")
        dialog.geometry("400x300")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 400, 300)
        
        # Add item details
        details_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Item name
        tk.Label(details_frame, text="Name:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=item["name"])
        name_entry = tk.Entry(details_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Item quantity
        tk.Label(details_frame, text="Quantity:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_var = tk.StringVar(value=str(item["quantity"]))
        quantity_entry = tk.Entry(details_frame, textvariable=quantity_var, width=10)
        quantity_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Item unit
        tk.Label(details_frame, text="Unit:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=2, column=0, sticky=tk.W, pady=5)
        unit_var = tk.StringVar(value=item["unit"])
        unit_entry = tk.Entry(details_frame, textvariable=unit_var, width=10)
        unit_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Item expiry
        tk.Label(details_frame, text="Expiry Date:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=3, column=0, sticky=tk.W, pady=5)
        expiry_var = tk.StringVar(value=item["expiry"])
        expiry_entry = tk.Entry(details_frame, textvariable=expiry_var, width=15)
        expiry_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Item category
        tk.Label(details_frame, text="Category:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=4, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar(value=item["category"])
        category_entry = tk.Entry(details_frame, textvariable=category_var, width=20)
        category_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Save button
        save_btn = tk.Button(
            button_frame, 
            text="Save Changes",
            command=lambda: self.save_item_changes(
                item_id, 
                name_var.get(), 
                float(quantity_var.get()), 
                unit_var.get(), 
                expiry_var.get(), 
                category_var.get(),
                dialog
            ),
            **self.config.BUTTON_STYLES["primary"]
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete button (only for Admin)
        if self.current_user["role"] == "Admin":
            delete_btn = tk.Button(
                button_frame, 
                text="Delete Item",
                command=lambda: self.delete_item(item_id, dialog),
                **self.config.BUTTON_STYLES["secondary"]
            )
            delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Disable name and category fields for Staff users
        if self.current_user["role"] != "Admin":
            name_entry.configure(state="disabled")
            category_entry.configure(state="disabled")
    
    def save_item_changes(self, item_id, name, quantity, unit, expiry, category, dialog):
        # Create updates dict
        updates = {
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "expiry": expiry,
            "category": category
        }
        
        # Update the item
        success = self.db.update_inventory_item(item_id, updates)
        
        if success:
            messagebox.showinfo("Success", f"Item {name} updated successfully")
            dialog.destroy()
            # Refresh inventory data
            self.load_inventory_data()
        else:
            messagebox.showerror("Error", "Failed to update item")
    
    def delete_item(self, item_id, dialog):
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this item?")
        if not confirm:
            return
        
        # Delete the item
        success = self.db.delete_inventory_item(item_id)
        
        if success:
            messagebox.showinfo("Success", "Item deleted successfully")
            dialog.destroy()
            # Refresh inventory data
            self.load_inventory_data()
        else:
            messagebox.showerror("Error", "Failed to delete item")
    
    def add_inventory_item(self):
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add New Inventory Item")
        dialog.geometry("400x300")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 400, 300)
        
        # Add item details form
        details_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Item name
        tk.Label(details_frame, text="Name:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Item quantity
        tk.Label(details_frame, text="Quantity:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=quantity_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Item unit
        tk.Label(details_frame, text="Unit:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=2, column=0, sticky=tk.W, pady=5)
        unit_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=unit_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Item expiry
        tk.Label(details_frame, text="Expiry Date:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=3, column=0, sticky=tk.W, pady=5)
        expiry_var = tk.StringVar(value=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        tk.Entry(details_frame, textvariable=expiry_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Item category
        tk.Label(details_frame, text="Category:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=4, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        categories = ["Vegetables", "Meat", "Dairy", "Dry Goods", "Oils", "Spices", "Beverages", "Other"]
        tk.OptionMenu(details_frame, category_var, *categories).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add button
        add_btn = tk.Button(
            button_frame, 
            text="Add Item",
            command=lambda: self.save_new_item(
                name_var.get(), 
                quantity_var.get(), 
                unit_var.get(), 
                expiry_var.get(), 
                category_var.get(),
                dialog
            ),
            **self.config.BUTTON_STYLES["primary"]
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Cancel",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
    
    def save_new_item(self, name, quantity, unit, expiry, category, dialog):
        # Validate inputs
        if not name or not quantity or not unit or not expiry or not category:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            quantity = float(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return
        
        # Create new item
        new_item = {
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "expiry": expiry,
            "category": category
        }
        
        # Add the item
        success = self.db.add_inventory_item(new_item)
        
        if success:
            messagebox.showinfo("Success", f"Item {name} added successfully")
            dialog.destroy()
            # Refresh inventory data
            self.load_inventory_data()
        else:
            messagebox.showerror("Error", "Failed to add item")
    
    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
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
        
        self.inventory_data = FoodInventory().displayItems().get("inventory_list", [])

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
        self.tree.column("stock", width=200, anchor="center")
        self.tree.column("totalQuantity", width=80, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind double-click event to open item details
        self.tree.bind("<Double-1>", self.on_item_double_click)

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

    def on_item_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_values = self.tree.item(selected_item, "values")
        if item_values:
            item_name = item_values[0]
            expiry_dates = item_values[1]
            total_quantity = item_values[2]

            # Create pop-up window
            dialog = tk.Toplevel(self)
            dialog.title("Item Details")
            dialog.geometry("300x250")
            self.center_window(dialog, 300, 250)

            tk.Label(dialog, text=f"Item Name:", font=self.normal_font).pack(pady=5)
            item_name_var = tk.StringVar(value=item_name)
            item_name_entry = tk.Entry(dialog, textvariable=item_name_var, state="normal" if self.current_user["role"] == "Admin" else "readonly")
            item_name_entry.pack(pady=2)

            tk.Label(dialog, text=f"Expiry Dates:", font=self.normal_font).pack(pady=5)
            expiry_dates_var = tk.StringVar(value=expiry_dates)
            expiry_dates_entry = tk.Entry(dialog, textvariable=expiry_dates_var, state="normal" if self.current_user["role"] == "Admin" else "readonly")
            expiry_dates_entry.pack(pady=2)

            tk.Label(dialog, text=f"Total Quantity:", font=self.normal_font).pack(pady=5)
            total_quantity_var = tk.StringVar(value=total_quantity)
            total_quantity_entry = tk.Entry(dialog, textvariable=total_quantity_var, state="normal" if self.current_user["role"] == "Admin" else "readonly")
            total_quantity_entry.pack(pady=2)

            def save_changes():
                """Save the updated details only if user is an admin."""
                if self.current_user["role"] != "Admin":
                    return

                new_item_name = item_name_var.get()
                new_expiry_dates = expiry_dates_var.get()
                new_total_quantity = total_quantity_var.get()

                if not new_total_quantity.isdigit():
                    messagebox.showerror("Error", "Total quantity must be a number.")
                    return

                # Logic to update the item in Firebase
                item_id = None
                for item_dict in self.inventory_data:
                    for key, value in item_dict.items():
                        if value["itemName"] == item_name:
                            item_id = key
                            break

                if item_id:
                    update_data = {
                        "itemName": new_item_name,
                        "stock": {new_expiry_dates: int(new_total_quantity)},
                        "totalQuantity": int(new_total_quantity)
                    }
                    FoodInventory().updateItem(item_id, update_data)
                    messagebox.showinfo("Success", "Item updated successfully!")
                    self.inventory_data = FoodInventory().displayItems()
                    self.load_inventory_data()
                    dialog.destroy()

            def delete_item():
                item_id = None
                for item_dict in self.inventory_data:
                    for key, value in item_dict.items():
                        if value["itemName"] == item_name:
                            item_id = key
                            break

                if item_id:
                    if messagebox.askyesno("Delete Item", f"Are you sure you want to delete '{item_name}'?"):
                        FoodInventory().deleteItem(item_id)
                        messagebox.showinfo("Success", f"Deleted '{item_name}' successfully!")
                        self.inventory_data = FoodInventory().displayItems()
                        self.load_inventory_data()
                        dialog.destroy()
            
            if self.current_user["role"] == "Admin":
                button_frame = tk.Frame(dialog)
                button_frame.pack(pady=10)

                tk.Button(button_frame, text="Save Changes", command=save_changes, **self.config.BUTTON_STYLES["primary"]).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Delete Item", command=delete_item, **self.config.BUTTON_STYLES["secondary"]).pack(side=tk.LEFT, padx=5)

            tk.Button(dialog, text="Close", command=dialog.destroy, **self.config.BUTTON_STYLES["secondary"]).pack(pady=5)

    def add_inventory_item(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Inventory Item")
        dialog.geometry("300x250")
        self.center_window(dialog, 300, 250)

        tk.Label(dialog, text="Item Name:").pack(pady=2)
        item_name_entry = tk.Entry(dialog)
        item_name_entry.pack(pady=2)

        tk.Label(dialog, text="Expiry Date (YYYY-MM-DD):").pack(pady=2)
        expiry_date_entry = tk.Entry(dialog)
        expiry_date_entry.pack(pady=2)

        tk.Label(dialog, text="Stock Quantity:").pack(pady=2)
        stock_quantity_entry = tk.Entry(dialog)
        stock_quantity_entry.pack(pady=2)

        def submit():
            item_name = item_name_entry.get()
            expiry_date = expiry_date_entry.get()
            stock_quantity = stock_quantity_entry.get()

            if not item_name or not expiry_date or not stock_quantity.isdigit():
                messagebox.showerror("Error", "Please enter valid values!")
                return

            try:
                datetime.strptime(expiry_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
                return

            stock_quantity = int(stock_quantity)

            new_item = {
                "itemName": item_name,
                "stock": {expiry_date: stock_quantity},
                "totalQuantity": stock_quantity
            }
            FoodInventory().createItem(new_item)
            messagebox.showinfo("Success", "Item added successfully!")
            dialog.destroy()

            self.inventory_data = FoodInventory().displayItems()
            self.load_inventory_data()

        submit_button = tk.Button(dialog, text="Add Item", command=submit, **self.config.BUTTON_STYLES["primary"])
        submit_button.pack(pady=10)

    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
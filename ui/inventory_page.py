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
        
        self.inventory_data = FoodInventory().displayItems()
        self.create_ui()
        self.load_inventory_data()
    
    def create_ui(self):
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            header, 
            text="Inventory Management",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=15)
        
        if self.current_user["role"] == "Admin":
            self.edit_btn = tk.Button(
                header, 
                text="Edit Item",
                command=self.on_edit_button_click,
                **self.config.BUTTON_STYLES["primary"],
                state=tk.DISABLED
            )
            self.edit_btn.pack(side=tk.RIGHT, padx=15)

            add_btn = tk.Button(
                header, 
                text="Add Item",
                command=self.add_inventory_item,
                **self.config.BUTTON_STYLES["primary"]
            )
            add_btn.pack(side=tk.RIGHT, padx=15)
        
        self.create_legend()
        
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.sort_order = {"itemName": False, "stock": False, "totalQuantity": False}
        
        # Create table with styles
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        
        self.tree = ttk.Treeview(table_frame, columns=("itemName", "stock", "totalQuantity"), show='headings')
        self.tree.heading("itemName", text="Item Name ▼", command=lambda: self.on_column_click("itemName"))
        self.tree.heading("stock", text="Expiry Date", command=lambda: self.on_column_click("stock"))
        self.tree.heading("totalQuantity", text="Quantity", command=lambda: self.on_column_click("totalQuantity"))
        
        self.tree.column("itemName", width=150, anchor="center")
        self.tree.column("stock", width=200, anchor="center")
        self.tree.column("totalQuantity", width=80, anchor="center")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_btn.config(state=tk.NORMAL)
        else:
            self.edit_btn.config(state=tk.DISABLED)
    
    def on_edit_button_click(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.on_item_double_click(None)
    
    def create_legend(self):
        legend_frame = tk.Frame(self, bg=self.config.BG_COLOR, bd=1, relief=tk.GROOVE)
        legend_frame.pack(fill=tk.X, padx=15, pady=5)
        
        legend_title = tk.Label(
            legend_frame,
            text="Color Legend:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        legend_title.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Low stock indicator
        low_stock_frame = tk.Frame(legend_frame, bg=self.config.BG_COLOR)
        low_stock_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        low_stock_color = tk.Frame(low_stock_frame, bg=self.config.LIGHTY_COLOR, width=20, height=20)
        low_stock_color.pack(side=tk.LEFT, padx=5)
        
        low_stock_label = tk.Label(
            low_stock_frame,
            text="Low Stock (<20)",
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        low_stock_label.pack(side=tk.LEFT)
        
        # Near expiry indicator
        near_expiry_frame = tk.Frame(legend_frame, bg=self.config.BG_COLOR)
        near_expiry_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        near_expiry_color = tk.Frame(near_expiry_frame, bg=self.config.ORANGE_COLOR, width=20, height=20)
        near_expiry_color.pack(side=tk.LEFT, padx=5)
        
        near_expiry_label = tk.Label(
            near_expiry_frame,
            text="Near Expiry (<7 days)",
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        near_expiry_label.pack(side=tk.LEFT)
        
        # Both low stock and near expiry
        both_frame = tk.Frame(legend_frame, bg=self.config.BG_COLOR)
        both_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        both_color = tk.Frame(both_frame, bg=self.config.SECONDARY_COLOR, width=20, height=20)
        both_color.pack(side=tk.LEFT, padx=5)
        
        both_label = tk.Label(
            both_frame,
            text="Low Stock & Near Expiry",
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        both_label.pack(side=tk.LEFT)

    def load_inventory_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.tree.tag_configure("low_stock", background=self.config.LIGHTY_COLOR, foreground="white")
        self.tree.tag_configure("near_expiry", background=self.config.ORANGE_COLOR, foreground="black")
        self.tree.tag_configure("low_and_near", background=self.config.SECONDARY_COLOR, foreground="black")

        if self.inventory_data:
            for item_dict in self.inventory_data:
                for item_id, item_details in item_dict.items():
                    item_name = item_details.get("itemName", "N/A")
                    stock = item_details.get("stock", {})
                    total_quantity = item_details.get("totalQuantity", "0")
                    is_low = item_details.get("is_low", False)
                    near_expiry = item_details.get("near_expiry", False)

                    expiry_dates = ", ".join(stock.keys()) if stock else "N/A"

                    if is_low and near_expiry:
                        tag = "low_and_near"
                    elif is_low:
                        tag = "low_stock"
                    elif near_expiry:
                        tag = "near_expiry"
                    else:
                        tag = ""

                    self.tree.insert("", "end", values=(item_name, expiry_dates, total_quantity), tags=(tag,))
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

            dialog = tk.Toplevel(self)
            dialog.title("Item Details")
            dialog.geometry("400x350")
            dialog.configure(bg=self.config.BG_COLOR)
            self.center_window(dialog, 400, 350)

            header_frame = tk.Frame(dialog, bg=self.config.PRIMARY_COLOR, height=40)
            header_frame.pack(fill=tk.X)
            
            header_label = tk.Label(
                header_frame, 
                text="Item Details", 
                font=("Helvetica", 16, "bold"),
                bg=self.config.PRIMARY_COLOR,
                fg="white"
            )
            header_label.pack(pady=8)

            content_frame = tk.Frame(dialog, bg=self.config.BG_COLOR, padx=20, pady=20)
            content_frame.pack(fill=tk.BOTH, expand=True)

            tk.Label(
                content_frame, 
                text="Item Name:", 
                font=("Helvetica", 12, "bold"),
                bg=self.config.BG_COLOR,
                fg=self.config.TEXT_COLOR
            ).pack(anchor="w", pady=(10, 2))
            
            item_name_var = tk.StringVar(value=item_name)
            item_name_entry = tk.Entry(
                content_frame, 
                textvariable=item_name_var, 
                font=("Helvetica", 12),
                state="normal" if self.current_user["role"] == "Admin" else "readonly",
                width=30
            )
            item_name_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

            tk.Label(
                content_frame, 
                text="Expiry Dates:", 
                font=("Helvetica", 12, "bold"),
                bg=self.config.BG_COLOR,
                fg=self.config.TEXT_COLOR
            ).pack(anchor="w", pady=(10, 2))
            
            expiry_dates_var = tk.StringVar(value=expiry_dates)
            expiry_dates_entry = tk.Entry(
                content_frame, 
                textvariable=expiry_dates_var, 
                font=("Helvetica", 12),
                state="normal" if self.current_user["role"] == "Admin" else "readonly",
                width=30
            )
            expiry_dates_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

            tk.Label(
                content_frame, 
                text="Total Quantity:", 
                font=("Helvetica", 12, "bold"),
                bg=self.config.BG_COLOR,
                fg=self.config.TEXT_COLOR
            ).pack(anchor="w", pady=(10, 2))
            
            total_quantity_var = tk.StringVar(value=total_quantity)
            total_quantity_entry = tk.Entry(
                content_frame, 
                textvariable=total_quantity_var, 
                font=("Helvetica", 12),
                state="normal" if self.current_user["role"] == "Admin" else "readonly",
                width=30
            )
            total_quantity_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

            def save_changes():
                if self.current_user["role"] != "Admin":
                    return

                new_item_name = item_name_var.get()
                new_expiry_dates = expiry_dates_var.get()
                new_total_quantity = total_quantity_var.get()

                if not new_total_quantity.isdigit():
                    messagebox.showerror("Error", "Total quantity must be a number.")
                    return

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
            
            button_frame = tk.Frame(content_frame, bg=self.config.BG_COLOR)
            button_frame.pack(fill=tk.X, pady=15)
            
            if self.current_user["role"] == "Admin":
                save_btn = tk.Button(
                    button_frame, 
                    text="Save Changes", 
                    command=save_changes, 
                    **self.config.BUTTON_STYLES["primary"]
                )
                save_btn.pack(side=tk.LEFT, padx=5)
                
                delete_btn = tk.Button(
                    button_frame, 
                    text="Delete Item", 
                    command=delete_item, 
                    **self.config.BUTTON_STYLES["secondary"]
                )
                delete_btn.pack(side=tk.LEFT, padx=5)

            close_btn = tk.Button(
                button_frame, 
                text="Close", 
                command=dialog.destroy, 
                **self.config.BUTTON_STYLES["secondary"]
            )
            close_btn.pack(side=tk.RIGHT, padx=5)

    def add_inventory_item(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Inventory Item")
        dialog.geometry("400x350")
        dialog.configure(bg=self.config.BG_COLOR)
        self.center_window(dialog, 400, 350)

        header_frame = tk.Frame(dialog, bg=self.config.PRIMARY_COLOR, height=40)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Add New Item", 
            font=("Helvetica", 16, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        header_label.pack(pady=8)

        content_frame = tk.Frame(dialog, bg=self.config.BG_COLOR, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            content_frame, 
            text="Item Name:", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        item_name_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        item_name_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Expiry Date (YYYY-MM-DD):", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        expiry_date_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        expiry_date_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Stock Quantity:", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        stock_quantity_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        stock_quantity_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

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

        button_frame = tk.Frame(content_frame, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=15)
        
        submit_button = tk.Button(
            button_frame, 
            text="Add Item", 
            command=submit, 
            **self.config.BUTTON_STYLES["primary"]
        )
        submit_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy, 
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def on_column_click(self, column_name):
        # Toggle sort order
        self.sort_order[column_name] = not self.sort_order[column_name]
        order_symbol = "▲" if self.sort_order[column_name] else "▼"

        self.tree.heading("itemName", text="Item Name")
        self.tree.heading("stock", text="Expiry Date")
        self.tree.heading("totalQuantity", text="Quantity")

        self.tree.heading(column_name, text=f"{column_name.replace('itemName', 'Item Name').replace('stock', 'Expiry Date').replace('totalQuantity', 'Quantity')} {order_symbol}")

        self.inventory_data = FoodInventory().displayItems(column_name, self.sort_order[column_name])
        self.load_inventory_data()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
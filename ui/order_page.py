import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.order_controller import OrderController
from models.order import Order

class OrderPage(tk.Frame):
    
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)
        
        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font

        self.create_ui()
        self.load_orders()

    def create_ui(self):
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(
            header, 
            text="Order Management",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        add_btn = tk.Button(
            header, 
            text="New Order",
            command=self.create_new_order,
            **self.config.BUTTON_STYLES["primary"]
        )
        add_btn.pack(side=tk.RIGHT, padx=5)

        self.receive_btn = tk.Button(
            header,
            text="Receive Order",
            command=self.receive_selected_order,
            state=tk.DISABLED,
            **self.config.BUTTON_STYLES["secondary"]
        )
        self.receive_btn.pack(side=tk.RIGHT, padx=5)

        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("ID", "Date", "Items", "Status")
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.orders_tree.heading("ID", text="ID")
        self.orders_tree.heading("Date", text="Date")
        self.orders_tree.heading("Items", text="Items")
        self.orders_tree.heading("Status", text="Status")
        
        self.orders_tree.column("ID", width=50)
        self.orders_tree.column("Date", width=100)
        self.orders_tree.column("Items", width=200)
        self.orders_tree.column("Status", width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.orders_tree.pack(fill=tk.BOTH, expand=True)

        self.orders_tree.bind("<<TreeviewSelect>>", self.on_row_selected)
        
    def load_orders(self):
        order_controller = OrderController()
        orders = order_controller.get_all_orders()
        self.orders_tree.delete(*self.orders_tree.get_children())
        
        if not orders:
            print("No orders found.")
            return

        for order_id, order_data in orders.items():
            order_date = order_data.get("order_date", "N/A")
            order_content = order_data.get("order_content", {})
            order_status = order_data.get("order_status", "Pending")

            formatted_content = ", ".join(
                [f"{item} ({details['quantity']}) - {details['expiry_date']}"
                for item, details in order_content.items()]
            )

            self.orders_tree.insert(
                "", tk.END, 
                values=(order_id, order_date, formatted_content, order_status)
            )

            print(f"Order ID: {order_id}, Date: {order_date}, Items: {formatted_content}, Status: {order_status}")

    def on_row_selected(self, event):
        # Enable the Receive Order button only if a row is selected and not received
        selected_item = self.orders_tree.selection()
        
        if selected_item:
            order_status = self.orders_tree.item(selected_item, "values")[3]
            
            if order_status == "Received":
                self.receive_btn.config(state=tk.DISABLED)
            else:
                self.receive_btn.config(state=tk.NORMAL)
        else:
            self.receive_btn.config(state=tk.DISABLED)

    def receive_selected_order(self):
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an order first.")
            return
        
        order_id = self.orders_tree.item(selected_item, "values")[0]
        
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to receive Order {order_id}?")
        if not confirm:
            return
        
        order_controller = OrderController()
        order_controller.receive_order(order_id)
        
        messagebox.showinfo("Success", f"Order {order_id} received!")
        
        self.load_orders()
        self.receive_btn.config(state=tk.DISABLED)

    def create_new_order(self):
        dialog = tk.Toplevel(self)
        dialog.title("New Order")
        dialog.geometry("400x350")
        dialog.configure(bg=self.config.BG_COLOR)
        self.center_window(dialog, 400, 350)

        header_frame = tk.Frame(dialog, bg=self.config.PRIMARY_COLOR, height=40)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Place New Order", 
            font=("Helvetica", 16, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        header_label.pack(pady=8)

        content_frame = tk.Frame(dialog, bg=self.config.BG_COLOR, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            content_frame, 
            text="Ingredient Name:", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        ingredient_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        ingredient_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Quantity:", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        quantity_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        quantity_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Expiration Date (YYYY-MM-DD):", 
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        expiry_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        expiry_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        def submit_order():
            ingredient = ingredient_entry.get().strip()
            quantity = quantity_entry.get().strip()
            expiry_date = expiry_entry.get().strip()

            if not ingredient or not quantity or not expiry_date:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                quantity = int(quantity)
                datetime.strptime(expiry_date, "%Y-%m-%d") 
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity or date format!")
                return

            order_content = {ingredient: {"quantity": quantity, "expiry_date": expiry_date}}
            order = Order(order_content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            order_controller = OrderController()
            order_controller.place_order(order)

            messagebox.showinfo("Success", "Order placed successfully!")
            dialog.destroy()
            self.load_orders()

        button_frame = tk.Frame(content_frame, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=15)

        submit_button = tk.Button(
            button_frame, 
            text="Place Order", 
            command=submit_order, 
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

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x}+{y}")

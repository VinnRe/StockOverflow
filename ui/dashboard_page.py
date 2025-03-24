import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from controllers.food_inventory_controller import FoodInventory
from controllers.staff_controller import StaffController
from controllers.order_controller import OrderController

class DashboardPage(tk.Frame):
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)
        
        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font
        
        self.create_ui()
        self.load_dashboard_data()

        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_ui(self):
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=10)
        
        title_label = tk.Label(
            header, 
            text="Admin Dashboard",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=15)
        
        self.timestamp_label = tk.Label(
            header,
            text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Helvetica", 10),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.timestamp_label.pack(side=tk.RIGHT, padx=15)
        
        refresh_btn = tk.Button(
            header,
            text="Refresh",
            command=self.load_dashboard_data,
            **self.config.BUTTON_STYLES["secondary"]
        )
        refresh_btn.pack(side=tk.RIGHT, padx=10)
        
        # Main content area
        self.content_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configure grid layout for buttons and cards
        self.content_frame.columnconfigure(0, weight=0)
        self.content_frame.columnconfigure(1, weight=1)
        
        # Side Menu Buttons
        button_frame = tk.Frame(self.content_frame, bg=self.config.BG_COLOR)
        button_frame.grid(row=0, column=0, sticky="ns", padx=10)

        button_options = self.config.BUTTON_STYLES["primary"]

        buttons = [
            ("Alerts & Notifications", "alert"),
            ("Inventory Summary", "inventory"),
            ("Recipe Summary", "recipe"),
            ("Order Summary", "order"),
        ]

        for i, (label, key) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=label,
                command=lambda k=key: self.show_frame(k),
                **button_options
            ).grid(row=i, column=0, padx=10, pady=5, sticky="ew")

        # Summary Cards
        self.cards = {
            "alert": self.create_summary_card(self.content_frame, "Alerts & Notifications"),
            "inventory": self.create_summary_card(self.content_frame, "Inventory Summary"),
            "recipe": self.create_summary_card(self.content_frame, "Recipe Summary"),
            "order": self.create_summary_card(self.content_frame, "Order Summary"),
        }

        self.show_frame("alert")

    def show_frame(self, frame_key):
        for key, (card, _) in self.cards.items():
            if key == frame_key:
                card.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
            else:
                card.grid_remove()

    def create_summary_card(self, parent, title):
        card = tk.Frame(parent, bg="white", bd=2, relief=tk.RAISED)
        card.grid(row=0, column=1, sticky="nsew")

        header = tk.Frame(card, bg=self.config.PRIMARY_COLOR, height=40)
        header.pack(fill=tk.X)

        title_label = tk.Label(
            header,
            text=title,
            font=("Helvetica", 14, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        title_label.pack(pady=10)

        container = tk.Frame(card, bg="white")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="white")

        def update_frame_width(event):
            canvas.itemconfig(window_id, width=event.width - 15)

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        container.bind("<Configure>", update_frame_width)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return card, scrollable_frame

    def load_dashboard_data(self):
        self.timestamp_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.load_inventory_summary()
        self.load_recipe_summary()
        self.load_order_summary()
        self.load_alerts()
        
    def load_inventory_summary(self):
        try:
            inventory_data = FoodInventory().displayItems()

            total_items = len(inventory_data)
            low_stock_count = 0
            near_expiry_count = 0
            total_quantity = 0
            normal_count = 0

            for item_dict in inventory_data:
                for item_id, item_details in item_dict.items():
                    total_quantity += item_details.get("totalQuantity", 0)
                    if item_details.get("is_low", False) and item_details.get("near_expiry", False):
                        low_stock_count += 1
                        near_expiry_count += 1
                    elif item_details.get("is_low", False):
                        low_stock_count += 1
                    elif item_details.get("near_expiry", False):
                        near_expiry_count += 1
                    else:
                        normal_count += 1

            inventory_card, inventory_content = self.cards["inventory"]

            for widget in inventory_content.winfo_children():
                widget.destroy()

            summary_frame = tk.Frame(inventory_content, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)

            tk.Label(
                summary_frame,
                text=f"Total Items: {total_items}",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Total Quantity: {total_quantity}",
                font=("Helvetica", 12),
                bg="white"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Low Stock Items: {low_stock_count}",
                font=("Helvetica", 12),
                bg="white",
                fg="red" if low_stock_count > 0 else "black"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Near Expiry Items: {near_expiry_count}",
                font=("Helvetica", 12),
                bg="white",
                fg="orange" if near_expiry_count > 0 else "black"
            ).pack(anchor="w", pady=5)

            separator = ttk.Separator(inventory_content, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)

        except Exception as e:
            tk.Label(
                inventory_content,
                text=f"Error loading inventory data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_recipe_summary(self):
        try:
            recipes = StaffController().viewAllRecipes()

            total_recipes = len(recipes)

            recipe_card, recipe_content = self.cards["recipe"]

            for widget in recipe_content.winfo_children():
                widget.destroy()

            summary_frame = tk.Frame(recipe_content, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)

            tk.Label(
                summary_frame,
                text=f"Total Recipes: {total_recipes}",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w", pady=5)

            separator = ttk.Separator(recipe_content, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)

            recent_label = tk.Label(
                recipe_content,
                text="Recent Recipes:",
                font=("Helvetica", 12, "bold"),
                bg="white"
            )
            recent_label.pack(anchor="w", padx=5, pady=5)

            recipe_list_frame = tk.Frame(recipe_content, bg="white")
            recipe_list_frame.pack(fill=tk.X, padx=10, pady=5)

            if recipes:
                ingredient_counts = {}

                for i, recipe_entry in enumerate(recipes[:8]):
                    for recipe_id, recipe_data in recipe_entry.items():
                        recipe_name = recipe_data.get("recipeName", "Unknown Recipe")
                        ingredients = recipe_data.get("ingredients", {})

                        for ingredient in ingredients:
                            if ingredient in ingredient_counts:
                                ingredient_counts[ingredient] += 1
                            else:
                                ingredient_counts[ingredient] = 1

                        recipe_item = tk.Frame(
                            recipe_list_frame, 
                            bg="white", 
                            bd=1, 
                            relief=tk.GROOVE,
                            padx=8,
                            pady=8
                        )
                        recipe_item.pack(fill=tk.X, pady=5)

                        tk.Label(
                            recipe_item,
                            text=recipe_name,
                            font=("Helvetica", 11, "bold"),
                            bg="white"
                        ).pack(anchor="w")

                        ingredients_text = ", ".join(list(ingredients.keys())[:3])
                        if len(ingredients) > 3:
                            ingredients_text += f" and {len(ingredients) - 3} more"

                        tk.Label(
                            recipe_item,
                            text=f"Ingredients: {ingredients_text}",
                            font=("Helvetica", 10),
                            bg="white",
                            fg="grey"
                        ).pack(anchor="w")

                if ingredient_counts:
                    separator2 = ttk.Separator(recipe_content, orient="horizontal")
                    separator2.pack(fill=tk.X, padx=15, pady=10)

                    chart_label = tk.Label(
                        recipe_content,
                        text="Most Used Ingredients",
                        font=("Helvetica", 12, "bold"),
                        bg="white"
                    )
                    chart_label.pack(anchor="w", padx=5, pady=5)

                    top_ingredients = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)[:5]

                    if top_ingredients:
                        ingredients, counts = zip(*top_ingredients)

                        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

                        short_names = [name[:12] + '...' if len(name) > 12 else name for name in ingredients]

                        bars = ax.bar(short_names, counts, color=self.config.PRIMARY_COLOR)

                        for bar in bars:
                            height = bar.get_height()
                            ax.annotate(f'{height}',
                                        xy=(bar.get_x() + bar.get_width() / 2, height),
                                        xytext=(0, 3),
                                        textcoords="offset points",
                                        ha='center', va='bottom',
                                        fontsize=8)

                        ax.set_ylabel('Recipes', fontsize=8)
                        ax.set_title('Ingredient Usage', fontsize=10)
                        ax.tick_params(axis='x', labelrotation=45, labelsize=8)
                        ax.tick_params(axis='y', labelsize=8)

                        plt.tight_layout()

                        # Create canvas for the matplotlib figure
                        chart_frame = tk.Frame(recipe_content, bg="white")
                        chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

                        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                        canvas.draw()
                        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                tk.Label(
                    recipe_list_frame,
                    text="No recipes found",
                    font=("Helvetica", 11),
                    bg="white"
                ).pack(anchor="w", pady=5)

        except Exception as e:
            tk.Label(
                recipe_content,
                text=f"Error loading recipe data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_order_summary(self):
        try:
            order_controller = OrderController()
            orders = order_controller.get_all_orders()

            order_card, order_content = self.cards["order"]

            for widget in order_content.winfo_children():
                widget.destroy()

            summary_frame = tk.Frame(order_content, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)

            total_orders = len(orders) if orders else 0

            status_counts = {"Pending": 0, "Received": 0, "Other": 0}
            for order_id, order_data in orders.items():
                status = order_data.get("order_status", "Other")
                if status in status_counts:
                    status_counts[status] += 1
                else:
                    status_counts["Other"] += 1

            tk.Label(
                summary_frame,
                text=f"Total Orders: {total_orders}",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Pending Orders: {status_counts['Pending']}",
                font=("Helvetica", 12),
                bg="white",
                fg="blue" if status_counts['Pending'] > 0 else "black"
            ).pack(anchor="w", pady=5)

            tk.Label(
                summary_frame,
                text=f"Received Orders: {status_counts['Received']}",
                font=("Helvetica", 12),
                bg="white"
            ).pack(anchor="w", pady=5)

            if total_orders > 0:
                separator = ttk.Separator(order_content, orient="horizontal")
                separator.pack(fill=tk.X, padx=15, pady=10)

                chart_label = tk.Label(
                    order_content,
                    text="Order Status",
                    font=("Helvetica", 12, "bold"),
                    bg="white"
                )
                chart_label.pack(anchor="w", padx=5, pady=5)

                # Create pie chart
                fig, ax = plt.subplots(figsize=(4, 3), dpi=100)

                # Data for pie chart
                status_values = [status_counts['Pending'], status_counts['Received'], status_counts['Other']]
                labels = ['Pending', 'Received', 'Other']
                colors = ['#2196F3', '#4CAF50', '#9E9E9E']

                filtered_data = [(count, label, color) for count, label, color in zip(status_values, labels, colors) if count > 0]

                if filtered_data:
                    counts, labels, colors = zip(*filtered_data)
                    ax.pie(
                        counts, 
                        labels=labels, 
                        colors=colors,
                        autopct='%1.1f%%', 
                        startangle=90,
                        textprops={'fontsize': 8}
                    )

                    ax.axis('equal')
                    plt.tight_layout()

                    # Create canvas for the matplotlib figure
                    chart_frame = tk.Frame(order_content, bg="white")
                    chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

                    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            separator2 = ttk.Separator(order_content, orient="horizontal")
            separator2.pack(fill=tk.X, padx=15, pady=10)

            # List recent orders
            recent_label = tk.Label(
                order_content,
                text="Recent Orders:",
                font=("Helvetica", 12, "bold"),
                bg="white"
            )
            recent_label.pack(anchor="w", padx=5, pady=5)

            if orders:
                order_list_frame = tk.Frame(order_content, bg="white")
                order_list_frame.pack(fill=tk.X, padx=10, pady=5)

                order_items = list(orders.items())

                for i, (order_id, order_data) in enumerate(order_items[:5]):
                    order_date = order_data.get("order_date", "N/A")
                    order_status = order_data.get("order_status", "Pending")

                    status_color = "green" if order_status == "Received" else "blue"

                    order_item = tk.Frame(
                        order_list_frame, 
                        bg="white", 
                        bd=1, 
                        relief=tk.GROOVE,
                        padx=8,
                        pady=8
                    )
                    order_item.pack(fill=tk.X, pady=5)

                    header_frame = tk.Frame(order_item, bg="white")
                    header_frame.pack(fill=tk.X)

                    tk.Label(
                        header_frame,
                        text=f"Order #{order_id}",
                        font=("Helvetica", 11, "bold"),
                        bg="white"
                    ).pack(side=tk.LEFT)

                    tk.Label(
                        header_frame,
                        text=f"({order_status})",
                        font=("Helvetica", 11),
                        bg="white",
                        fg=status_color
                    ).pack(side=tk.RIGHT)

                    tk.Label(
                        order_item,
                        text=f"Date: {order_date}",
                        font=("Helvetica", 10),
                        bg="white",
                        fg="grey"
                    ).pack(anchor="w")

                    order_content_data = order_data.get("order_content", {})
                    if order_content_data:
                        items_text = ", ".join(list(order_content_data.keys())[:2])
                        if len(order_content_data) > 2:
                            items_text += f" and {len(order_content_data) - 2} more"

                        tk.Label(
                            order_item,
                            text=f"Items: {items_text}",
                            font=("Helvetica", 10),
                            bg="white",
                            fg="grey"
                        ).pack(anchor="w")

                    if i >= 4:
                        break
            else:
                tk.Label(
                    order_content,
                    text="No orders found",
                    font=("Helvetica", 11),
                    bg="white"
                ).pack(anchor="w", padx=10, pady=5)

        except Exception as e:
            tk.Label(
                order_content,
                text=f"Error loading order data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_alerts(self):
        try:
            # Get inventory data for alerts
            inventory_data = FoodInventory().displayItems()

            alert_card, alert_content = self.cards["alert"]

            for widget in alert_content.winfo_children():
                widget.destroy()

            header_frame = tk.Frame(alert_content, bg="white")
            header_frame.pack(fill=tk.X, padx=5, pady=10)

            tk.Label(
                header_frame,
                text="System Alerts",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w")

            separator = ttk.Separator(alert_content, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)

            alerts_frame = tk.Frame(alert_content, bg="white")
            alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            has_alerts = False

            low_stock_items = []
            for item_dict in inventory_data:
                for item_id, item_details in item_dict.items():
                    if item_details.get("is_low", False):
                        low_stock_items.append({
                            "name": item_details.get("itemName", "Unknown Item"),
                            "quantity": item_details.get("totalQuantity", 0)
                        })

            if low_stock_items:
                has_alerts = True
                alert_frame = tk.Frame(
                    alerts_frame, 
                    bg=self.config.LIGHTY_COLOR, 
                    padx=10, 
                    pady=8,
                    bd=1,
                    relief=tk.RAISED
                )
                alert_frame.pack(fill=tk.X, pady=8)

                tk.Label(
                    alert_frame,
                    text="Low Stock Alert",
                    font=("Helvetica", 11, "bold"),
                    bg=self.config.LIGHTY_COLOR,
                    fg="white"
                ).pack(anchor="w")

                # Show low stock items
                for i, item in enumerate(low_stock_items[:5]):
                    tk.Label(
                        alert_frame,
                        text=f"• {item['name']} ({item['quantity']} left)",
                        font=("Helvetica", 10),
                        bg=self.config.LIGHTY_COLOR,
                        fg="white"
                    ).pack(anchor="w")

                if len(low_stock_items) > 5:
                    tk.Label(
                        alert_frame,
                        text=f"• and {len(low_stock_items) - 5} more items",
                        font=("Helvetica", 10),
                        bg=self.config.LIGHTY_COLOR,
                        fg="white"
                    ).pack(anchor="w")

                tk.Button(
                    alert_frame,
                    text="View Inventory",
                    command=lambda: self.master.master.master.show_inventory(),
                    **self.config.BUTTON_STYLES["secondary"]
                ).pack(anchor="e", pady=5)

            # If no alerts, show a message
            if not has_alerts:
                tk.Label(
                    alert_content,
                    text="No alerts at this time",
                    font=("Helvetica", 12),
                    bg="white",
                    fg="green"
                ).pack(anchor="w", pady=15)

                status_frame = tk.Frame(alert_content, bg="white")
                status_frame.pack(pady=15)

                canvas = tk.Canvas(status_frame, width=50, height=50, bg="white", highlightthickness=0)
                canvas.pack()

                canvas.create_oval(5, 5, 45, 45, fill="#4CAF50", outline="#4CAF50")

                canvas.create_line(15, 25, 25, 35, fill="white", width=3)
                canvas.create_line(25, 35, 35, 15, fill="white", width=3)

        except Exception as e:
            tk.Label(
                alert_content,
                text=f"Error loading alerts: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)

    def on_close(self):
        plt.close("all")
        self.master.quit()
        self.master.destroy()
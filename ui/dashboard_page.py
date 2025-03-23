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
    
    def create_ui(self):
        # Header
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
        
        # Last updated timestamp
        self.timestamp_label = tk.Label(
            header,
            text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Helvetica", 10),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        self.timestamp_label.pack(side=tk.RIGHT, padx=15)
        
        # Refresh button
        refresh_btn = tk.Button(
            header,
            text="Refresh",
            command=self.load_dashboard_data,
            **self.config.BUTTON_STYLES["secondary"]
        )
        refresh_btn.pack(side=tk.RIGHT, padx=10)
        
        # Main content area with summary cards
        content_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configure grid layout for cards with proper spacing
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)
        
        # Create summary cards
        self.inventory_card, self.inventory_canvas = self.create_summary_card(
            content_frame, "Inventory Summary", 0, 0
        )
        
        self.recipe_card, self.recipe_canvas = self.create_summary_card(
            content_frame, "Recipe Summary", 0, 1
        )
        
        self.order_card, self.order_canvas = self.create_summary_card(
            content_frame, "Recent Orders", 1, 0
        )
        
        self.alert_card, self.alert_canvas = self.create_summary_card(
            content_frame, "Alerts & Notifications", 1, 1
        )
    
    def create_summary_card(self, parent, title, row, column):
        # Create the card frame
        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief=tk.RAISED,
            highlightbackground=self.config.PRIMARY_COLOR,
            highlightthickness=2
        )
        card.grid(row=row, column=column, padx=12, pady=12, sticky="nsew")
        
        # Card header
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
        
        # Create canvas with scrollbar for content
        canvas_frame = tk.Frame(card, bg="white")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Canvas for scrollable content
        canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            highlightthickness=0
        )
        
        # Scrollbar for canvas
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        # Content frame inside canvas
        content_frame = tk.Frame(canvas, bg="white", padx=15, pady=15)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add content frame to canvas
        content_window = canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)
        
        # Configure canvas scrolling
        def configure_canvas(event):
            # Update the scrollregion to encompass the inner frame
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Update the width of the content window to fill the canvas
            canvas.itemconfig(content_window, width=event.width)
            
        canvas.bind("<Configure>", configure_canvas)
        content_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return content_frame, canvas
    
    def load_dashboard_data(self):
        # Update timestamp
        self.timestamp_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Clear existing content in cards
        for widget in self.inventory_card.winfo_children():
            widget.destroy()
        
        for widget in self.recipe_card.winfo_children():
            widget.destroy()
        
        for widget in self.order_card.winfo_children():
            widget.destroy()
        
        for widget in self.alert_card.winfo_children():
            widget.destroy()
        
        # Load inventory summary
        self.load_inventory_summary()
        
        # Load recipe summary
        self.load_recipe_summary()
        
        # Load order summary
        self.load_order_summary()
        
        # Load alerts
        self.load_alerts()
    
    def load_inventory_summary(self):
        try:
            inventory_data = FoodInventory().displayItems()
            
            # Count total items, low stock items, and near expiry items
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
            
            # Create summary section
            summary_frame = tk.Frame(self.inventory_card, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)
            
            # Create summary labels with better spacing
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
            
            # Add separator
            separator = ttk.Separator(self.inventory_card, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)
            
            # Add inventory status chart (pie chart)
            if total_items > 0:
                chart_label = tk.Label(
                    self.inventory_card,
                    text="Inventory Status",
                    font=("Helvetica", 12, "bold"),
                    bg="white"
                )
                chart_label.pack(anchor="w", padx=5, pady=5)
                
                # Create pie chart
                fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
                
                # Data for pie chart
                status_counts = [
                    normal_count,
                    low_stock_count - (low_stock_count if near_expiry_count > 0 else 0), 
                    near_expiry_count - (near_expiry_count if low_stock_count > 0 else 0),
                    min(low_stock_count, near_expiry_count) if low_stock_count > 0 and near_expiry_count > 0 else 0
                ]
                
                labels = ['Normal', 'Low Stock', 'Near Expiry', 'Low & Near Expiry']
                colors = ['#4CAF50', '#FFC107', '#FF9800', '#F44336']
                
                # Only include non-zero values
                filtered_data = [(count, label, color) for count, label, color in zip(status_counts, labels, colors) if count > 0]
                
                if filtered_data:
                    counts, labels, colors = zip(*filtered_data)
                    wedges, texts, autotexts = ax.pie(
                        counts, 
                        labels=labels, 
                        colors=colors,
                        autopct='%1.1f%%', 
                        startangle=90,
                        textprops={'fontsize': 8}
                    )
                    
                    # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.axis('equal')
                    plt.tight_layout()
                    
                    # Create canvas for the matplotlib figure
                    chart_frame = tk.Frame(self.inventory_card, bg="white")
                    chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                    
                    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            tk.Label(
                self.inventory_card,
                text=f"Error loading inventory data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_recipe_summary(self):
        try:
            recipes = StaffController().viewAllRecipes()
            
            # Count total recipes
            total_recipes = len(recipes)
            
            # Create summary labels
            summary_frame = tk.Frame(self.recipe_card, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)
            
            tk.Label(
                summary_frame,
                text=f"Total Recipes: {total_recipes}",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w", pady=5)
            
            # Add separator
            separator = ttk.Separator(self.recipe_card, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)
            
            # List most recent recipes
            recent_label = tk.Label(
                self.recipe_card,
                text="Recent Recipes:",
                font=("Helvetica", 12, "bold"),
                bg="white"
            )
            recent_label.pack(anchor="w", padx=5, pady=5)
            
            recipe_list_frame = tk.Frame(self.recipe_card, bg="white")
            recipe_list_frame.pack(fill=tk.X, padx=10, pady=5)
            
            if recipes:
                # Track ingredient counts for chart
                ingredient_counts = {}
                
                for i, recipe_entry in enumerate(recipes[:8]):  # Show up to 8 recipes
                    for recipe_id, recipe_data in recipe_entry.items():
                        recipe_name = recipe_data.get("recipeName", "Unknown Recipe")
                        ingredients = recipe_data.get("ingredients", {})
                        
                        # Update ingredient counts for chart
                        for ingredient in ingredients:
                            if ingredient in ingredient_counts:
                                ingredient_counts[ingredient] += 1
                            else:
                                ingredient_counts[ingredient] = 1
                        
                        # Create recipe item frame with border
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
                        
                        # Show ingredients
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
                
                # Add ingredient usage chart if we have data
                if ingredient_counts:
                    # Add separator
                    separator2 = ttk.Separator(self.recipe_card, orient="horizontal")
                    separator2.pack(fill=tk.X, padx=15, pady=10)
                    
                    chart_label = tk.Label(
                        self.recipe_card,
                        text="Most Used Ingredients",
                        font=("Helvetica", 12, "bold"),
                        bg="white"
                    )
                    chart_label.pack(anchor="w", padx=5, pady=5)
                    
                    # Sort ingredients by usage and take top 5
                    top_ingredients = sorted(ingredient_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    if top_ingredients:
                        ingredients, counts = zip(*top_ingredients)
                        
                        # Create bar chart
                        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
                        
                        # Shorten long ingredient names
                        short_names = [name[:12] + '...' if len(name) > 12 else name for name in ingredients]
                        
                        bars = ax.bar(short_names, counts, color=self.config.PRIMARY_COLOR)
                        
                        # Add count values on top of bars
                        for bar in bars:
                            height = bar.get_height()
                            ax.annotate(f'{height}',
                                        xy=(bar.get_x() + bar.get_width() / 2, height),
                                        xytext=(0, 3),  # 3 points vertical offset
                                        textcoords="offset points",
                                        ha='center', va='bottom',
                                        fontsize=8)
                        
                        ax.set_ylabel('Recipes', fontsize=8)
                        ax.set_title('Ingredient Usage', fontsize=10)
                        ax.tick_params(axis='x', labelrotation=45, labelsize=8)
                        ax.tick_params(axis='y', labelsize=8)
                        
                        plt.tight_layout()
                        
                        # Create canvas for the matplotlib figure
                        chart_frame = tk.Frame(self.recipe_card, bg="white")
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
                self.recipe_card,
                text=f"Error loading recipe data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_order_summary(self):
        try:
            order_controller = OrderController()
            orders = order_controller.get_all_orders()
            
            # Summary frame
            summary_frame = tk.Frame(self.order_card, bg="white")
            summary_frame.pack(fill=tk.X, padx=5, pady=10)
            
            # Count total orders and pending orders
            total_orders = len(orders) if orders else 0
            
            # Count orders by status
            status_counts = {"Pending": 0, "Received": 0, "Other": 0}
            for order_id, order_data in orders.items():
                status = order_data.get("order_status", "Other")
                if status in status_counts:
                    status_counts[status] += 1
                else:
                    status_counts["Other"] += 1
            
            # Create summary labels
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
            
            # Add order status chart if we have orders
            if total_orders > 0:
                # Add separator
                separator = ttk.Separator(self.order_card, orient="horizontal")
                separator.pack(fill=tk.X, padx=15, pady=10)
                
                chart_label = tk.Label(
                    self.order_card,
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
                
                # Only include non-zero values
                filtered_data = [(count, label, color) for count, label, color in zip(status_values, labels, colors) if count > 0]
                
                if filtered_data:
                    counts, labels, colors = zip(*filtered_data)
                    wedges, texts, autotexts = ax.pie(
                        counts, 
                        labels=labels, 
                        colors=colors,
                        autopct='%1.1f%%', 
                        startangle=90,
                        textprops={'fontsize': 8}
                    )
                    
                    # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.axis('equal')
                    plt.tight_layout()
                    
                    # Create canvas for the matplotlib figure
                    chart_frame = tk.Frame(self.order_card, bg="white")
                    chart_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                    
                    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add separator
            separator2 = ttk.Separator(self.order_card, orient="horizontal")
            separator2.pack(fill=tk.X, padx=15, pady=10)
            
            # List recent orders
            recent_label = tk.Label(
                self.order_card,
                text="Recent Orders:",
                font=("Helvetica", 12, "bold"),
                bg="white"
            )
            recent_label.pack(anchor="w", padx=5, pady=5)
            
            if orders:
                order_list_frame = tk.Frame(self.order_card, bg="white")
                order_list_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Convert to list for easier slicing
                order_items = list(orders.items())
                
                for i, (order_id, order_data) in enumerate(order_items[:5]):
                    order_date = order_data.get("order_date", "N/A")
                    order_status = order_data.get("order_status", "Pending")
                    
                    status_color = "green" if order_status == "Received" else "blue"
                    
                    # Create order item frame with border
                    order_item = tk.Frame(
                        order_list_frame, 
                        bg="white", 
                        bd=1, 
                        relief=tk.GROOVE,
                        padx=8,
                        pady=8
                    )
                    order_item.pack(fill=tk.X, pady=5)
                    
                    # Header frame for order ID and status
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
                    
                    # Date
                    tk.Label(
                        order_item,
                        text=f"Date: {order_date}",
                        font=("Helvetica", 10),
                        bg="white",
                        fg="grey"
                    ).pack(anchor="w")
                    
                    # Order content
                    order_content = order_data.get("order_content", {})
                    if order_content:
                        items_text = ", ".join(list(order_content.keys())[:2])
                        if len(order_content) > 2:
                            items_text += f" and {len(order_content) - 2} more"
                        
                        tk.Label(
                            order_item,
                            text=f"Items: {items_text}",
                            font=("Helvetica", 10),
                            bg="white",
                            fg="grey"
                        ).pack(anchor="w")
                    
                    if i >= 4:  # Only show up to 5 orders
                        break
            else:
                tk.Label(
                    self.order_card,
                    text="No orders found",
                    font=("Helvetica", 11),
                    bg="white"
                ).pack(anchor="w", padx=10, pady=5)
            
            
        except Exception as e:
            tk.Label(
                self.order_card,
                text=f"Error loading order data: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)
    
    def load_alerts(self):
        try:
            # Get inventory data for alerts
            inventory_data = FoodInventory().displayItems()
            
            # Create alerts header
            header_frame = tk.Frame(self.alert_card, bg="white")
            header_frame.pack(fill=tk.X, padx=5, pady=10)
            
            tk.Label(
                header_frame,
                text="System Alerts",
                font=("Helvetica", 12, "bold"),
                bg="white"
            ).pack(anchor="w")
            
            # Add separator
            separator = ttk.Separator(self.alert_card, orient="horizontal")
            separator.pack(fill=tk.X, padx=15, pady=10)
            
            alerts_frame = tk.Frame(self.alert_card, bg="white")
            alerts_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            # Track if we have any alerts
            has_alerts = False
            
            # Check for low stock items
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
                
                # Show low stock items in a nicely formatted way
                for i, item in enumerate(low_stock_items[:5]):  # Limit to 5 items
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
            
            # Check for near expiry items
            near_expiry_items = []
            for item_dict in inventory_data:
                for item_id, item_details in item_dict.items():
                    if item_details.get("near_expiry", False):
                        stock = item_details.get("stock", {})
                        # Get the earliest expiry date
                        expiry_date = min(stock.keys()) if stock else "Unknown"
                        near_expiry_items.append({
                            "name": item_details.get("itemName", "Unknown Item"),
                            "expiry": expiry_date
                        })
            
            if near_expiry_items:
                has_alerts = True
                alert_frame = tk.Frame(
                    alerts_frame, 
                    bg=self.config.ORANGE_COLOR, 
                    padx=10, 
                    pady=8,
                    bd=1,
                    relief=tk.RAISED
                )
                alert_frame.pack(fill=tk.X, pady=8)
                
                tk.Label(
                    alert_frame,
                    text="Expiry Alert",
                    font=("Helvetica", 11, "bold"),
                    bg=self.config.ORANGE_COLOR,
                    fg="black"
                ).pack(anchor="w")
                
                # Show near expiry items in a nicely formatted way
                for i, item in enumerate(near_expiry_items[:5]):  # Limit to 5 items
                    tk.Label(
                        alert_frame,
                        text=f"• {item['name']} (Expires: {item['expiry']})",
                        font=("Helvetica", 10),
                        bg=self.config.ORANGE_COLOR,
                        fg="black"
                    ).pack(anchor="w")
                
                if len(near_expiry_items) > 5:
                    tk.Label(
                        alert_frame,
                        text=f"• and {len(near_expiry_items) - 5} more items",
                        font=("Helvetica", 10),
                        bg=self.config.ORANGE_COLOR,
                        fg="black"
                    ).pack(anchor="w")
                
                tk.Button(
                    alert_frame,
                    text="View Inventory",
                    command=lambda: self.master.master.master.show_inventory(),
                    **self.config.BUTTON_STYLES["secondary"]
                ).pack(anchor="e", pady=5)
            
            # Check for pending orders
            order_controller = OrderController()
            orders = order_controller.get_all_orders()
            
            pending_orders = []
            for order_id, order_data in orders.items():
                if order_data.get("order_status") == "Pending":
                    pending_orders.append({
                        "id": order_id,
                        "date": order_data.get("order_date", "N/A")
                    })
            
            if pending_orders:
                has_alerts = True
                alert_frame = tk.Frame(
                    alerts_frame, 
                    bg="lightblue", 
                    padx=10, 
                    pady=8,
                    bd=1,
                    relief=tk.RAISED
                )
                alert_frame.pack(fill=tk.X, pady=8)
                
                tk.Label(
                    alert_frame,
                    text="Pending Orders",
                    font=("Helvetica", 11, "bold"),
                    bg="lightblue",
                    fg="black"
                ).pack(anchor="w")
                
                # Show pending orders in a nicely formatted way
                for i, order in enumerate(pending_orders[:5]):  # Limit to 5 orders
                    tk.Label(
                        alert_frame,
                        text=f"• Order #{order['id']} ({order['date']})",
                        font=("Helvetica", 10),
                        bg="lightblue",
                        fg="black"
                    ).pack(anchor="w")
                
                if len(pending_orders) > 5:
                    tk.Label(
                        alert_frame,
                        text=f"• and {len(pending_orders) - 5} more orders",
                        font=("Helvetica", 10),
                        bg="lightblue",
                        fg="black"
                    ).pack(anchor="w")
                
                tk.Button(
                    alert_frame,
                    text="View Orders",
                    command=lambda: self.master.master.master.show_orders(),
                    **self.config.BUTTON_STYLES["secondary"]
                ).pack(anchor="e", pady=5)
            
            # If no alerts, show a message
            if not has_alerts:
                tk.Label(
                    self.alert_card,
                    text="No alerts at this time",
                    font=("Helvetica", 12),
                    bg="white",
                    fg="green"
                ).pack(anchor="w", pady=15)
                
                # Add a good status image or icon
                status_frame = tk.Frame(self.alert_card, bg="white")
                status_frame.pack(pady=15)
                
                # Create a simple "check mark" using a canvas
                canvas = tk.Canvas(status_frame, width=50, height=50, bg="white", highlightthickness=0)
                canvas.pack()
                
                # Draw a green circle
                canvas.create_oval(5, 5, 45, 45, fill="#4CAF50", outline="#4CAF50")
                
                # Draw a white checkmark
                canvas.create_line(15, 25, 25, 35, fill="white", width=3)
                canvas.create_line(25, 35, 35, 15, fill="white", width=3)
            
        except Exception as e:
            tk.Label(
                self.alert_card,
                text=f"Error loading alerts: {str(e)}",
                font=("Helvetica", 12),
                bg="white",
                fg="red"
            ).pack(anchor="w", pady=5)


"""
Analytics dashboard UI for StockOverflow
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsPage(tk.Frame):
    """Analytics dashboard page"""
    
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
        """Create the analytics page UI"""
        # Create header
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(
            header, 
            text="Analytics Dashboard",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            header, 
            text="Refresh Data",
            command=self.refresh_analytics,
            **self.config.BUTTON_STYLES["primary"]
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create dashboard layout
        dashboard_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create top row with summary cards
        top_row = tk.Frame(dashboard_frame, bg=self.config.BG_COLOR)
        top_row.pack(fill=tk.X, pady=5)
        
        # Create summary cards
        self.create_summary_cards(top_row)
        
        # Create bottom row with charts
        bottom_row = tk.Frame(dashboard_frame, bg=self.config.BG_COLOR)
        bottom_row.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create charts
        self.create_charts(bottom_row)
    
    def create_summary_cards(self, parent):
        """Create summary cards for the dashboard"""
        # Get data
        inventory = self.db.get_inventory()
        recipes = self.db.get_recipes()
        orders = self.db.get_orders()
        
        # Calculate metrics
        total_inventory_items = len(inventory)
        low_stock_items = sum(1 for item in inventory if item["quantity"] < 10)
        expiring_soon_items = 0
        for item in inventory:
            try:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d")
                if (expiry_date - datetime.now()).days < 7:
                    expiring_soon_items += 1
            except:
                pass
        
        total_recipes = len(recipes)
        total_orders = len(orders)
        completed_orders = sum(1 for order in orders if order["status"] == "Completed")
        
        # Create card frame
        card_frame = tk.Frame(parent, bg=self.config.BG_COLOR)
        card_frame.pack(fill=tk.X, pady=5)
        
        # Inventory card
        inventory_card = tk.Frame(card_frame, bg="white", bd=1, relief=tk.RAISED)
        inventory_card.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        tk.Label(inventory_card, text="Inventory", font=self.header_font, bg="white").pack(anchor=tk.W, padx=10, pady=5)
        tk.Label(inventory_card, text=f"Total Items: {total_inventory_items}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(inventory_card, text=f"Low Stock: {low_stock_items}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(inventory_card, text=f"Expiring Soon: {expiring_soon_items}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        
        # Recipes card
        recipes_card = tk.Frame(card_frame, bg="white", bd=1, relief=tk.RAISED)
        recipes_card.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        tk.Label(recipes_card, text="Recipes", font=self.header_font, bg="white").pack(anchor=tk.W, padx=10, pady=5)
        tk.Label(recipes_card, text=f"Total Recipes: {total_recipes}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        
        # Orders card
        orders_card = tk.Frame(card_frame, bg="white", bd=1, relief=tk.RAISED)
        orders_card.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        
        tk.Label(orders_card, text="Orders", font=self.header_font, bg="white").pack(anchor=tk.W, padx=10, pady=5)
        tk.Label(orders_card, text=f"Total Orders: {total_orders}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(orders_card, text=f"Completed Orders: {completed_orders}", bg="white").pack(anchor=tk.W, padx=10, pady=2)
        tk.Label(orders_card, text=f"Completion Rate: {completed_orders/total_orders*100:.1f}%" if total_orders > 0 else "Completion Rate: N/A", bg="white").pack(anchor=tk.W, padx=10, pady=2)
    
    def create_charts(self, parent):
        """Create charts for the dashboard"""
        # Create charts frame
        charts_frame = tk.Frame(parent, bg=self.config.BG_COLOR)
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create left chart (Inventory by Category)
        left_chart_frame = tk.Frame(charts_frame, bg="white", bd=1, relief=tk.RAISED)
        left_chart_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        tk.Label(left_chart_frame, text="Inventory by Category", font=self.header_font, bg="white").pack(anchor=tk.W, padx=10, pady=5)
        
        # Get inventory data
        inventory = self.db.get_inventory()
        
        # Group by category
        categories = {}
        for item in inventory:
            category = item["category"]
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        # Create figure
        fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        
        # Create pie chart
        wedges, texts, autotexts = ax1.pie(
            categories.values(), 
            labels=categories.keys(), 
            autopct='%1.1f%%',
            startangle=90
        )
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax1.axis('equal')
        
        # Create canvas
        canvas1 = FigureCanvasTkAgg(fig1, left_chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Create right chart (Expiring Items)
        right_chart_frame = tk.Frame(charts_frame, bg="white", bd=1, relief=tk.RAISED)
        right_chart_frame.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        tk.Label(right_chart_frame, text="Items Expiring Soon", font=self.header_font, bg="white").pack(anchor=tk.W, padx=10, pady=5)
        
        # Get expiring items
        expiring_items = []
        for item in inventory:
            try:
                expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d")
                days_until_expiry = (expiry_date - datetime.now()).days
                if days_until_expiry < 14:  # Show items expiring in the next 2 weeks
                    expiring_items.append((item["name"], days_until_expiry))
            except:
                pass
        
        # Sort by days until expiry
        expiring_items.sort(key=lambda x: x[1])
        
        # Take top 10
        expiring_items = expiring_items[:10]
        
        # Create figure
        fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        ax2 = fig2.add_subplot(111)
        
        # Create horizontal bar chart
        if expiring_items:
            names = [item[0] for item in expiring_items]
            days = [item[1] for item in expiring_items]
            
            # Create colors based on days (red for expired, yellow for soon)
            colors = ['#FF9999' if d <= 0 else '#FFCC99' if d <= 3 else '#FFFF99' for d in days]
            
            ax2.barh(names, days, color=colors)
            ax2.set_xlabel('Days until expiry')
            ax2.set_title('Items Expiring Soon')
            
            # Add value labels
            for i, v in enumerate(days):
                ax2.text(v + 0.1, i, str(v), va='center')
        else:
            ax2.text(0.5, 0.5, 'No items expiring soon', ha='center', va='center')
        
        # Create canvas
        canvas2 = FigureCanvasTkAgg(fig2, right_chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def refresh_analytics(self):
        """Refresh the analytics dashboard"""
        # Clear the frame
        for widget in self.winfo_children():
            widget.destroy()
        
        # Recreate the UI
        self.create_ui()
    
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
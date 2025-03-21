"""
Recipe management UI for StockOverflow
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RecipePage(tk.Frame):
    """Recipe management page"""
    
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
        """Create the recipe page UI"""
        # Create header
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(
            header, 
            text="Recipe Management",
            font=self.title_font,
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Add recipe button (only for Admin)
        if self.current_user["role"] == "Admin":
            add_btn = tk.Button(
                header, 
                text="Add Recipe",
                command=self.add_recipe,
                **self.config.BUTTON_STYLES["primary"]
            )
            add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create recipes table
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a treeview for the recipes
        columns = ("ID", "Name", "Category", "Cost", "Actions")
        self.recipes_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configure columns
        self.recipes_tree.heading("ID", text="ID")
        self.recipes_tree.heading("Name", text="Name")
        self.recipes_tree.heading("Category", text="Category")
        self.recipes_tree.heading("Cost", text="Cost")
        self.recipes_tree.heading("Actions", text="Actions")
        
        # Configure column widths
        self.recipes_tree.column("ID", width=50)
        self.recipes_tree.column("Name", width=200)
        self.recipes_tree.column("Category", width=150)
        self.recipes_tree.column("Cost", width=100)
        self.recipes_tree.column("Actions", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.recipes_tree.yview)
        self.recipes_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipes_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click event
        self.recipes_tree.bind("<Double-1>", self.on_recipe_select)
        
        # Load recipe data
        self.load_recipe_data()
    
    def load_recipe_data(self):
        """Load recipe data into the treeview"""
        # Clear existing items
        for i in self.recipes_tree.get_children():
            self.recipes_tree.delete(i)
        
        # Get recipe data
        recipes = self.db.get_recipes()
        
        # Add items to treeview
        for recipe in recipes:
            recipe_values = (
                recipe["id"],
                recipe["name"],
                recipe["category"],
                f"${recipe['cost']:.2f}",
                "View/Edit"
            )
            
            # Add recipe to treeview
            self.recipes_tree.insert("", tk.END, values=recipe_values)
    
    def on_recipe_select(self, event):
        """Handle recipe selection (double-click)"""
        # Get the selected item
        selection = self.recipes_tree.selection()
        if not selection:
            return
        
        # Get the item values
        item_values = self.recipes_tree.item(selection[0], "values")
        recipe_id = int(item_values[0])
        
        # Show recipe details in a dialog
        self.show_recipe_details(recipe_id)
    
    def show_recipe_details(self, recipe_id):
        """Show recipe details in a dialog"""
        # Get recipe data
        recipes = self.db.get_recipes()
        inventory = self.db.get_inventory()
        
        # Find the recipe
        recipe = next((r for r in recipes if r["id"] == recipe_id), None)
        if not recipe:
            messagebox.showerror("Error", f"Recipe with ID {recipe_id} not found")
            return
        
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title(f"Recipe Details: {recipe['name']}")
        dialog.geometry("500x400")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 500, 400)
        
        # Add recipe details
        details_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Recipe name
        tk.Label(details_frame, text="Name:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=recipe["name"])
        name_entry = tk.Entry(details_frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Recipe category
        tk.Label(details_frame, text="Category:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar(value=recipe["category"])
        category_entry = tk.Entry(details_frame, textvariable=category_var, width=20)
        category_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Recipe cost
        tk.Label(details_frame, text="Cost:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=2, column=0, sticky=tk.W, pady=5)
        cost_var = tk.StringVar(value=str(recipe["cost"]))
        cost_entry = tk.Entry(details_frame, textvariable=cost_var, width=10)
        cost_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Ingredients label
        tk.Label(details_frame, text="Ingredients:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        # Ingredients list
        ingredients_frame = tk.Frame(details_frame, bg=self.config.BG_COLOR)
        ingredients_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        # Create a treeview for the ingredients
        columns = ("Item", "Quantity", "Unit")
        ingredients_tree = ttk.Treeview(ingredients_frame, columns=columns, show="headings", height=5)
        
        # Configure columns
        ingredients_tree.heading("Item", text="Item")
        ingredients_tree.heading("Quantity", text="Quantity")
        ingredients_tree.heading("Unit", text="Unit")
        
        # Configure column widths
        ingredients_tree.column("Item", width=200)
        ingredients_tree.column("Quantity", width=100)
        ingredients_tree.column("Unit", width=70)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(ingredients_frame, orient=tk.VERTICAL, command=ingredients_tree.yview)
        ingredients_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        ingredients_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add ingredients to treeview
        for ingredient in recipe["ingredients"]:
            item = next((i for i in inventory if i["id"] == ingredient["item_id"]), None)
            if item:
                ingredient_values = (
                    item["name"],
                    ingredient["quantity"],
                    ingredient["unit"]
                )
                ingredients_tree.insert("", tk.END, values=ingredient_values)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Save button (only for Admin)
        if self.current_user["role"] == "Admin":
            save_btn = tk.Button(
                button_frame, 
                text="Save Changes",
                command=lambda: self.save_recipe_changes(
                    recipe_id, 
                    name_var.get(), 
                    category_var.get(), 
                    float(cost_var.get()),
                    dialog
                ),
                **self.config.BUTTON_STYLES["primary"]
            )
            save_btn.pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame, 
            text="Close",
            command=dialog.destroy,
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Disable fields for Staff users
        if self.current_user["role"] != "Admin":
            name_entry.configure(state="disabled")
            category_entry.configure(state="disabled")
            cost_entry.configure(state="disabled")
    
    def save_recipe_changes(self, recipe_id, name, category, cost, dialog):
        """Save recipe changes"""
        # Create updates dict
        updates = {
            "name": name,
            "category": category,
            "cost": cost
        }
        
        # Update the recipe
        success = self.db.update_recipe(recipe_id, updates)
        
        if success:
            messagebox.showinfo("Success", f"Recipe {name} updated successfully")
            dialog.destroy()
            # Refresh recipe data
            self.load_recipe_data()
        else:
            messagebox.showerror("Error", "Failed to update recipe")
    
    def add_recipe(self):
        """Add a new recipe"""
        # Create a dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add New Recipe")
        dialog.geometry("500x400")
        dialog.configure(bg=self.config.BG_COLOR)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog on the screen
        self.center_window(dialog, 500, 400)
        
        # Add recipe details form
        details_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Recipe name
        tk.Label(details_frame, text="Name:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=name_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Recipe category
        tk.Label(details_frame, text="Category:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        categories = ["Soups", "Main Course", "Appetizers", "Desserts", "Beverages", "Other"]
        tk.OptionMenu(details_frame, category_var, *categories).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Recipe cost
        tk.Label(details_frame, text="Cost:", font=self.header_font, bg=self.config.BG_COLOR).grid(row=2, column=0, sticky=tk.W, pady=5)
        cost_var = tk.StringVar()
        tk.Entry(details_frame, textvariable=cost_var, width=10).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Add button
        add_btn = tk.Button(
            button_frame, 
            text="Add Recipe",
            command=lambda: messagebox.showinfo("Not Implemented", "Add recipe functionality not fully implemented in this demo"),
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
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.staff_controller import StaffController

class RecipePage(tk.Frame):
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)

        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font
        
        self.selected_recipe_id = None  # Store selected recipe ID
        
        self.create_ui()

    def create_ui(self):
        # Header
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(header, text="Recipe Management", font=self.title_font, bg=self.config.BG_COLOR, fg=self.config.TEXT_COLOR)
        title_label.pack(side=tk.LEFT, padx=5)

        if self.current_user["role"] == "Admin":
            add_btn = tk.Button(header, text="Add Recipe", command=self.add_recipe, **self.config.BUTTON_STYLES["primary"])
            add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Table Frame
        table_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Recipe Name", "Ingredients")
        self.recipes_tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.recipes_tree.heading("Recipe Name", text="Recipe Name")
        self.recipes_tree.heading("Ingredients", text="Ingredients")

        self.recipes_tree.column("Recipe Name", width=200, anchor="center")
        self.recipes_tree.column("Ingredients", width=300, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.recipes_tree.yview)
        self.recipes_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipes_tree.pack(fill=tk.BOTH, expand=True)

        # Bind row selection event
        self.recipes_tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        # Action Buttons
        self.action_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        self.action_frame.pack(fill=tk.X, pady=5)

        self.make_button = tk.Button(self.action_frame, text="Make Recipe", command=self.make_recipe, state=tk.DISABLED, **self.config.BUTTON_STYLES["primary"])
        self.make_button.pack(pady=5)

        self.load_recipe_data()

    def load_recipe_data(self):
        self.recipes_tree.delete(*self.recipes_tree.get_children())  # Clear existing items

        recipes = StaffController().viewAllRecipes()
        for recipe_entry in recipes:
            for recipe_id, recipe_data in recipe_entry.items():
                recipe_name = recipe_data.get("recipeName", "Unknown Recipe")
                ingredients = recipe_data.get("ingredients", {})
                ingredients_str = ", ".join([f"{item} ({qty})" for item, qty in ingredients.items()])

                self.recipes_tree.insert("", tk.END, values=(recipe_name, ingredients_str), tags=(recipe_id,))

    def on_row_selected(self, event):
        selected = self.recipes_tree.selection()
        if selected:
            self.selected_recipe_id = self.recipes_tree.item(selected, "tags")[0]
            self.make_button.config(state=tk.NORMAL)
        else:
            self.selected_recipe_id = None
            self.make_button.config(state=tk.DISABLED)

    def make_recipe(self):
        if not self.selected_recipe_id:
            return

        success = StaffController().orderRecipe(self.selected_recipe_id)

        if success:
            messagebox.showinfo("Success", "Recipe made successfully, inventory updated!")
        else:
            messagebox.showerror("Error", "Not enough ingredients in inventory!")

    def add_recipe(self):
        def add_ingredient():
            selected_item = ingredient_var.get()
            quantity = quantity_var.get()
            if selected_item and quantity.isdigit():
                ingredients_list.insert(tk.END, f"{selected_item} ({quantity})")
                recipe_ingredients[selected_item] = int(quantity)
            else:
                messagebox.showerror("Error", "Please select an ingredient and enter a valid quantity.")

        def save_recipe():
            recipe_name = recipe_name_var.get().strip()
            if not recipe_name or not recipe_ingredients:
                messagebox.showerror("Error", "Recipe name and ingredients are required.")
                return
            
            new_recipe = {"recipeName": recipe_name, "ingredients": recipe_ingredients}
            StaffController().addRecipe(new_recipe)
            messagebox.showinfo("Success", "Recipe added successfully.")
            dialog.destroy()
            self.load_recipe_data()

        dialog = tk.Toplevel(self)
        dialog.title("Add Recipe")
        self.center_window(dialog, 400, 400)

        tk.Label(dialog, text="Recipe Name:").pack(pady=5)
        recipe_name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=recipe_name_var).pack(pady=5)

        tk.Label(dialog, text="Select Ingredient:").pack(pady=5)
        inventory_items = [item["itemName"] for item in StaffController().inventory_ref.get().values()]
        ingredient_var = tk.StringVar()
        ingredient_dropdown = ttk.Combobox(dialog, textvariable=ingredient_var, values=inventory_items)
        ingredient_dropdown.pack(pady=5)
        
        tk.Label(dialog, text="Quantity:").pack(pady=5)
        quantity_var = tk.StringVar()
        tk.Entry(dialog, textvariable=quantity_var).pack(pady=5)
        
        tk.Button(dialog, text="Add Ingredient", command=add_ingredient).pack(pady=5)
        
        ingredients_list = tk.Listbox(dialog, height=5)
        ingredients_list.pack(pady=5, fill=tk.BOTH, expand=True)
        
        recipe_ingredients = {}
        tk.Button(dialog, text="Save Recipe", command=save_recipe).pack(pady=10)


    def center_window(self, window, width, height):
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set the position
        window.geometry(f"{width}x{height}+{x}+{y}")
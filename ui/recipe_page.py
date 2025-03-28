import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.staff_controller import StaffController
from models.recipe import Recipe
from models.ingredient import Ingredient

class RecipePage(tk.Frame):
    def __init__(self, parent, db, config, current_user, title_font, header_font, normal_font):
        super().__init__(parent, bg=config.BG_COLOR)

        self.db = db
        self.config = config
        self.current_user = current_user
        self.title_font = title_font
        self.header_font = header_font
        self.normal_font = normal_font
        
        self.selected_recipe_id = None
        
        self.create_ui()

    def create_ui(self):
        header = tk.Frame(self, bg=self.config.BG_COLOR)
        header.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(header, text="Recipe Management", font=self.title_font, bg=self.config.BG_COLOR, fg=self.config.TEXT_COLOR)
        title_label.pack(side=tk.LEFT, padx=5)

        if self.current_user["role"] == "Admin":
            add_btn = tk.Button(header, text="Add Recipe", command=self.add_recipe, **self.config.BUTTON_STYLES["primary"])
            add_btn.pack(side=tk.RIGHT, padx=5)
            self.delete_btn = tk.Button(header, text="Delete Recipe", 
                                        command=self.delete_recipe, state=tk.DISABLED, 
                                        **self.config.BUTTON_STYLES["secondary"]
                                        )
            self.delete_btn.pack(side=tk.RIGHT, padx=5)
        
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

        self.recipes_tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        self.action_frame = tk.Frame(self, bg=self.config.BG_COLOR)
        self.action_frame.pack(fill=tk.X, pady=5)

        self.make_button = tk.Button(
                            self.action_frame, text="Make Recipe", 
                            command=self.make_recipe, state=tk.DISABLED, 
                            **self.config.BUTTON_STYLES["primary"])
        self.make_button.pack(pady=5)

        self.load_recipe_data()

    def load_recipe_data(self):
        self.recipes_tree.delete(*self.recipes_tree.get_children())

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
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state=tk.NORMAL)
        else:
            self.selected_recipe_id = None
            self.make_button.config(state=tk.DISABLED)
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state=tk.DISABLED)

    def make_recipe(self):
        if not self.selected_recipe_id:
            return

        success = StaffController().orderRecipe(self.selected_recipe_id)

        if success:
            messagebox.showinfo("Success", "Recipe made successfully, inventory updated!")
        else:
            messagebox.showerror("Error", "Not enough ingredients in inventory!")

    def add_recipe(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Recipe")
        dialog.geometry("400x600")
        dialog.configure(bg=self.config.BG_COLOR)
        self.center_window(dialog, 400, 600)

        header_frame = tk.Frame(dialog, bg=self.config.PRIMARY_COLOR, height=40)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame, 
            text="Add New Recipe", 
            font=("Helvetica", 16, "bold"),
            bg=self.config.PRIMARY_COLOR,
            fg="white"
        )
        header_label.pack(pady=8)

        content_frame = tk.Frame(dialog, bg=self.config.BG_COLOR, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            content_frame, 
            text="Recipe Name:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))

        recipe_name_entry = tk.Entry(content_frame, font=("Helvetica", 12), width=30)
        recipe_name_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Select Ingredient:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))

        inventory_items = [item["itemName"] for item in StaffController().inventory_ref.get().values()]
        ingredient_var = tk.StringVar()
        ingredient_dropdown = ttk.Combobox(content_frame, textvariable=ingredient_var, values=inventory_items)
        ingredient_dropdown.pack(anchor="w", pady=(0, 10), fill=tk.X)

        tk.Label(
            content_frame, 
            text="Quantity:",
            font=("Helvetica", 12, "bold"),
            bg=self.config.BG_COLOR,
            fg=self.config.TEXT_COLOR
        ).pack(anchor="w", pady=(10, 2))
        
        quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(content_frame, textvariable=quantity_var, font=("Helvetica", 12), width=30)
        quantity_entry.pack(anchor="w", pady=(0, 10), fill=tk.X)

        ingredients_list = tk.Listbox(content_frame, height=5)
        ingredients_list.pack(pady=(10, 5), fill=tk.BOTH, expand=True)

        recipe_ingredients_obj = Ingredient()
        recipe_ingredients = {}

        def add_ingredient():
            selected_item = ingredient_var.get()
            quantity = quantity_var.get()
            if selected_item and quantity.isdigit():
                ingredients_list.insert(tk.END, f"{selected_item} ({quantity})")
                recipe_ingredients.update(recipe_ingredients_obj.add_ingredient(selected_item, quantity))
            else:
                messagebox.showerror("Error", "Please select an ingredient and enter a valid quantity.")

        def save_recipe():
            recipe_name = recipe_name_entry.get().strip()
            if not recipe_name or not recipe_ingredients:
                messagebox.showerror("Error", "Recipe name and ingredients are required.")
                return
            
            new_recipe = Recipe(recipe_name, recipe_ingredients)
            new_recipe_dict = new_recipe.to_dict()
            print(new_recipe_dict)
            StaffController().addRecipe(new_recipe_dict)
            messagebox.showinfo("Success", "Recipe added successfully.")
            dialog.destroy()
            self.load_recipe_data()

        button_frame = tk.Frame(content_frame, bg=self.config.BG_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        add_ingredient_button = tk.Button(
            button_frame, 
            text="Add Ingredient", 
            command=add_ingredient,
            **self.config.BUTTON_STYLES["primary"]
        )
        add_ingredient_button.pack(side=tk.LEFT, padx=5)
        
        save_button = tk.Button(
            button_frame, 
            text="Save Recipe", 
            command=save_recipe,
            **self.config.BUTTON_STYLES["primary"]
        )
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(
            content_frame, 
            text="Cancel", 
            command=dialog.destroy, 
            **self.config.BUTTON_STYLES["secondary"]
        )
        cancel_button.pack(pady=5)

    def delete_recipe(self):
        if not self.selected_recipe_id:
            messagebox.showerror("Error", "No recipe selected.")
            return

        confirm = messagebox.askyesno("Delete Recipe", "Are you sure you want to delete this recipe?")
        if not confirm:
            return

        is_deleted = StaffController().deleteRecipe(self.selected_recipe_id)
        if is_deleted:
            messagebox.showinfo("Success", "Recipe deleted successfully.")
            self.load_recipe_data()
            self.selected_recipe_id = None
            if hasattr(self, 'delete_btn'):
                self.delete_btn.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Failed to delete recipe.")

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"{width}x{height}+{x}+{y}")
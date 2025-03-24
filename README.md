
<p align="center">
  <img src="https://github.com/VinnRe/StockOverflow/blob/merged-branches/images/stockoverflow_logo_wbg.png" alt="StockOverflow Logo">
</p>


# Stock Overflow

StockOverflow is a python app that is designed to help small to medium-sized food service businesses reduce food waste through effective inventory management. The system focuses on tracking perishable ingredients with their expiration dates, managing recipes, and monitoring stock levels.

<p>
  <img src="https://github.com/VinnRe/StockOverflow/blob/merged-branches/images/SDG12.png" alt="SDG12 Logo">
</p>

The project is made with [SDG 12: Responsible Consumption and Production](https://sdgs.un.org/goals/goal12) in mind. StockOverflow directly supports SDG 12 through several key mechanisms: Food Waste Reduction, Inventory Optimization, and Data Visibility
## 🤓 Developers

[🙋‍♂️ Briones, Sean Kyron](https://www.github.com/Seankyron)
| [🙋‍♂️ Capinpin, Kobe Andrew](https://www.github.com/VinnRe)

[🙋‍♂️ Cuarto, Mico Raphael](https://www.github.com/oocim)
| [🙋‍♀️ Odasco, Hersey Anne](https://www.github.com/herseyy)


## ❇️ Features ❇️

- Role-Based Access Control with Dynamic UI
    - Admin Role 
        - Has full access to all system functions including:
            - Adding, editing, and deleting inventory items
            - Creating new recipes
            - Full order management capabilities
            - User authentication
    - Staff Role 
        - Manages daily inventory operations with limited access:
            - Viewing inventory with status indicators
            - Making recipes from the recipe list
            - Creating basic orders
            - Receiving deliveries


- Recipe Manager
    - Stores recipes with their ingredient requirements
    - Verifies ingredient availability before recipe execution
    - Automatically updates inventory when recipes are made
    - Supports adding new recipes with ingredient quantities
    - Admin Only Features
        - Create a Recipe with the items from the inventory

- Admin Only Features
    - Inventory Tracking with Expiry Management
        - Displays inventory items with their quantities and expiration dates
        - Provides visual indicators for low stock (items with less than 20 units)
        - Highlights items nearing expiration (within 7 days)
        - Supports searching for specific items by name or ID
        - Sortable inventory list by item name, expiry date, or quantity

    - Order Management with Status Tracking
        - Create an order to restock items in inventory
        - Set orderes to be received and auto add the received items
        - Creates orders for new inventory items
        - Records order status (Pending/Received)
        - Updates inventory when orders are received
        - Includes a simple reordering system for low-stock items
        - Prevents re-receiving already received orders

- FIFO Management System
    - Tracks multiple batches of the same item with different expirat dates
    - When making recipes, automatically uses oldest stock first
    - Validates expiration dates when making recipes, skipping expire items
    - Deducts quantities from appropriate batches based on expiration dates
    - Prevents waste by prioritizing older inventory


- Simple Authentication System
    - Basic username/password authentication for admin access
    - Session management for current user
    - Role-based UI adaptation


## 💻 Tech Stack 🖥️

#### Programming Language: Python 3.13.2
    - Used for all backend logic and UI implementation

#### GUI Framework: Tkinter
    - Used for creating the desktop application interface
    - Custom styling with configurable colors and button styles
    - Responsive layout with frames and treeviews

#### Database: Firebase (Realtime Database)
    - Used for storing and retrieving all application data
    - Real-time synchronization between the application and database
    - Structured data storage for inventory, recipes, orders, and users



## 🗎 Documentation 🗎

The link below leads to the documentation of the system. It will provide the reason, UML Diagrams, and Summary of the Code

[Link to Documentation](https://docs.google.com/document/d/1nl6XO6EwzGRvPcKQMFHb6A0KTgOZ6peJ5dlKCMnDixI/edit?usp=sharing)


## 🖼️ Screenshots 🖼️

### Staff View
<p align="center">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/staffview_recipe.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/staffview_admin_auth.png" alt="Staff View Admin Auth">
</p>

### Admin View
<p align="center">
  <h3>Dashboard</h3>
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_dashboard_an.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_dashboard_is.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_dashboard_os.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_dashboard_rc.png" alt="Staff View Main">
  <h3>Recipe Management</h3>
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_recipe_m.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_recipe_ar.png" alt="Staff View Main">
  <h3>Inventory Management</h3>
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_inv_m.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_inv_ai.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_inv_ei.png" alt="Staff View Main">
  <h3>Order Management</h3>
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_order_m.png" alt="Staff View Main">
  <img src="https://github.com/VinnRe/StockOverflow/blob/beta-main/images/StockOverflow/adminview_order_no.png" alt="Staff View Main">
</p>
 
## 📁 Environment Variables 📁

To run this project, you will need to add the following environment variables to your .env file and you will need to create a key.json in the root folder

#### .env file
```bash
    DB_URL=https://link-to-your-firebase+data.base
```

#### key.json file
```bash
    {
        "type": "enter-service-type",
        "project_id": "enter-your-project-id",
        "private_key_id": "enter-your-private-key-id",
        "private_key": "enter-your-private-key",
        "client_email": "enter-the-account-email",
        "client_id": "enter-your-client-id",
        "auth_uri": "enter-the-auth-uri",
        "token_uri": "enter-the-token-uri",
        "auth_provider_x509_cert_url": "enter-the-auth-provider-cert-url",
        "client_x509_cert_url": "enter-the-client-cert-url",
        "universe_domain": "enter-the-univ-dom"
    }
```

#### DO NOT COMMIT YOUR .ENV FILE OR THE KEY.JSON TO YOUR REPO OR EVEN SEND THIS ANYWHERE!!!
## 🚀 Installation 🚀

We require using Python 3.10.x or above to use the system.
Here is the link to download [python](https://www.python.org/downloads/).

For the installation we assume that you're using VSCode to code in python. Here is the link for [VSCode](https://code.visualstudio.com/download)

### Windows Installation

#### Step 1: Clone the Repo!

First we clone the project. You can use Github Desktop or use the terminal.

```bash
  git clone https://github.com/VinnRe/StockOverflow.git
```

#### Step 2: Setting up the Virtual Environment

Inside the root folder of the project, create a virtual environment (venv) in VSCode

Press the keys Crtl + Shift + P to open up the Command Pallette, then type this in.

```bash
    >Python: Create Environment
```

Then press enter and select "Venv" option and select the interpreter path you want to use. In this case we select Python 3.10.x or Above.

```bash
    Python 3.10.x
```
    
Wait for the venv to finish installing.

After the venv finishes installing you need to activate the venv in the terminal

Press Ctrl + ` (tilde) to open up the Terminal in VSCode

Make sure you are in the ROOT FOLDER of the project. 

Write this in the terminal
```bash
    .venv\Scripts\activate
```

If you see this in your terminal it means that you have activated your venv.
```bash
    (.venv) path:\to\your\project>
```

#### Step 3: Installing all the dependencies

In the terminal write this to install all the used dependencies in the project.

```bash
    pip install -r requirements.txt
```

Wait for everything to install then we can move on to how run the program.


## 🏃 Run in your Machine 🏃‍♀️

Make sure you are in the root folder of the project.

To start the program, simply write this and now play around with it!

```bash
    python main.py
```

or use

```bash
    python3 main.py
```

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AuthController:
    def __init__(self):
        self.admin = None
        self.db_url = os.getenv("DB_URL") + "/user.json"

    def get_admin_credentials(self):
        response = requests.get(self.db_url)
        if response.status_code == 200:
            admin_data = response.json()
            if admin_data:
                return admin_data.get('username'), admin_data.get('password')
        return None, None

    def login_admin(self, username, password):
        stored_username, stored_password = self.get_admin_credentials()
        if stored_username and stored_password:
            if username == stored_username and password == stored_password:
                self.admin = (username, password)
                print("Login successful.")
                return True
        print("Invalid credentials.")
        return False

    def logout_admin(self):
        if self.admin:
            self.admin = None
            print("Logged out successfully.")
        else:
            print("No admin is logged in.")

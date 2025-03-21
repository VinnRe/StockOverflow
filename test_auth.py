from models.user import Admin

# Create an Admin instance
admin = Admin()

# Prompt for login credentials
username = input("Enter username: ")
password = input("Enter password: ")

# Attempt login
if admin.login(username, password):
    print("Admin is now logged in.")

    # Test logout
    logout_choice = input("Do you want to log out? (yes/no): ")
    if logout_choice.lower() == "yes":
        admin.logout()
else:
    print("Login failed. Check your credentials.")

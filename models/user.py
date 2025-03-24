from controllers.auth_controller import AuthController

class Admin:
    def __init__(self):
        # Initialize authentication controller
        self.auth_controller = AuthController()
        self.logged_in = False

    def login(self, input_username: str, input_password: str):
        # Attempt admin login and update login status
        if self.auth_controller.login_admin(input_username, input_password):
            self.logged_in = True
            return True
        return False

    def logout(self):
        # Logout only if currently logged in
        if self.logged_in:
            self.logged_in = False
            self.auth_controller.logout_admin()
        else:
            print("You are not logged in.")

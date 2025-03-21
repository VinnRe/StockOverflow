from controllers.auth import AuthController

class Admin:
    def __init__(self):
        self.auth_controller = AuthController()
        self.logged_in = False

    def login(self, input_username: str, input_password: str):
        if self.auth_controller.login_admin(input_username, input_password):
            self.logged_in = True
            return True
        return False

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            self.auth_controller.logout_admin()
        else:
            print("You are not logged in.")

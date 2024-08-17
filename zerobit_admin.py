class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def authenticate(self, entered_username, entered_password):
        return entered_username == self.username and entered_password == self.password
    

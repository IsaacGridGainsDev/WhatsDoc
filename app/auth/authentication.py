import os
import json
import hashlib
import secrets
from pathlib import Path

class Authentication:
    """
    Simple authentication system for WhatsDoc app
    """
    def __init__(self, data_dir=None):
        """
        Initialize authentication system
        
        Args:
            data_dir (str, optional): Directory to store user data
        """
        if data_dir is None:
            # Default to a 'users' directory in the app's data folder
            self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "users")
        else:
            self.data_dir = data_dir
        
        # Ensure the directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Path to the users file
        self.users_file = os.path.join(self.data_dir, "users.json")
        
        # Create users file if it doesn't exist
        if not os.path.exists(self.users_file):
            self._save_users({})
        
        # Current user
        self.current_user = None
    
    def register(self, username, password, email=None):
        """
        Register a new user
        
        Args:
            username (str): Username
            password (str): Password
            email (str, optional): Email address
            
        Returns:
            bool: Success status
        """
        # Load existing users
        users = self._load_users()
        
        # Check if username already exists
        if username in users:
            return False, "Username already exists"
        
        # Generate salt
        salt = secrets.token_hex(16)
        
        # Hash password with salt
        password_hash = self._hash_password(password, salt)
        
        # Create user
        users[username] = {
            "password_hash": password_hash,
            "salt": salt,
            "email": email,
            "created_at": self._get_timestamp()
        }
        
        # Save users
        self._save_users(users)
        
        return True, "User registered successfully"
    
    def login(self, username, password):
        """
        Login a user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            bool: Success status
        """
        # Load existing users
        users = self._load_users()
        
        # Check if username exists
        if username not in users:
            return False, "Invalid username or password"
        
        # Get user
        user = users[username]
        
        # Hash password with user's salt
        password_hash = self._hash_password(password, user["salt"])
        
        # Check if password matches
        if password_hash != user["password_hash"]:
            return False, "Invalid username or password"
        
        # Set current user
        self.current_user = username
        
        return True, "Login successful"
    
    def logout(self):
        """
        Logout the current user
        
        Returns:
            bool: Success status
        """
        if self.current_user is None:
            return False, "No user is logged in"
        
        self.current_user = None
        return True, "Logout successful"
    
    def is_logged_in(self):
        """
        Check if a user is logged in
        
        Returns:
            bool: True if a user is logged in, False otherwise
        """
        return self.current_user is not None
    
    def get_current_user(self):
        """
        Get the current user
        
        Returns:
            str: Username of the current user, or None if no user is logged in
        """
        return self.current_user
    
    def change_password(self, username, old_password, new_password):
        """
        Change a user's password
        
        Args:
            username (str): Username
            old_password (str): Old password
            new_password (str): New password
            
        Returns:
            bool: Success status
        """
        # Load existing users
        users = self._load_users()
        
        # Check if username exists
        if username not in users:
            return False, "User does not exist"
        
        # Get user
        user = users[username]
        
        # Hash old password with user's salt
        old_password_hash = self._hash_password(old_password, user["salt"])
        
        # Check if old password matches
        if old_password_hash != user["password_hash"]:
            return False, "Invalid password"
        
        # Generate new salt
        salt = secrets.token_hex(16)
        
        # Hash new password with new salt
        password_hash = self._hash_password(new_password, salt)
        
        # Update user
        user["password_hash"] = password_hash
        user["salt"] = salt
        users[username] = user
        
        # Save users
        self._save_users(users)
        
        return True, "Password changed successfully"
    
    def _hash_password(self, password, salt):
        """
        Hash a password with a salt
        
        Args:
            password (str): Password
            salt (str): Salt
            
        Returns:
            str: Hashed password
        """
        # Combine password and salt
        salted_password = password + salt
        
        # Hash with SHA-256
        hash_obj = hashlib.sha256(salted_password.encode())
        
        return hash_obj.hexdigest()
    
    def _load_users(self):
        """
        Load users from file
        
        Returns:
            dict: Users dictionary
        """
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {str(e)}")
            return {}
    
    def _save_users(self, users):
        """
        Save users to file
        
        Args:
            users (dict): Users dictionary
            
        Returns:
            bool: Success status
        """
        try:
            with open(self.users_file, "w") as f:
                json.dump(users, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving users: {str(e)}")
            return False
    
    def _get_timestamp(self):
        """
        Get current timestamp
        
        Returns:
            str: Timestamp
        """
        import datetime
        return datetime.datetime.now().isoformat()

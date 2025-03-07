from Models.user import User
from database.database import SessionLocal
from datetime import datetime

class UserService:
    def create_or_update_auth0_user(self, user_data):
        """Create or update user from Auth0 data"""
        db = SessionLocal()
        try:
            # Try to find existing user by email or auth_token
            user = db.query(User).filter(
                (User.email == user_data['email']) | 
                (User.auth_token == user_data['auth_token'])
            ).first()
            
            if not user:
                # Create new user
                user = User(**user_data)
                db.add(user)
                print(f"Creating new user: {user_data['email']}")
            else:
                # Update existing user
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.last_login = datetime.now()
                print(f"Updating existing user: {user_data['email']}")
            
            db.commit()
            db.refresh(user)
            return user, None
            
        except Exception as e:
            db.rollback()
            print(f"Database error: {str(e)}")
            return None, str(e)
        finally:
            db.close()

    def get_user_by_email(self, email):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.email == email).first()
        finally:
            db.close()

    def get_user_by_auth_token(self, auth_token):
        db = SessionLocal()
        try:
            return db.query(User).filter(User.auth_token == auth_token).first()
        finally:
            db.close()


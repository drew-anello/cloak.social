from Models.user import User
from database.database import SessionLocal
from datetime import datetime

class UserService:
    def create_or_update_auth0_user(self, auth0_user):
        """Create or update user from Auth0 data"""
        db = SessionLocal()
        try:
            # Try to find existing user
            user = db.query(User).filter(User.email == auth0_user['email']).first()
            
            if not user:
                user = User(
                    username=auth0_user.get('nickname', auth0_user['email']),
                    email=auth0_user['email'],
                    password='auth0_user',  # placeholder since Auth0 handles auth
                    dob=datetime.now(),
                    account_type='standard',
                    is_active=True,
                    is_admin=False,
                    admin_level=0,
                    auth_token=auth0_user.get('sub')  # Store Auth0 user ID
                )
                db.add(user)
            else:
                user.last_login = datetime.now()
                user.auth_token = auth0_user.get('sub')
            
            db.commit()
            db.refresh(user)
            return user, None
            
        except Exception as e:
            db.rollback()
            return None, str(e)
        finally:
            db.close()


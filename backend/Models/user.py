from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Column, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import validates
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    admin_level: Mapped[int] = mapped_column(default=0, nullable=True)
    dob: Mapped[datetime] = mapped_column(nullable=False)
    account_type: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    last_login: Mapped[datetime] = mapped_column(default=datetime.now)
    auth_token: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', is_admin={self.is_admin}, admin_level={self.admin_level})>"
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'is_user': self.is_user,
            'is_admin': self.is_admin,
            'admin_level': self.admin_level,
            'account_type': self.account_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'dob': self.dob.isoformat() if self.dob else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    



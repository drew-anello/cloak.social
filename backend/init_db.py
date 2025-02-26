from database import engine
from Models import User, Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("creating database tables...")
    init_db()
    print("database tables created")
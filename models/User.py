from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey
from database.__init__ import Base,SessionLocal
import pandas as pd
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    fullname = Column(String, index=True)
    address = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(Integer, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    role_id = Column(Integer, ForeignKey('role.role_id'),index=True)
    
    
print("User model created successfully.")


def import_user_data(csv_file_path):
    """
    Import data into the User table from a CSV file.
    """
    try:
        df = pd.read_csv(csv_file_path)
        with SessionLocal() as session:
            for _, row in df.iterrows():
                user = User(
                    fullname=row['fullname'],
                    address=row['address'],
                    email=row['email'],
                    phone=row['phone'],
                    username=row['username'],
                    password=row['password'],  # Hash password
                    role_id=row['role_id'],  # Ensure roles exist in Role table
                )
                session.add(user)
            session.commit()
            print(f"User data imported successfully from {csv_file_path}")
    except Exception as e:
        print(f"Error importing User data: {e}")


import_user_data('user.csv')
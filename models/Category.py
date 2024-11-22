# FILE: Category.py
from sqlalchemy import Column, Integer, String, BigInteger
from database.__init__ import Base,SessionLocal
import pandas as pd
class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, index=True, primary_key=True)
    name = Column(String, index=True)
    
print("Category model created successfully.")

def import_csv_to_database(csv_file_path):
    # Create a session
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)
        
        # Convert DataFrame rows to Payment objects
        with SessionLocal() as session:
            for _, row in df.iterrows():
                role = Category(name=row['name'])  # Match column name in CSV
                session.add(role)
            
            # Commit the session
            session.commit()
            print(f"Data imported successfully from {csv_file_path}")
    except Exception as e:
        print(f"Error importing data: {e}")

    
import_csv_to_database('category.csv')
from sqlalchemy import Column, Integer, String, BigInteger
from database.__init__ import Base,SessionLocal
import pandas as pd
class Role(Base):
    __tablename__ = "role"
    
    
    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    
print("Role model created successfully.")

def import_role_data(csv_file_path):
    # Create a session
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file_path)
        
        # Convert DataFrame rows to Payment objects
        with SessionLocal() as session:
            for _, row in df.iterrows():
                role = Role(name=row['name'])  # Match column name in CSV
                session.add(role)
            
            # Commit the session
            session.commit()
            print(f"Data imported successfully from {csv_file_path}")
    except Exception as e:
        print(f"Error importing data: {e}")

    
#import_csv_to_database('role.csv')
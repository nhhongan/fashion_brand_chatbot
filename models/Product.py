
from sqlalchemy import Column, Integer, String, BigInteger,ForeignKey
from database.__init__ import Base,SessionLocal
import pandas as pd
class Product(Base):
    __tablename__ = "product"
    
    product_id = Column(Integer,primary_key=True, index=True,autoincrement=True)
    name = Column(String, index=True)
    department = Column(String, index=True)
    clothing = Column(String, index=True)
    type_of_clothing = Column(String, index=True)
    price = Column(String, index=True)
    color = Column(String, index=True)
    


print("Product model created successfully.")




def import_product_data(csv_file_path):
    """
    Import data into the Product table from a CSV file.
    """
    try:
        df = pd.read_csv(csv_file_path)
        with SessionLocal() as session:
            for _, row in df.iterrows():
                user = Product(
                    product_id = row['product_id'],
                    name = row['name'],
                    department = row['department'],
                    clothing = row['clothing'],
                    type_of_clothing=  row['type_of_clothing'],
                    price = row['price'],
                    color = row['color']
                )
                session.add(user)
            session.commit()
            print(f"User data imported successfully from {csv_file_path}")
    except Exception as e:
        print(f"Error importing User data: {e}")


import_product_data('product_df3.csv')
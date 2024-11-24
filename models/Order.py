import pandas as pd
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.exc import SQLAlchemyError

from database.__init__ import Base, SessionLocal


class Order(Base):
    __tablename__ = "order"
    
    order_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    payment_id = Column(Integer, ForeignKey('payment.payment_id'), index=True)
    product_id = Column(Integer, ForeignKey('product.product_id'), index=True)
    
    
print("Order model created successfully.")

def fetch_product_price(session, product_id):
    """
    Fetch the price of a product from the product table based on product_id.
    """
    try:
        product = session.execute(f"SELECT price FROM product WHERE product_id = {product_id}").fetchone()
        return product[0] if product else 0
    except SQLAlchemyError as e:
        print(f"Error fetching product price: {e}")
        return 0

# def import_order_data(csv_file_path):
#     """
#     Import data into the Order table from a CSV file, ensuring compatibility with the database schema.
#     """
#     try:
#         # Read the CSV file
#         df = pd.read_csv(csv_file_path)

#         # Convert all numeric columns to native Python integers
#         numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
#         for col in numeric_columns:
#             df[col] = df[col].fillna(0).astype(int).apply(int)

#         # Create a new database session
#         with SessionLocal() as session:
#             for _, row in df.iterrows():
#                 # Ensure values are converted to Python types
#                 order = Order(
#                     order_id=int(row['order_id']),
#                     user_id=int(row['user_id']),
#                     quantity=int(row['quantity']),
#                     payment_id=int(row['payment_id']),
#                     product_id=int(row['product_id']),
#                 )
#                 session.add(order)

#             # Commit the session
#             session.commit()
#             print(f"Order data imported successfully from {csv_file_path}")

#     except SQLAlchemyError as sql_err:
#         print(f"Database error occurred: {sql_err}")
#     except ValueError as val_err:
#         print(f"Value error in CSV data: {val_err}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
        
        
# import_order_data('order_formatted.csv')

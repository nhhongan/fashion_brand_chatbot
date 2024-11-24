import pandas as pd
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.exc import SQLAlchemyError

from database.__init__ import Base, SessionLocal


class Order(Base):
    __tablename__ = "order"
    
    order_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_id = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    total_price = Column(BigInteger, index=True)
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

def import_order_data(csv_file_path):
    """
    Import data into the Order table from a CSV file, calculating total_price.
    """
    try:
        df = pd.read_csv(csv_file_path)
        with SessionLocal() as session:
            for _, row in df.iterrows():
                price = fetch_product_price(session, row['product_id'])
                total_price = row['quantity'] * price
                order = Order(
                    order_id=row['order_id'],
                    user_id=row['user_id'],
                    quantity=row['quantity'],
                    total_price=total_price,
                    payment_id=row['payment_id'],
                    product_id=row['product_id'],
                )
                session.add(order)
            session.commit()
            print(f"Order data imported successfully from {csv_file_path}")
    except Exception as e:
        print(f"Error importing Order data: {e}")


import_order_data('fashion_brand_chatbot/order.csv')


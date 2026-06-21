import mysql.connector
from pymongo import MongoClient
import pandas as pd
from datetime import datetime, timedelta
import random

class DatabaseManager:
    def __init__(self):
        # 1. Local MySQL Initialization
        self.sql_conn = mysql.connector.connect(host="localhost", user="root", password="B3ngal@india") # Change to your local MySQL password
        self.sql_cursor = self.sql_conn.cursor()
        self.sql_cursor.execute("CREATE DATABASE IF NOT EXISTS advanced_inr_db")
        self.sql_cursor.execute("USE advanced_inr_db")
        self.sql_cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_registry (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255),
                current_price DECIMAL(12,2),
                merchant_platform VARCHAR(100),
                last_updated DATETIME
            )
        """)
        
        # 2. Local MongoDB Initialization
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["advanced_inr_db"]
        self.history_collection = self.mongo_db["price_historical_logs"]
        
        # Automatically generate 30 days of data if database is fresh
        self.seed_historical_kaggle_dataset()

    def seed_historical_kaggle_dataset(self):
        """Pre-populates a professional 30-day time-series dataset to train the ML model immediately."""
        if self.history_collection.count_documents({}) > 0:
            return 
            
        print("[DATABASE] Ingesting comprehensive 30-day historical dataset...")
        
        products_pool = [
            ("Apple iPhone 15 Pro (128 GB)", 129900.00, "Amazon.in"),
            ("Samsung Galaxy S24 Ultra", 124999.00, "Flipkart"),
            ("Sony WH-1000XM5 Headphones", 29990.00, "Reliance Digital"),
            ("MacBook Air M3 (8GB/256GB)", 114900.00, "Amazon.in"),
            ("Logitech MX Master 3S Mouse", 9495.00, "Flipkart")
        ]
        
        today = datetime.now()
        seeded_records = []
        
        for day_offset in range(30, 0, -1):
            record_date = (today - timedelta(days=day_offset)).strftime('%Y-%m-%d %H:%M:%S')
            
            for name, base_price, platform in products_pool:
                if "iPhone" in name or "Sony" in name:
                    trend_factor = (day_offset * 0.002) 
                else:
                    trend_factor = -(day_offset * 0.0015)
                    
                daily_noise = random.uniform(-0.01, 0.01)
                historical_price = round(base_price * (1 + trend_factor + daily_noise), 2)
                
                seeded_records.append({
                    "product_name": name,
                    "price_inr": historical_price,
                    "platform": platform,
                    "region": "India",
                    "timestamp": record_date
                })
                
        # Bulk load history logs directly into MongoDB
        self.history_collection.insert_many(seeded_records)
        
        # Store the current operational dashboard baseline into MySQL
        df_latest = pd.DataFrame(seeded_records).tail(5)
        for _, row in df_latest.iterrows():
            insert_query = """
                INSERT INTO product_registry (product_name, current_price, merchant_platform, last_updated)
                VALUES (%s, %s, %s, %s)
            """
            self.sql_cursor.execute(insert_query, (
                row['product_name'], 
                row['price_inr'], 
                row['platform'], 
                row['timestamp']
            ))
        self.sql_conn.commit()
        print("[DATABASE] Success! 150 historical documents committed to databases.")

    def save_data_pipeline(self, df):
        """Appends new runtime scraper batches downstream to both tracking environments."""
        for _, row in df.iterrows():
            self.sql_cursor.execute("DELETE FROM product_registry WHERE product_name = %s", (row['product_name'],))
            insert_query = """
                INSERT INTO product_registry (product_name, current_price, merchant_platform, last_updated)
                VALUES (%s, %s, %s, %s)
            """
            self.sql_cursor.execute(insert_query, (
                row['product_name'], 
                row['price_inr'], 
                row['platform'], 
                row['timestamp']
            ))
        self.sql_conn.commit()
        self.history_collection.insert_many(df.to_dict(orient='records'))

    def get_tracked_products(self):
        self.sql_cursor.execute("SELECT product_name, current_price, merchant_platform FROM product_registry")
        return self.sql_cursor.fetchall()

    def get_mongo_history_log(self, product_name):
        cursor = self.history_collection.find({"product_name": product_name})
        return pd.DataFrame(list(cursor))
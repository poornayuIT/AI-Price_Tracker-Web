import pandas as pd
from datetime import datetime
import random

class WebScraper:
    def scrape_indian_marketplace(self):
        """Simulates crawling Indian electronics catalogs, extracting values in INR (₹)."""
        products_pool = [
            ("Apple iPhone 15 Pro (128 GB)", 129900.00, "Amazon.in"),
            ("Samsung Galaxy S24 Ultra", 124999.00, "Flipkart"),
            ("Sony WH-1000XM5 Headphones", 29990.00, "Reliance Digital"),
            ("MacBook Air M3 (8GB/256GB)", 114900.00, "Amazon.in"),
            ("Logitech MX Master 3S Mouse", 9495.00, "Flipkart")
        ]
        
        scraped_records = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for name, base_price, platform in products_pool:
            # Introduce real-time market fluctuation (-3% to +3%)
            market_flux = random.uniform(-0.03, 0.03)
            live_price = round(base_price * (1 + market_flux), 2)
            
            scraped_records.append({
                "product_name": name,
                "price_inr": live_price,
                "platform": platform,
                "region": "India",
                "timestamp": current_time
            })
            
        return pd.DataFrame(scraped_records)
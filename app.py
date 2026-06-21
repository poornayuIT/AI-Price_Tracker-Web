from flask import Flask, render_template, redirect
from src.scraper import WebScraper
from src.database import DatabaseManager
from src.forecaster import AIPriceForecaster

app = Flask(__name__)
db_engine = DatabaseManager()
scraper_engine = WebScraper()

@app.route('/')
def dashboard_view():
    active_inventory = db_engine.get_tracked_products()
    compiled_data = []
    
    for item in active_inventory:
        name, current_price, platform = item
        
        # Load time-series history records from MongoDB cluster
        history_df = db_engine.get_mongo_history_log(name)
        
        # Execute ML Scikit-Learn predictions
        ai_status, projected_shift, model_reliability = AIPriceForecaster.run_prediction_engine(history_df)
        
        compiled_data.append({
            "name": name,
            "price": f"₹{float(current_price):,.2f}", 
            "merchant": platform,
            "status": ai_status,
            "shift": f"₹{projected_shift:,.2f}" if isinstance(projected_shift, (int, float)) else projected_shift,
            "accuracy": model_reliability,
            "datapoints": len(history_df)
        })
        
    return render_template('index.html', products=compiled_data)

@app.route('/trigger-pipeline', methods=['POST'])
def trigger_pipeline():
    fresh_df = scraper_engine.scrape_indian_marketplace()
    db_engine.save_data_pipeline(fresh_df)
    return redirect('/')

if __name__ == '__main__':
    print("[SERVER] Spinning up the Flask Web Dashboard on HTTP port 5000...")
    app.run(debug=True, port=5000)
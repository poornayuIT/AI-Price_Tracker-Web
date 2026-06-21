from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import numpy as np

class AIPriceForecaster:
    @staticmethod
    def run_prediction_engine(historical_df):
        """Uses Linear Regression to isolate price paths and checks accuracy using MAE."""
        if len(historical_df) < 4:
            return "Model Training Required", 0.00, "N/A"
            
        historical_df['time_step'] = range(len(historical_df))
        
        X = historical_df[['time_step']].values
        y = historical_df['price_inr'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Calculate regression historical error checking parameters
        predictions = model.predict(X)
        mae_score = mean_absolute_error(y, predictions)
        
        # Predict price value for the next time-step
        next_step = np.array([[len(historical_df)]])
        projected_cost = model.predict(next_step)[0]
        
        price_delta = projected_cost - y[-1]
        
        if price_delta > 0:
            status = "PRICE SPIKE EXPECTED 📈"
        elif price_delta < 0:
            status = "PRICE DROP EXPECTED 📉"
        else:
            status = "STABLE MARKET ⚖️"
            
        return status, round(abs(price_delta), 2), f"₹{round(mae_score, 2)}"
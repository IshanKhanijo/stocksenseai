import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import os
import base64
import time
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="AI Predict | StockSense AI", layout="wide")
st.title("📈 AI Stock Predictor")
st.markdown("Enter a stock ticker to predict the next closing price using 10 years of historical OHLCV data.")

def show_loading_gif(gif_path="trader_robot.gif"):
    try:
        with open(gif_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <img src="data:image/gif;base64,{encoded}" width="300" />
                    <div style="font-size:18px; font-weight:600; margin-top:12px;">Crunching the markets...</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        st.warning("⚠️ Loading GIF not found.")

class StockLSTMPredictor:
    def __init__(self, symbol='AAPL', lookback_window=90):
        self.symbol = symbol
        self.lookback_window = lookback_window
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        
    def fetch_data(self, period='10y'):
        """Fetch stock data from Yahoo Finance"""
        print(f"Fetching {self.symbol} data...")
        stock = yf.Ticker(self.symbol)
        data = stock.history(period=period)
        
        # Use multiple features for better prediction
        features = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.data = data[features].copy()
        
        # Add technical indicators
        self.data['MA_10'] = self.data['Close'].rolling(window=10).mean()
        self.data['MA_30'] = self.data['Close'].rolling(window=30).mean()
        self.data['Volatility'] = self.data['Close'].rolling(window=10).std()
        self.data['Price_Change'] = self.data['Close'].pct_change()
        
        # Drop NaN values
        self.data = self.data.dropna()
        
        return self.data
    
    def prepare_data(self, test_size=0.2):
        """Prepare data for LSTM training"""
        # Scale the data
        scaled_data = self.scaler.fit_transform(self.data)
        
        # Create sequences
        X, y = [], []
        for i in range(self.lookback_window, len(scaled_data)):
            X.append(scaled_data[i-self.lookback_window:i])
            y.append(scaled_data[i, 3])  # Close price is at index 3
        
        X, y = np.array(X), np.array(y)
        
        # Split into train and test sets
        split_idx = int(len(X) * (1 - test_size))
        
        self.X_train = X[:split_idx]
        self.X_test = X[split_idx:]
        self.y_train = y[:split_idx]
        self.y_test = y[split_idx:]
        
    def build_model(self):
        """Build LSTM model"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.X_train.shape[1], self.X_train.shape[2])),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        self.model = model
        
    def train_model(self, epochs=50, batch_size=32, validation_split=0.2):
        """Train the LSTM model"""
        from tensorflow.keras.callbacks import EarlyStopping
        
        early_stopping = EarlyStopping(
            monitor='val_loss', patience=10, restore_best_weights=True
        )
        
        history = self.model.fit(
            self.X_train, self.y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=validation_split,
            callbacks=[early_stopping],
            verbose=1
        )
        
        return history
    
    def evaluate_model(self):
        """Evaluate model performance"""
        # Make predictions
        train_pred = self.model.predict(self.X_train)
        test_pred = self.model.predict(self.X_test)
        
        # Inverse transform predictions (only for close price)
        # Create dummy array with same shape as original data
        dummy_train = np.zeros((len(train_pred), self.data.shape[1]))
        dummy_test = np.zeros((len(test_pred), self.data.shape[1]))
        dummy_train[:, 3] = train_pred.flatten()
        dummy_test[:, 3] = test_pred.flatten()
        
        train_pred_scaled = self.scaler.inverse_transform(dummy_train)[:, 3]
        test_pred_scaled = self.scaler.inverse_transform(dummy_test)[:, 3]
        
        # Inverse transform actual values
        dummy_y_train = np.zeros((len(self.y_train), self.data.shape[1]))
        dummy_y_test = np.zeros((len(self.y_test), self.data.shape[1]))
        dummy_y_train[:, 3] = self.y_train
        dummy_y_test[:, 3] = self.y_test
        
        y_train_scaled = self.scaler.inverse_transform(dummy_y_train)[:, 3]
        y_test_scaled = self.scaler.inverse_transform(dummy_y_test)[:, 3]
        
        # Calculate metrics
        test_rmse = np.sqrt(mean_squared_error(y_test_scaled, test_pred_scaled))
        test_mae = mean_absolute_error(y_test_scaled, test_pred_scaled)
        test_r2 = r2_score(y_test_scaled, test_pred_scaled)
        
        return test_mae, test_rmse, test_r2
    
    def predict_next_day(self):
        """Predict next day's closing price"""
        # Get last sequence from the data
        last_sequence = self.scaler.transform(self.data.tail(self.lookback_window))
        last_sequence = last_sequence.reshape(1, self.lookback_window, -1)
        
        # Make prediction
        pred_scaled = self.model.predict(last_sequence)
        
        # Inverse transform
        dummy = np.zeros((1, self.data.shape[1]))
        dummy[0, 3] = pred_scaled[0, 0]
        pred_price = self.scaler.inverse_transform(dummy)[0, 3]
        
        return pred_price
    
    def save_model_and_scaler(self, model_path, scaler_path):
        """Save trained model and scaler"""
        self.model.save(model_path)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def load_model_and_scaler(self, model_path, scaler_path):
        """Load trained model and scaler"""
        self.model = load_model(model_path)
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)

# Streamlit UI
ticker = st.text_input("📥 Enter Stock Ticker (e.g. AAPL, TSLA):", value="AAPL").upper()
look_back = 90
model_path = f"models/{ticker}_lstm_model.keras"
scaler_path = f"models/{ticker}_scaler.pkl"

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

if st.button("🔮 Predict Next Day Price"):
    show_loading_gif()
    time.sleep(2)

    try:
        # Initialize predictor
        predictor = StockLSTMPredictor(symbol=ticker, lookback_window=look_back)
        
        # Fetch data
        df = predictor.fetch_data(period="10y")
        if df.empty or df.shape[0] < 100:
            st.error("❌ Not enough historical data downloaded.")
            st.stop()
        st.write("✅ Raw data downloaded:", df.shape[0], "rows")
        
    except Exception as e:
        st.error(f"❌ Error downloading data: {str(e)}")
        st.stop()

    try:
        # Check if model exists
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            st.info("🔄 Loading existing model...")
            predictor.load_model_and_scaler(model_path, scaler_path)
            
            # Still need to prepare data for prediction
            predictor.prepare_data(test_size=0.2)
            
        else:
            st.info("🏗️ Training new model...")
            # Prepare data
            predictor.prepare_data(test_size=0.2)
            
            # Build and train model
            predictor.build_model()
            predictor.train_model(epochs=50, batch_size=32)
            
            # Save model and scaler
            predictor.save_model_and_scaler(model_path, scaler_path)
            st.success("💾 Model saved for future use!")
            
    except Exception as e:
        st.error(f"❌ Error loading/training model: {str(e)}")
        st.stop()

    try:
        # Evaluate model
        mae, rmse, r2 = predictor.evaluate_model()
        
        # Make next day prediction
        predicted_price = predictor.predict_next_day()
        
    except Exception as e:
        st.error(f"❌ Error in prediction: {str(e)}")
        st.stop()

    # Display results with your exact UI format
    st.success("✅ Prediction Complete")
    st.markdown(f"### 📈 Predicted Closing Price for Next Day ({ticker}): **${float(predicted_price):.2f}**")
    

# Add some additional info
st.markdown("---")
st.markdown("### ℹ️ Model Information")
st.markdown("""
**Features Used:**
- Open, High, Low, Close, Volume prices
- 10-day and 30-day Moving Averages
- Price volatility and change patterns
- 90-day lookback window for temporal patterns

**Model Architecture:**
- 3-layer LSTM with dropout regularization
- 50 units per LSTM layer
- Dense layers for final prediction
- Early stopping to prevent overfitting

**Note:** Models are automatically saved and reused for faster predictions on subsequent runs.
""")
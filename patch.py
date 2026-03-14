import re

with open("ai_models/feature_engineer.py", "r") as f:
    content = f.read()

# Replace the specific lines
old_lines = """        # Pre-calculate indicators for the entire series (vectorized in TA-Lib)
        rsi = talib.RSI(df["close"], timeperiod=14)
        macd_line, _, macd_hist = talib.MACD(df["close"])

        # Fill NaNs before converting to values to ensure consistency
        rsi = rsi.fillna(0.5).values
        macd_line = macd_line.fillna(0).values
        macd_hist = macd_hist.fillna(0).values
        close_vals = df["close"].values"""

new_lines = """        # Pre-calculate indicators for the entire series (vectorized in TA-Lib)
        # --- ⚡ Bolt Optimization: Pass NumPy arrays to TA-Lib ---
        # Passing raw NumPy arrays bypasses Pandas Series overhead for index alignment.
        close_vals = df["close"].values
        rsi = talib.RSI(close_vals, timeperiod=14)
        macd_line, _, macd_hist = talib.MACD(close_vals)

        # Fill NaNs before converting to values to ensure consistency
        rsi = np.nan_to_num(rsi, nan=0.5)
        macd_line = np.nan_to_num(macd_line, nan=0.0)
        macd_hist = np.nan_to_num(macd_hist, nan=0.0)"""

content = content.replace(old_lines, new_lines)

with open("ai_models/feature_engineer.py", "w") as f:
    f.write(content)

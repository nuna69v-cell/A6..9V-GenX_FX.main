import re

with open(".jules/bolt.md", "r") as f:
    content = f.read()

# Add the new journal entry
new_entry = """
## 2026-03-14 - Passing NumPy Arrays to TA-Lib and NaN handling
**Learning:** I identified a performance bottleneck in `ai_models/feature_engineer.py` where Pandas Series were passed directly to `talib.RSI` and `talib.MACD`. I also noticed that the `fillna` function on the result was executed as Pandas Series methods instead of using NumPy array techniques, leading to suboptimal performance due to Pandas series overhead.
**Action:** Extract `.values` from DataFrame columns first to get NumPy arrays, and pass these arrays directly to `talib` functions. Use `np.nan_to_num` for efficient NaN handling instead of Pandas `fillna()`. This removes index alignment and series validation overhead from Pandas in the performance-sensitive feature engineering path.
"""
content += new_entry

with open(".jules/bolt.md", "w") as f:
    f.write(content)

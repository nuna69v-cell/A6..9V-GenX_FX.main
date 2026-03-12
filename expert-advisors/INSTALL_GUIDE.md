# GenX FX EA - MT5 Installation Guide

## Files
| File | Broker | Account | Server |
|------|--------|---------|--------|
| `GenX_Exness_MT5.mq5` | Exness | 169926536 | Exness-MT5Real24 |
| `GenX_FxPro_MT5.mq5`  | FxPro  | 530142568 | FxPro-MT5 Live02 |

---

## Step 1 — Deploy your dashboard (get your URL)

Before installing the EA, you need a **public URL** for your dashboard.
- Click **Deploy** (Publish) on your Replit project
- Your URL will look like: `https://genx-fx-yourname.replit.app`
- Copy this URL — you'll paste it into the EA settings

---

## Step 2 — Allow WebRequests in MT5

This is **required** or the EA cannot connect to the server.

1. Open MT5
2. Go to **Tools → Options → Expert Advisors** tab
3. Check **"Allow WebRequest for listed URL"**
4. Click **Add URL** and enter your Replit dashboard URL
   - Example: `https://genx-fx-yourname.replit.app`
5. Click **OK**

---

## Step 3 — Copy the EA file to MT5

### For Exness (account 169926536):
1. In MT5 go to **File → Open Data Folder**
2. Navigate to `MQL5 → Experts`
3. Copy **`GenX_Exness_MT5.mq5`** into that folder
4. In MT5, open **MetaEditor** (press F4)
5. Open the file and click **Compile** (F7) — should show 0 errors

### For FxPro (account 530142568):
1. Do the same on your FxPro MT5 terminal
2. Copy **`GenX_FxPro_MT5.mq5`** into `MQL5 → Experts`
3. Compile it in MetaEditor

---

## Step 4 — Attach EA to a chart

1. Open any chart (e.g. XAUUSD H1)
2. In the **Navigator** panel, find your EA under **Expert Advisors**
3. Drag it onto the chart
4. In the EA settings dialog:
   - Set **ServerURL** = your Replit dashboard URL
   - **AccountNumber** is pre-filled (169926536 or 530142568)
   - **BrokerServer** is pre-filled
   - Set **EnableAutoTrade** = true
   - Adjust **RiskPercent** (default 1%)
5. Click **OK**
6. Make sure **AutoTrading** button is ON (green) in the MT5 toolbar

---

## Step 5 — Verify connection

1. Check the MT5 **Experts** tab in the terminal — you should see:
   ```
   GenX FX EA (Exness) v3.0 starting
   Registered with server. ID: exness_169926536_...
   ```
2. In your **GenX dashboard**, refresh the Broker Accounts panel
3. The account should now show **CONNECTED** with balance/equity

---

## Step 6 — Send a test signal

1. In the dashboard, go to the **Broker Accounts** section
2. Click **Broadcast Signal**
3. Set direction (BUY/SELL), symbol, entry, SL, TP
4. Click **Broadcast to All EAs** or **Test** for a dummy signal
5. Watch the MT5 terminal — the trade should execute

---

## Settings Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| ServerURL | (your URL) | Your deployed Replit dashboard URL |
| RiskPercent | 1.0 | % of balance to risk per trade |
| DefaultLotSize | 0.01 | Lot size if no SL is given |
| MaxLotSize | 1.0 | Hard cap on lot size |
| MaxOpenPositions | 5 | Max concurrent trades per EA |
| MaxSpreadPoints | 50 | Skip trade if spread exceeds this |
| SignalPollSec | 5 | How often EA checks for new signals |
| HeartbeatSec | 30 | How often EA reports status |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| EA shows "WebRequest failed" | Add dashboard URL to Tools → Options → Expert Advisors → Allow WebRequest |
| EA shows "Registration failed" | Check ServerURL is correct and app is deployed (not just running in dev) |
| CONNECTED not showing in dashboard | Wait 30 seconds for heartbeat, then click Refresh |
| Trade not executing | Check AutoTrading is ON, EA is attached, EnableAutoTrade=true |

//+------------------------------------------------------------------+
//|  GenX FX - FxPro MT5 EA                                         |
//|  Broker  : FxPro-MT5 Live02                                     |
//|  Account : 530142568                                            |
//|  Connects to GenX dashboard via HTTP REST API                   |
//|  Version : 3.0                                                  |
//+------------------------------------------------------------------+
#property copyright "GenX FX Trading System"
#property version   "3.00"
#property strict

#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>

//--- !! IMPORTANT: In MT5, go to Tools > Options > Expert Advisors
//---    and add your server URL to the "Allow WebRequest for listed URL" list.

//--- Server settings (edit ServerURL to match your deployed Replit URL)
input string   ServerURL        = "https://YOUR-REPLIT-APP.replit.app"; // Dashboard server URL
input string   BrokerID         = "fxpro";                               // Broker identifier
input string   AccountNumber    = "530142568";                            // MT5 account number
input string   BrokerServer     = "FxPro-MT5 Live02";                   // Broker server name

//--- Trading settings
input int      MagicNumber      = 530142;   // Magic number for orders
input double   DefaultLotSize   = 0.01;     // Default lot size
input double   MaxLotSize       = 1.0;      // Maximum lot size
input double   RiskPercent      = 1.0;      // Risk % per trade (0 = use signal lot)
input int      MaxOpenPositions = 5;        // Max open positions
input int      MaxSpreadPoints  = 50;       // Max spread in points to trade
input bool     EnableAutoTrade  = true;     // Enable/disable auto execution
input int      SlippagePoints   = 10;       // Allowed slippage in points

//--- Polling settings
input int      SignalPollSec    = 5;        // How often to poll for signals (seconds)
input int      HeartbeatSec     = 30;       // Heartbeat interval (seconds)
input bool     DebugLog         = true;     // Print debug messages

//--- Globals
CTrade         trade;
CPositionInfo  posInfo;
string         connectionId     = "";
datetime       lastPoll         = 0;
datetime       lastHeartbeat    = 0;
bool           registered       = false;

//+------------------------------------------------------------------+
int OnInit()
{
   trade.SetExpertMagicNumber(MagicNumber);
   trade.SetDeviationInPoints(SlippagePoints);
   trade.SetTypeFilling(ORDER_FILLING_IOC);

   Print("=== GenX FX EA (FxPro) v3.0 starting ===");
   Print("Server: ", ServerURL);
   Print("Account: ", AccountNumber, " on ", BrokerServer);

   connectionId = BrokerID + "_" + AccountNumber + "_" + IntegerToString((int)TimeLocal());

   if(!RegisterWithServer())
      Print("WARNING: Could not register with server. Will retry on next tick.");

   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   if(registered)
      UnregisterFromServer();
   Print("=== GenX FX EA (FxPro) stopped ===");
}

//+------------------------------------------------------------------+
void OnTick()
{
   datetime now = TimeLocal();

   if(now - lastHeartbeat >= HeartbeatSec)
   {
      if(!registered)
         RegisterWithServer();
      else
         SendHeartbeat();
      lastHeartbeat = now;
   }

   if(EnableAutoTrade && registered && (now - lastPoll >= SignalPollSec))
   {
      PollAndExecuteSignals();
      lastPoll = now;
   }
}

//+------------------------------------------------------------------+
bool RegisterWithServer()
{
   string body = "{\"eaName\":\"GenX-FxPro-EA\","
               + "\"connectionId\":\"" + connectionId + "\","
               + "\"accountNumber\":\"" + AccountNumber + "\","
               + "\"symbol\":\"" + Symbol() + "\","
               + "\"timeframe\":\"" + EnumToString(Period()) + "\","
               + "\"broker\":\"" + BrokerID + "\","
               + "\"server\":\"" + BrokerServer + "\"}";

   string response = HttpPost(ServerURL + "/api/mt45/register", body);
   if(response == "") return false;

   if(StringFind(response, "\"success\":true") >= 0)
   {
      registered = true;
      if(DebugLog) Print("Registered with server. ID: ", connectionId);
      return true;
   }
   Print("Registration failed: ", response);
   return false;
}

//+------------------------------------------------------------------+
void UnregisterFromServer()
{
   string body = "{\"connectionId\":\"" + connectionId + "\"}";
   HttpPost(ServerURL + "/api/mt45/unregister", body);
   registered = false;
}

//+------------------------------------------------------------------+
void SendHeartbeat()
{
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double equity  = AccountInfoDouble(ACCOUNT_EQUITY);

   string body = "{\"connectionId\":\"" + connectionId + "\","
               + "\"status\":\"active\","
               + "\"balance\":" + DoubleToString(balance, 2) + ","
               + "\"equity\":"  + DoubleToString(equity, 2)  + ","
               + "\"openPositions\":" + IntegerToString(CountOpenPositions()) + "}";

   string response = HttpPost(ServerURL + "/api/mt45/heartbeat", body);
   if(DebugLog && response != "") Print("Heartbeat OK");
}

//+------------------------------------------------------------------+
void PollAndExecuteSignals()
{
   string response = HttpGet(ServerURL + "/api/mt45/signals/" + connectionId);
   if(response == "" || StringFind(response, "\"signals\":[]") >= 0) return;

   if(DebugLog) Print("Signals received: ", response);

   int pos = 0;
   while(true)
   {
      int signalStart = StringFind(response, "{\"signal\":", pos);
      if(signalStart < 0) break;

      int signalEnd = StringFind(response, "}", signalStart);
      if(signalEnd < 0) break;

      string signalObj = StringSubstr(response, signalStart, signalEnd - signalStart + 1);
      ProcessSignalJSON(signalObj);
      pos = signalEnd + 1;
   }
}

//+------------------------------------------------------------------+
void ProcessSignalJSON(string json)
{
   string direction  = ExtractStringValue(json, "signal");
   string symbol     = ExtractStringValue(json, "symbol");
   double entryPrice = ExtractDoubleValue(json, "entryPrice");
   double stopLoss   = ExtractDoubleValue(json, "stopLoss");
   double takeProfit = ExtractDoubleValue(json, "targetPrice");
   double confidence = ExtractDoubleValue(json, "confidence");
   string signalId   = ExtractStringValue(json, "id");

   if(direction == "" || symbol == "") return;
   if(symbol == "" || symbol == "any") symbol = Symbol();

   Print("Processing signal: ", direction, " ", symbol,
         " Entry:", entryPrice, " SL:", stopLoss, " TP:", takeProfit,
         " Confidence:", confidence);

   if(CountOpenPositions() >= MaxOpenPositions)
   {
      Print("Max positions reached. Signal skipped.");
      return;
   }

   if(SymbolInfoInteger(symbol, SYMBOL_SPREAD) > MaxSpreadPoints)
   {
      Print("Spread too high. Signal skipped.");
      return;
   }

   double lots = CalculateLotSize(symbol, stopLoss, entryPrice, direction);

   bool success = false;
   if(direction == "BUY")
      success = trade.Buy(lots, symbol, 0, stopLoss, takeProfit, "GenX#" + signalId);
   else if(direction == "SELL")
      success = trade.Sell(lots, symbol, 0, stopLoss, takeProfit, "GenX#" + signalId);
   else if(direction == "CLOSE_ALL")
   {
      CloseAllPositions(symbol);
      return;
   }

   SendTradeConfirmation(signalId, success ? "executed" : "failed", trade.ResultRetcode());
}

//+------------------------------------------------------------------+
double CalculateLotSize(string symbol, double sl, double entry, string direction)
{
   if(RiskPercent <= 0 || sl <= 0) return NormalizeLots(symbol, DefaultLotSize);

   double balance    = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = balance * RiskPercent / 100.0;
   double tickValue  = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize   = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   double point      = SymbolInfoDouble(symbol, SYMBOL_POINT);

   double slPips = 0;
   if(direction == "BUY")  slPips = MathAbs(entry - sl) / point;
   else                    slPips = MathAbs(sl - entry) / point;

   if(slPips <= 0) return NormalizeLots(symbol, DefaultLotSize);

   double lots = riskAmount / (slPips * tickValue / tickSize);
   return NormalizeLots(symbol, lots);
}

//+------------------------------------------------------------------+
double NormalizeLots(string symbol, double lots)
{
   double minLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double maxLot  = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   double lotStep = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

   lots = MathMax(minLot, MathMin(maxLot, MathFloor(lots / lotStep) * lotStep));
   lots = MathMin(lots, MaxLotSize);
   return NormalizeDouble(lots, 2);
}

//+------------------------------------------------------------------+
int CountOpenPositions()
{
   int count = 0;
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(posInfo.SelectByIndex(i) && posInfo.Magic() == MagicNumber)
         count++;
   }
   return count;
}

//+------------------------------------------------------------------+
void CloseAllPositions(string symbol)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(posInfo.SelectByIndex(i) && posInfo.Magic() == MagicNumber)
      {
         if(symbol == "" || symbol == "any" || posInfo.Symbol() == symbol)
            trade.PositionClose(posInfo.Ticket());
      }
   }
}

//+------------------------------------------------------------------+
void SendTradeConfirmation(string signalId, string status, uint retcode)
{
   string body = "{\"connectionId\":\"" + connectionId + "\","
               + "\"originalSignal\":{\"id\":\"" + signalId + "\"},"
               + "\"status\":\"" + status + "\","
               + "\"retcode\":" + IntegerToString((int)retcode) + ","
               + "\"timestamp\":\"" + TimeToString(TimeLocal()) + "\"}";
   HttpPost(ServerURL + "/api/mt45/trade-confirmation", body);
}

//+------------------------------------------------------------------+
string HttpGet(string url)
{
   char   data[], result[];
   string headers = "";
   int    timeout = 5000;
   int    statusCode = WebRequest("GET", url, headers, timeout, data, result, headers);
   if(statusCode != 200) { if(DebugLog) Print("GET failed ", url, " code:", statusCode); return ""; }
   return CharArrayToString(result);
}

string HttpPost(string url, string body)
{
   uchar  data[], result[];
   string headers = "Content-Type: application/json\r\n";
   int    timeout = 5000;
   StringToCharArray(body, data, 0, StringLen(body));
   ArrayResize(data, ArraySize(data) - 1);
   string resHeaders = "";
   int    statusCode = WebRequest("POST", url, headers, timeout, data, result, resHeaders);
   if(statusCode != 200 && statusCode != 201)
   {
      if(DebugLog) Print("POST failed ", url, " code:", statusCode, " body:", body);
      return "";
   }
   return CharArrayToString(result);
}

//+------------------------------------------------------------------+
string ExtractStringValue(string json, string key)
{
   string search = "\"" + key + "\":\"";
   int start = StringFind(json, search);
   if(start < 0) return "";
   start += StringLen(search);
   int end = StringFind(json, "\"", start);
   if(end < 0) return "";
   return StringSubstr(json, start, end - start);
}

double ExtractDoubleValue(string json, string key)
{
   string search = "\"" + key + "\":";
   int start = StringFind(json, search);
   if(start < 0) return 0;
   start += StringLen(search);
   int end = start;
   while(end < StringLen(json))
   {
      string c = StringSubstr(json, end, 1);
      if(c == "," || c == "}") break;
      end++;
   }
   return StringToDouble(StringSubstr(json, start, end - start));
}

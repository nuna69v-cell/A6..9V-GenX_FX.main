//+------------------------------------------------------------------+
//|                                           MeltSignalExporter.mq5 |
//|                                           GenX FX Trading System |
//|                                         https://www.genx-fx.com/ |
//+------------------------------------------------------------------+
#property copyright "GenX FX Trading System"
#property link      "https://www.genx-fx.com/"
#property version   "1.00"

//--- Input parameters
input string   ExportFileName = "melt_signal.csv"; // Name of the export file
input int      ExportIntervalSeconds = 60;         // How often to export data (in seconds)

//--- Global variables
datetime lastExportTime = 0;
int fileHandle = INVALID_HANDLE;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   // Timer setup for periodic export
   EventSetTimer(1);
   Print("MeltSignalExporter EA Initialized. Exporting to: ", ExportFileName);
   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   EventKillTimer();
   if(fileHandle != INVALID_HANDLE)
     {
      FileClose(fileHandle);
     }
   Print("MeltSignalExporter EA Deinitialized.");
  }

//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
   datetime currentTime = TimeCurrent();

   // Check if it's time to export
   if(currentTime - lastExportTime >= ExportIntervalSeconds)
     {
      ExportSignalData();
      lastExportTime = currentTime;
     }
  }

//+------------------------------------------------------------------+
//| Export Signal Data Function                                      |
//+------------------------------------------------------------------+
void ExportSignalData()
  {
   // We open the file in read/write/share mode to allow the Python bridge to read it
   fileHandle = FileOpen(ExportFileName, FILE_WRITE|FILE_CSV|FILE_ANSI|FILE_COMMON);

   if(fileHandle == INVALID_HANDLE)
     {
      Print("Error opening file for export: ", GetLastError());
      return;
     }

   // Build the signal data payload.
   // Example format: Symbol,Time,Bid,Ask,SignalType,Action
   // For "Hot Melting Iron", let's simulate a basic breakout/trend signal

   string symbol = Symbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);

   // Placeholder logic for generating a signal type (e.g. BUY, SELL, HOLD)
   string action = "HOLD";
   double ma14 = iMA(symbol, PERIOD_CURRENT, 14, 0, MODE_SMA, PRICE_CLOSE);

   // Basic placeholder signal generation
   if(bid > ma14) action = "BUY";
   else if(ask < ma14) action = "SELL";

   // Format the row
   string row = StringFormat("%s,%s,%.5f,%.5f,%s",
                             symbol,
                             TimeToString(TimeCurrent(), TIME_DATE|TIME_MINUTES|TIME_SECONDS),
                             bid,
                             ask,
                             action);

   // Move to the end of the file to append, or just overwrite if keeping the file small is preferred.
   // Here we append:
   FileSeek(fileHandle, 0, SEEK_END);

   FileWrite(fileHandle, row);
   FileClose(fileHandle);

   Print("Signal exported: ", row);
  }
//+------------------------------------------------------------------+

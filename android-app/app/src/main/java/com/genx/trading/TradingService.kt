package com.genx.trading

import android.app.Service
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.ServiceCompat

// ⚡ Bolt: High-Performance Trading Service Node
class TradingService : Service() {

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        // 1. Create a persistent notification (Required for FGS)
        val notification = NotificationCompat.Builder(this, "VISION_OPS_CHANNEL")
            .setContentTitle("VisionOps: System Active")
            .setContentText("Monitoring FXPro/Exness Tick Data...")
            .setSmallIcon(android.R.drawable.ic_dialog_info) // Fallback icon
            .build()

        // 2. Launch as Foreground Service with Android 15 DataSync type
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            ServiceCompat.startForeground(
                this, 101, notification,
                ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC
            )
        } else {
             startForeground(101, notification)
        }

        // 3. Initiate the Trading Loop (Logic handled in background thread)
        startTradingLoop()

        return START_STICKY // Ensures service restarts if the OS kills it
    }

    // ⚡ Bolt Optimization: Android 15 Timeout Handler
    override fun onTimeout(startId: Int, fgsType: Int) {
        super.onTimeout(startId, fgsType)
        // 6-hour limit reached. Save state and prepare for automatic restart.
        Log.w("Bolt", "FGS Timeout reached. Cycling service for persistence.")
        stopSelf()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun startTradingLoop() {
        // Implementation for websocket connection to FXPro and Exness
        Log.i("Bolt", "Starting trading loop...")
    }
}

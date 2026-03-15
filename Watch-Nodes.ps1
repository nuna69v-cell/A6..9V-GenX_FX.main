# ⚡ Bolt: Parallel Node Monitor v2.0
$Nodes = @("192.168.1.10", "192.168.1.11", "node3.local", "node4.local", "node5.local")

Write-Host "🚀 Starting Parallel Node Watchdog..." -ForegroundColor Cyan

while ($true) {
    $Results = $Nodes | ForEach-Object -Parallel {
        $Ping = Test-Connection -ComputerName $_ -Count 1 -ErrorAction SilentlyContinue
        if ($Ping) {
            [PSCustomObject]@{
                Node     = $_
                Status   = "ONLINE 🟢"
                Latency  = "$($Ping.Latency)ms"
                Priority = if ($Ping.Latency -gt 100) { "WARNING ⚠️" } else { "OPTIMAL ⚡" }
            }
        } else {
            [PSCustomObject]@{
                Node     = $_
                Status   = "OFFLINE 🔴"
                Latency  = "N/A"
                Priority = "CRITICAL 🔥"
            }
        }
    } -ThrottleLimit 5

    Clear-Host
    $Results | Format-Table -AutoSize

    # ⚡ Bolt Optimization: Sleep for 2 seconds to save CPU cycles
    Start-Sleep -Seconds 2
}

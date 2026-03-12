import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { queryClient } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "@/hooks/use-toast";
import {
  RefreshCw,
  Send,
  Shield,
  TrendingUp,
  Wifi,
  WifiOff,
  ChevronDown,
  ChevronUp,
  AlertTriangle,
  DollarSign,
  BarChart2,
  Layers,
  Activity,
  ExternalLink,
  Copy,
  CheckCheck
} from "lucide-react";

interface BrokerAccount {
  id: string;
  broker: string;
  server: string;
  accountId: string;
  label: string;
  color: string;
}

const ACCOUNTS: BrokerAccount[] = [
  {
    id: "exness",
    broker: "Exness",
    server: "Exness-MT5Real24",
    accountId: "169926536",
    label: "Exness MT5 Real",
    color: "emerald",
  },
  {
    id: "fxpro",
    broker: "FxPro",
    server: "FxPro-MT5 Live02",
    accountId: "530142568",
    label: "FxPro MT5 Live",
    color: "blue",
  },
];

// Exness live account data from API logs
const EXNESS_LIVE = {
  leverage: 2000,
  tradeEnabled: true,
  symbols: ["XAUUSDm","EURUSDm","USDJPYm","GBPCHFm","XAGUSDm","BTCXAUm","ETHUSDm","USDCADm","NVDAm","US30m","UK100m","XAUEURm"],
};

function useEAConnections() {
  return useQuery<{ connections: any[] }>({
    queryKey: ["/api/mt45/connections"],
    refetchInterval: 8000,
  });
}

function useBroadcastSignal() {
  return useMutation({
    mutationFn: async (signal: any) => {
      const res = await fetch("/api/mt45/broadcast-signal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ signal }),
      });
      return res.json();
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["/api/mt45/connections"] });
      toast({ title: "Signal Broadcast", description: data.message || "Signal queued" });
    },
    onError: () => toast({ title: "Broadcast Failed", variant: "destructive" }),
  });
}

function useTestSignal() {
  return useMutation({
    mutationFn: async () => {
      const res = await fetch("/api/mt45/test-signal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      return res.json();
    },
    onSuccess: (data) => {
      toast({ title: "Test Signal Sent", description: data.message || `Sent to ${data.sentCount} EAs` });
    },
  });
}

function cls(color: string) {
  if (color === "emerald") return {
    bg: "bg-emerald-500/10 border-emerald-500/20",
    text: "text-emerald-400",
    badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    dot: "bg-emerald-500",
  };
  return {
    bg: "bg-blue-500/10 border-blue-500/20",
    text: "text-blue-400",
    badge: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    dot: "bg-blue-500",
  };
}

export function BrokerAccounts() {
  const { data: connectionsData, isLoading, refetch } = useEAConnections();
  const { mutate: broadcastSignal, isPending: broadcastPending } = useBroadcastSignal();
  const { mutate: testSignal, isPending: testPending } = useTestSignal();
  const [expandedBroker, setExpandedBroker] = useState<string | null>("fxpro");
  const [copied, setCopied] = useState(false);

  const serverUrl = window.location.origin;
  const copyServerUrl = () => {
    navigator.clipboard.writeText(serverUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      toast({ title: "Server URL Copied", description: serverUrl });
    });
  };
  const [showSignalForm, setShowSignalForm] = useState(false);
  const [signal, setSignal] = useState({
    signal: "BUY",
    symbol: "XAUUSDm",
    entryPrice: "",
    stopLoss: "",
    targetPrice: "",
    confidence: 0.8,
  });

  const connections = connectionsData?.connections || [];

  const getConn = (accountId: string) =>
    connections.find((c) => c.accountNumber === accountId);

  const totalActive = connections.filter((c) => c.isActive).length;

  const handleBroadcast = () => {
    broadcastSignal({
      ...signal,
      entryPrice: parseFloat(signal.entryPrice) || 0,
      stopLoss: parseFloat(signal.stopLoss) || 0,
      targetPrice: parseFloat(signal.targetPrice) || 0,
    });
  };

  return (
    <div className="glass-panel rounded-2xl p-6 space-y-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">Broker Accounts</h2>
          <p className="text-sm text-muted-foreground mt-0.5">Live MT5 connections</p>
        </div>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => refetch()}
          className="text-muted-foreground hover:text-foreground border border-border/40 h-8 px-2"
          data-testid="button-refresh-connections"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? "animate-spin" : ""}`} />
        </Button>
      </div>

      {/* Security notice */}
      <div className="flex gap-2 p-3 rounded-xl bg-yellow-500/5 border border-yellow-500/20 text-xs text-yellow-400">
        <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
        <span>Change your MT5 passwords immediately if shared publicly. These are live accounts.</span>
      </div>

      {/* Summary bar */}
      <div className="grid grid-cols-3 gap-2 text-xs">
        <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40 text-center">
          <div className="text-muted-foreground mb-1">Accounts</div>
          <div className="font-mono font-semibold">{ACCOUNTS.length}</div>
        </div>
        <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40 text-center">
          <div className="text-muted-foreground mb-1">Connected</div>
          <div className={`font-mono font-semibold ${totalActive > 0 ? "text-emerald-400" : "text-muted-foreground"}`}>
            {totalActive}
          </div>
        </div>
        <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40 text-center">
          <div className="text-muted-foreground mb-1">Signals</div>
          <div className="font-mono font-semibold text-primary">Live</div>
        </div>
      </div>

      {/* Broker Cards */}
      <div className="space-y-2.5">
        {ACCOUNTS.map((account) => {
          const c = cls(account.color);
          const conn = getConn(account.accountId);
          const isConnected = conn?.isActive ?? false;
          const isExpanded = expandedBroker === account.id;
          const isExness = account.id === "exness";

          return (
            <div
              key={account.id}
              className="rounded-xl border border-border/50 overflow-hidden"
              data-testid={`card-broker-${account.id}`}
            >
              {/* Header row */}
              <button
                className="w-full flex items-center justify-between p-3.5 bg-secondary/20 hover:bg-secondary/30 transition-colors text-left"
                onClick={() => setExpandedBroker(isExpanded ? null : account.id)}
                data-testid={`button-expand-${account.id}`}
              >
                <div className="flex items-center gap-3">
                  <div className={`p-1.5 rounded-lg border ${c.bg}`}>
                    <TrendingUp className={`w-4 h-4 ${c.text}`} />
                  </div>
                  <div>
                    <div className="font-semibold text-sm">{account.label}</div>
                    <div className="text-xs text-muted-foreground font-mono">{account.accountId}</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded-full border text-xs font-mono flex items-center gap-1.5 ${
                    isConnected ? c.badge : "bg-muted/20 text-muted-foreground border-muted/30"
                  }`}>
                    {isConnected
                      ? <><Wifi className="w-3 h-3" />LIVE</>
                      : <><WifiOff className="w-3 h-3" />OFFLINE</>
                    }
                  </span>
                  {isExpanded
                    ? <ChevronUp className="w-3.5 h-3.5 text-muted-foreground" />
                    : <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
                  }
                </div>
              </button>

              {/* Expanded details */}
              {isExpanded && (
                <div className="p-4 border-t border-border/40 bg-secondary/10 space-y-3">
                  {/* Live stats grid */}
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40">
                      <div className="flex items-center gap-1.5 text-muted-foreground mb-1">
                        <DollarSign className="w-3 h-3" />
                        <span className="uppercase tracking-wider">Balance</span>
                      </div>
                      <div className="font-mono font-semibold text-sm" data-testid={`text-balance-${account.id}`}>
                        {conn?.balance != null
                          ? `$${Number(conn.balance).toFixed(2)}`
                          : isExness ? "$20.00" : "--"}
                      </div>
                    </div>

                    <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40">
                      <div className="flex items-center gap-1.5 text-muted-foreground mb-1">
                        <BarChart2 className="w-3 h-3" />
                        <span className="uppercase tracking-wider">Leverage</span>
                      </div>
                      <div className="font-mono font-semibold text-sm" data-testid={`text-leverage-${account.id}`}>
                        {conn?.leverage ? `1:${conn.leverage}` : isExness ? "1:2000" : "1:500"}
                      </div>
                    </div>

                    <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40">
                      <div className="flex items-center gap-1.5 text-muted-foreground mb-1">
                        <Activity className="w-3 h-3" />
                        <span className="uppercase tracking-wider">Positions</span>
                      </div>
                      <div className="font-mono font-semibold text-sm" data-testid={`text-positions-${account.id}`}>
                        {conn?.openPositions ?? (isExness ? "0" : "--")}
                      </div>
                    </div>

                    <div className="bg-secondary/30 rounded-lg p-2.5 border border-border/40">
                      <div className="flex items-center gap-1.5 text-muted-foreground mb-1">
                        <Layers className="w-3 h-3" />
                        <span className="uppercase tracking-wider">Server</span>
                      </div>
                      <div className="font-mono text-[10px] text-foreground/80 leading-tight" data-testid={`text-server-${account.id}`}>
                        {account.server}
                      </div>
                    </div>
                  </div>

                  {/* Exness: show available symbols */}
                  {isExness && (
                    <div className="space-y-1.5">
                      <div className="text-xs text-muted-foreground uppercase tracking-wider">Subscribed Symbols</div>
                      <div className="flex flex-wrap gap-1">
                        {EXNESS_LIVE.symbols.map((sym) => (
                          <span
                            key={sym}
                            className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-mono"
                          >
                            {sym}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Trade enabled badge */}
                  {isExness && (
                    <div className="flex items-center gap-2 text-xs">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                      <span className="text-emerald-400 font-medium">Trade Enabled · Real Account</span>
                    </div>
                  )}

                  {/* FxPro connection options */}
                  {!isExness && (
                    <div className="space-y-2.5">
                      {/* FxPro Edge direct link */}
                      <a
                        href="https://edge.fxpro.group/"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-between w-full p-3 rounded-lg bg-blue-500/10 border border-blue-500/30 hover:bg-blue-500/20 transition-colors"
                        data-testid="link-fxpro-edge"
                      >
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 rounded bg-blue-600 flex items-center justify-center text-[10px] font-bold text-white">FX</div>
                          <div>
                            <div className="text-xs font-semibold text-blue-400">Open FxPro Edge</div>
                            <div className="text-[10px] text-blue-400/60">edge.fxpro.group</div>
                          </div>
                        </div>
                        <ExternalLink className="w-3.5 h-3.5 text-blue-400" />
                      </a>

                      {/* Server URL to copy for MT5 EA config */}
                      <div className="p-3 rounded-lg bg-secondary/20 border border-border/40 space-y-2">
                        <div className="text-[10px] text-muted-foreground uppercase tracking-wider font-medium">
                          Connect via MT5 EA — copy your server URL
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="flex-1 bg-secondary/40 rounded px-2 py-1.5 font-mono text-[10px] text-foreground/80 truncate border border-border/30">
                            {serverUrl}
                          </div>
                          <button
                            onClick={copyServerUrl}
                            className="shrink-0 p-1.5 rounded-md bg-primary/10 hover:bg-primary/20 border border-primary/20 text-primary transition-colors"
                            data-testid="button-copy-server-url"
                          >
                            {copied ? <CheckCheck className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                          </button>
                        </div>
                        <div className="text-[10px] text-muted-foreground leading-relaxed">
                          1. Open FxPro MT5 → Tools → Options → Expert Advisors<br />
                          2. Allow WebRequest for the URL above<br />
                          3. Attach <span className="font-mono text-foreground">GenX_FxPro_MT5.mq5</span> to any chart
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Signal broadcast toggle */}
      <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border/40 pt-4">
        <span className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${totalActive > 0 ? "bg-emerald-500 animate-pulse" : "bg-muted-foreground"}`} />
          {totalActive > 0 ? `${totalActive} EA active` : "No EAs connected"}
        </span>
        <button
          onClick={() => setShowSignalForm(!showSignalForm)}
          className="flex items-center gap-1 text-primary hover:text-primary/80 transition-colors font-medium"
          data-testid="button-toggle-signal-form"
        >
          <Send className="w-3.5 h-3.5" />
          {showSignalForm ? "Hide" : "Broadcast Signal"}
        </button>
      </div>

      {/* Signal Broadcast Panel */}
      {showSignalForm && (
        <div className="border border-border/50 rounded-xl p-4 space-y-3 bg-secondary/10">
          <div className="text-sm font-medium">Broadcast Trading Signal</div>

          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <Label className="text-xs text-muted-foreground uppercase tracking-wider">Direction</Label>
              <div className="flex gap-2">
                {["BUY", "SELL"].map((dir) => (
                  <button
                    key={dir}
                    onClick={() => setSignal({ ...signal, signal: dir })}
                    className={`flex-1 py-1.5 rounded-lg text-xs font-mono font-bold border transition-colors ${
                      signal.signal === dir
                        ? dir === "BUY"
                          ? "bg-emerald-500/20 border-emerald-500/50 text-emerald-400"
                          : "bg-red-500/20 border-red-500/50 text-red-400"
                        : "bg-secondary/30 border-border/40 text-muted-foreground"
                    }`}
                    data-testid={`button-signal-${dir.toLowerCase()}`}
                  >
                    {dir}
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs text-muted-foreground uppercase tracking-wider">Symbol</Label>
              <select
                value={signal.symbol}
                onChange={(e) => setSignal({ ...signal, symbol: e.target.value })}
                className="w-full h-8 rounded-md bg-secondary/20 border border-border/50 text-sm font-mono px-2 text-foreground"
                data-testid="select-signal-symbol"
              >
                {EXNESS_LIVE.symbols.map((sym) => (
                  <option key={sym} value={sym}>{sym}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2">
            {[
              { label: "Entry", key: "entryPrice", id: "entry" },
              { label: "Stop Loss", key: "stopLoss", id: "sl" },
              { label: "Take Profit", key: "targetPrice", id: "tp" },
            ].map(({ label, key, id }) => (
              <div key={key} className="space-y-1.5">
                <Label className="text-xs text-muted-foreground uppercase tracking-wider">{label}</Label>
                <Input
                  value={(signal as any)[key]}
                  onChange={(e) => setSignal({ ...signal, [key]: e.target.value })}
                  placeholder="0.00"
                  className="bg-secondary/20 border-border/50 font-mono text-sm h-8"
                  data-testid={`input-signal-${id}`}
                />
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handleBroadcast}
              disabled={broadcastPending}
              size="sm"
              className="flex-1 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20"
              data-testid="button-broadcast-signal"
            >
              <Send className="w-3.5 h-3.5 mr-1.5" />
              {broadcastPending ? "Sending..." : "Broadcast to All EAs"}
            </Button>
            <Button
              onClick={() => testSignal()}
              disabled={testPending}
              size="sm"
              variant="ghost"
              className="border border-border/40 text-muted-foreground"
              data-testid="button-test-signal"
            >
              {testPending ? "..." : "Test"}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

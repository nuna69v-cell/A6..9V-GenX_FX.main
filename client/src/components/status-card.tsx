import { useBotStatus, useRunJob } from "@/hooks/use-config";
import { Button } from "@/components/ui/button";
import { 
  Play, 
  Clock, 
  Server, 
  CheckCircle2, 
  AlertCircle 
} from "lucide-react";
import { format } from "date-fns";
import { toast } from "@/hooks/use-toast";

export function StatusCard() {
  const { data: status, isLoading, refetch } = useBotStatus();
  const { mutate: runJob, isPending: isRunning } = useRunJob();

  const handleRunJob = () => {
    runJob(undefined, {
      onSuccess: () => {
        toast({
          title: "Job Started",
          description: "The trading bot job has been triggered successfully.",
        });
        refetch();
      },
      onError: (error) => {
        toast({
          title: "Job Failed",
          description: error.message,
          variant: "destructive",
        });
      },
    });
  };

  if (isLoading) {
    return (
      <div className="h-[200px] w-full rounded-2xl bg-card/50 animate-pulse border border-border/40" />
    );
  }

  return (
    <div className="glass-panel rounded-2xl p-6 relative overflow-hidden group">
      {/* Decorative gradient background */}
      <div className="absolute top-0 right-0 w-[300px] h-[300px] bg-primary/5 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2" />

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-lg font-semibold tracking-tight">System Status</h2>
            <p className="text-sm text-muted-foreground mt-1">Current operational metrics</p>
          </div>
          <div className={`px-3 py-1 rounded-full border text-xs font-mono flex items-center gap-2 ${
            status?.isRunning 
              ? "bg-green-500/10 border-green-500/20 text-green-500" 
              : "bg-yellow-500/10 border-yellow-500/20 text-yellow-500"
          }`}>
            <span className={`w-2 h-2 rounded-full ${status?.isRunning ? "bg-green-500 animate-pulse" : "bg-yellow-500"}`} />
            {status?.isRunning ? "ACTIVE" : "IDLE"}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-secondary/30 rounded-xl p-4 border border-border/50">
            <div className="flex items-center gap-2 text-muted-foreground mb-2">
              <Clock className="w-4 h-4" />
              <span className="text-xs font-medium uppercase tracking-wider">Last Execution</span>
            </div>
            <div className="text-lg font-mono font-medium">
              {status?.lastRun ? format(new Date(status.lastRun), "HH:mm:ss") : "--:--:--"}
              <span className="text-xs text-muted-foreground ml-2">
                 {status?.lastRun ? format(new Date(status.lastRun), "MMM dd") : ""}
              </span>
            </div>
          </div>

          <div className="bg-secondary/30 rounded-xl p-4 border border-border/50">
            <div className="flex items-center gap-2 text-muted-foreground mb-2">
              <Server className="w-4 h-4" />
              <span className="text-xs font-medium uppercase tracking-wider">Next Scheduled</span>
            </div>
            <div className="text-lg font-mono font-medium">
              {status?.nextJob || "Not scheduled"}
            </div>
          </div>
        </div>

        <Button 
          onClick={handleRunJob}
          disabled={isRunning}
          className="w-full bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 hover:border-primary/50 shadow-lg shadow-primary/5 transition-all duration-300"
        >
          {isRunning ? (
            <>
              <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin mr-2" />
              Initializing Pipeline...
            </>
          ) : (
            <>
              <Play className="w-4 h-4 mr-2" />
              Trigger Job Manually
            </>
          )}
        </Button>
      </div>
    </div>
  );
}

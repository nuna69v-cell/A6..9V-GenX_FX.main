import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Video } from "lucide-react";

export function BigoLiveRoom() {
  return (
    <Card className="col-span-1 border-muted/50 bg-background/50 backdrop-blur-sm shadow-sm overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between pb-2 bg-gradient-to-r from-background to-secondary/20">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <div className="p-1.5 bg-primary/10 rounded-md">
            <Video className="w-4 h-4 text-primary" />
          </div>
          Live Trading Room
        </CardTitle>
        <div className="flex items-center space-x-2 bg-red-500/10 px-2.5 py-1 rounded-full border border-red-500/20">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
          </span>
          <span className="text-[10px] font-bold tracking-wider text-red-500">LIVE</span>
        </div>
      </CardHeader>
      <CardContent className="pt-4 space-y-4">
        <div className="flex justify-between items-start text-sm">
          <div className="space-y-1">
            <p className="font-medium text-foreground">ExnessMT5Real24</p>
            <p className="text-muted-foreground text-xs flex items-center gap-1.5">
              <span className="bg-secondary px-1.5 py-0.5 rounded text-[10px] font-mono border border-border/50">BIGO LIVE</span>
              <span>ID: 1110941575</span>
            </p>
          </div>
        </div>

        <div className="aspect-video w-full rounded-lg overflow-hidden bg-black/5 flex items-center justify-center relative border border-border group">
          <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10 bg-background/80 backdrop-blur-sm">
             <Video className="w-10 h-10 text-muted-foreground mb-3 opacity-50" />
             <p className="text-sm font-medium">BIGO LIVE Broadcast</p>
             <p className="text-xs text-muted-foreground mt-1 max-w-[80%]">Watch live trading sessions and real-time analysis</p>
             <a
                href="https://www.bigo.tv/user/ExnessMT5Real24?sc=HmDkE7"
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 px-4 py-2 bg-primary text-primary-foreground text-xs font-medium rounded-md hover:bg-primary/90 transition-colors shadow-sm w-full max-w-[140px]"
              >
                Watch Now
              </a>
          </div>
        </div>

        <div className="pt-2 flex justify-between items-center border-t border-border/50">
          <a
            href="https://www.bigo.tv/user/ExnessMT5Real24?sc=HmDkE7"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-muted-foreground hover:text-primary transition-colors flex items-center gap-1"
          >
            Open in BIGO App
          </a>
          <span className="text-[10px] text-muted-foreground">feedback@bigo.tv</span>
        </div>
      </CardContent>
    </Card>
  );
}

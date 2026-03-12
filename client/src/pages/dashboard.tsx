import { Layout } from "@/components/layout";
import { ConfigForm } from "@/components/config-form";
import { StatusCard } from "@/components/status-card";
import { ActivityChart } from "@/components/activity-chart";
import { BrokerAccounts } from "@/components/broker-accounts";
import { motion } from "framer-motion";

export default function Dashboard() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 15
      }
    }
  };

  return (
    <Layout>
      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-6"
      >
        {/* Page Header */}
        <motion.div variants={itemVariants} className="flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight mb-2">Dashboard</h1>
            <p className="text-muted-foreground">
              Monitor and control your GenX FX trading bot — dual broker setup.
            </p>
          </div>
          <div className="flex gap-3">
            <span className="px-3 py-1 rounded-full bg-secondary/50 border border-border/50 text-xs font-mono text-muted-foreground flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              Node: Singapore-1
            </span>
            <span className="px-3 py-1 rounded-full bg-secondary/50 border border-border/50 text-xs font-mono text-muted-foreground flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span>
              2 Brokers
            </span>
          </div>
        </motion.div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column - Chart + Config */}
          <motion.div variants={itemVariants} className="lg:col-span-2 space-y-6">
            <ActivityChart />
            <ConfigForm />
          </motion.div>

          {/* Right column - Status + Brokers */}
          <motion.div variants={itemVariants} className="space-y-6">
            <StatusCard />
            <BrokerAccounts />
          </motion.div>
        </div>
      </motion.div>
    </Layout>
  );
}

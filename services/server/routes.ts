import { Express } from 'express';
import { db } from './db.js';
import { users, tradingAccounts, positions, notifications, educationalResources, botConfig, botConfigInsertSchema } from '@shared/schema';
import { eq, desc, and, or, ilike, count } from 'drizzle-orm';
import { spawn } from 'child_process';
import * as fs from 'fs';

/**
 * Registers all the API routes for the application.
 * @param {Express} app - The Express application instance.
 */
export function registerRoutes(app: Express) {

  // Test route
  app.get('/api/test', async (req, res) => {
    try {
      res.json({ 
        message: 'API is working!', 
        timestamp: new Date().toISOString(),
        database: 'Connected'
      });
    } catch (error) {
      console.error('Test route error:', error);
      res.status(500).json({ error: 'Test route failed' });
    }
  });

  // Database health check
  app.get('/api/db-health', async (req, res) => {
    try {
      const result = await db.select({ count: count() }).from(users);
      res.json({ 
        status: 'healthy', 
        userCount: result[0].count,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Database health check failed:', error);
      res.status(500).json({ error: 'Database connection failed' });
    }
  });

  // Comprehensive health check
  app.get('/api/health', async (req, res) => {
    try {
      const checks = {
        database: 'unknown',
        python_service: 'unknown',
        websocket: 'active',
        memory: process.memoryUsage(),
        uptime: process.uptime()
      };

      // Test database connection
      try {
        await db.select().from(users).limit(1);
        checks.database = 'connected';
      } catch (dbError) {
        checks.database = 'disconnected';
      }

      // Check Python service (if applicable)
      try {
        // This would be where you'd ping your Python service
        checks.python_service = 'available';
      } catch (pyError) {
        checks.python_service = 'unavailable';
      }

      const isHealthy = checks.database === 'connected';

      res.status(isHealthy ? 200 : 503).json({
        status: isHealthy ? 'healthy' : 'degraded',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development',
        version: '1.0.0',
        checks
      });
    } catch (error) {
      console.error('Health check failed:', error);
      res.status(503).json({
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error.message
      });
    }
  });

  // Educational Resources Routes
  app.get('/api/educational-resources', async (req, res) => {
    try {
      const { page = '1', limit = '10', search = '', skillLevel, category } = req.query;
      const offset = (parseInt(page as string) - 1) * parseInt(limit as string);

      const whereConditions = [];

      if (search) {
        whereConditions.push(
          or(
            ilike(educationalResources.title, `%${search}%`),
            ilike(educationalResources.description, `%${search}%`)
          )
        );
      }

      if (skillLevel) {
        whereConditions.push(eq(educationalResources.skillLevel, skillLevel as string));
      }

      if (category) {
        whereConditions.push(eq(educationalResources.category, category as string));
      }

      const resources = await db
        .select()
        .from(educationalResources)
        .where(whereConditions.length > 0 ? and(...whereConditions) : undefined)
        .orderBy(desc(educationalResources.createdAt))
        .limit(parseInt(limit as string))
        .offset(offset);

      const totalCount = await db
        .select({ count: count() })
        .from(educationalResources)
        .where(whereConditions.length > 0 ? and(...whereConditions) : undefined);

      res.json({
        resources,
        pagination: {
          page: parseInt(page as string),
          limit: parseInt(limit as string),
          total: totalCount[0].count,
          totalPages: Math.ceil(totalCount[0].count / parseInt(limit as string))
        }
      });
    } catch (error) {
      console.error('Error fetching educational resources:', error);
      res.status(500).json({ error: 'Failed to fetch educational resources' });
    }
  });

  // Seed known broker accounts on startup
  (async () => {
    try {
      const existing = await db.select().from(tradingAccounts);
      if (existing.length === 0) {
        await db.insert(tradingAccounts).values([
          {
            accountName: 'Exness MT5 Real',
            broker: 'exness',
            accountId: '169926536',
            platform: 'MT5',
            balance: '20.00',
            currency: 'USD',
            isActive: true,
          },
          {
            accountName: 'FxPro MT5 Live',
            broker: 'fxpro',
            accountId: '530142568',
            platform: 'MT5',
            balance: '0.00',
            currency: 'USD',
            isActive: true,
          },
        ]);
        console.log('Seeded broker accounts (Exness + FxPro)');
      }
    } catch (e) {
      console.error('Failed to seed broker accounts:', e);
    }
  })();

  // Trading accounts routes
  app.get('/api/trading-accounts', async (req, res) => {
    try {
      const accounts = await db
        .select()
        .from(tradingAccounts)
        .orderBy(desc(tradingAccounts.createdAt));

      res.json({ accounts });
    } catch (error) {
      console.error('Error fetching trading accounts:', error);
      res.status(500).json({ error: 'Failed to fetch trading accounts' });
    }
  });

  // Update trading account balance
  app.patch('/api/trading-accounts/:id', async (req, res) => {
    try {
      const { id } = req.params;
      const { balance, isActive } = req.body;
      const [updated] = await db.update(tradingAccounts)
        .set({ balance: balance?.toString(), isActive })
        .where(eq(tradingAccounts.id, parseInt(id)))
        .returning();
      res.json(updated);
    } catch (error) {
      console.error('Error updating trading account:', error);
      res.status(500).json({ error: 'Failed to update account' });
    }
  });

  // Positions routes
  app.get('/api/positions', async (req, res) => {
    try {
      const activePositions = await db
        .select()
        .from(positions)
        .where(eq(positions.status, 'open'))
        .orderBy(desc(positions.openTime));

      res.json({ positions: activePositions });
    } catch (error) {
      console.error('Error fetching positions:', error);
      res.status(500).json({ error: 'Failed to fetch positions' });
    }
  });

  // Notifications routes
  app.get('/api/notifications', async (req, res) => {
    try {
      const recentNotifications = await db
        .select()
        .from(notifications)
        .orderBy(desc(notifications.createdAt))
        .limit(50);

      res.json({ notifications: recentNotifications });
    } catch (error) {
      console.error('Error fetching notifications:', error);
      res.status(500).json({ error: 'Failed to fetch notifications' });
    }
  });

  // System stats
  app.get('/api/stats', async (req, res) => {
    try {
      const [usersCount, accountsCount, positionsCount, notificationsCount] = await Promise.all([
        db.select({ count: count() }).from(users),
        db.select({ count: count() }).from(tradingAccounts),
        db.select({ count: count() }).from(positions).where(eq(positions.status, 'open')),
        db.select({ count: count() }).from(notifications)
      ]);

      res.json({
        users: usersCount[0].count,
        tradingAccounts: accountsCount[0].count,
        activePositions: positionsCount[0].count,
        notifications: notificationsCount[0].count,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      res.status(500).json({ error: 'Failed to fetch stats' });
    }
  });

  // MT4/5 EA Connection Management
  const eaConnections = new Map();
  const pendingSignals = new Map();

  // Auto-register known accounts on startup so dashboard always shows them
  eaConnections.set('exness_169926536_live', {
    eaName: 'GenX-Exness-Live',
    connectionId: 'exness_169926536_live',
    accountNumber: '169926536',
    symbol: 'XAUUSDm',
    timeframe: 'H1',
    broker: 'exness',
    server: 'Exness-MT5Real24',
    status: 'registered',
    balance: 20,
    equity: 20,
    openPositions: 0,
    leverage: 2000,
    tradeEnabled: true,
    lastHeartbeat: new Date(),
    connectedAt: new Date()
  });
  eaConnections.set('fxpro_530142568_live', {
    eaName: 'GenX-FxPro-Live',
    connectionId: 'fxpro_530142568_live',
    accountNumber: '530142568',
    symbol: 'XAUUSD',
    timeframe: 'H1',
    broker: 'fxpro',
    server: 'FxPro-MT5 Live02',
    status: 'registered',
    balance: null,
    equity: null,
    openPositions: 0,
    leverage: 500,
    tradeEnabled: false,
    lastHeartbeat: new Date(Date.now() - 120000), // 2 min ago = offline
    connectedAt: new Date()
  });

  // Register EA connection
  app.post('/api/mt45/register', async (req, res) => {
    try {
      const { eaName, connectionId, accountNumber, symbol, timeframe } = req.body;

      eaConnections.set(connectionId, {
        eaName,
        connectionId,
        accountNumber,
        symbol,
        timeframe,
        status: 'connected',
        lastHeartbeat: new Date(),
        connectedAt: new Date()
      });

      console.log(`EA registered: ${eaName} (${connectionId})`);

      res.json({ 
        success: true, 
        message: 'EA registered successfully',
        connectionId 
      });
    } catch (error) {
      console.error('Error registering EA:', error);
      res.status(500).json({ error: 'Failed to register EA' });
    }
  });

  // Unregister EA connection
  app.post('/api/mt45/unregister', async (req, res) => {
    try {
      const { connectionId } = req.body;

      if (eaConnections.has(connectionId)) {
        eaConnections.delete(connectionId);
        pendingSignals.delete(connectionId);
        console.log(`EA unregistered: ${connectionId}`);
      }

      res.json({ success: true, message: 'EA unregistered successfully' });
    } catch (error) {
      console.error('Error unregistering EA:', error);
      res.status(500).json({ error: 'Failed to unregister EA' });
    }
  });

  // EA heartbeat
  app.post('/api/mt45/heartbeat', async (req, res) => {
    try {
      const { connectionId, status, balance, equity } = req.body;

      if (eaConnections.has(connectionId)) {
        const connection = eaConnections.get(connectionId);
        connection.lastHeartbeat = new Date();
        connection.status = status;
        connection.balance = balance;
        connection.equity = equity;
        eaConnections.set(connectionId, connection);
      }

      res.json({ success: true });
    } catch (error) {
      console.error('Error processing heartbeat:', error);
      res.status(500).json({ error: 'Failed to process heartbeat' });
    }
  });

  // Get signals for specific EA
  app.get('/api/mt45/signals/:connectionId', async (req, res) => {
    try {
      const { connectionId } = req.params;

      const signals = pendingSignals.get(connectionId) || [];

      // Clear signals after sending
      pendingSignals.set(connectionId, []);

      res.json({ signals });
    } catch (error) {
      console.error('Error fetching signals:', error);
      res.status(500).json({ error: 'Failed to fetch signals' });
    }
  });

  // Send signal to EA
  app.post('/api/mt45/send-signal', async (req, res) => {
    try {
      const { connectionId, signal } = req.body;

      if (!eaConnections.has(connectionId)) {
        return res.status(404).json({ error: 'EA connection not found' });
      }

      const currentSignals = pendingSignals.get(connectionId) || [];
      currentSignals.push({
        ...signal,
        id: Date.now(),
        timestamp: new Date().toISOString()
      });
      pendingSignals.set(connectionId, currentSignals);

      res.json({ success: true, message: 'Signal queued for EA' });
    } catch (error) {
      console.error('Error sending signal:', error);
      res.status(500).json({ error: 'Failed to send signal' });
    }
  });

  // Trade confirmation from EA
  app.post('/api/mt45/trade-confirmation', async (req, res) => {
    try {
      const { connectionId, originalSignal, status, timestamp } = req.body;

      console.log(`Trade confirmation from ${connectionId}: ${status}`);

      // Here you could store trade confirmations in database
      // await db.insert(tradeConfirmations).values({...});

      res.json({ success: true });
    } catch (error) {
      console.error('Error processing trade confirmation:', error);
      res.status(500).json({ error: 'Failed to process confirmation' });
    }
  });

  // Get all EA connections status
  app.get('/api/mt45/connections', async (req, res) => {
    try {
      const connections = Array.from(eaConnections.values()).map(conn => ({
        ...conn,
        isActive: (new Date().getTime() - new Date(conn.lastHeartbeat).getTime()) < 60000 // Active if heartbeat within 1 minute
      }));

      res.json({ connections });
    } catch (error) {
      console.error('Error fetching connections:', error);
      res.status(500).json({ error: 'Failed to fetch connections' });
    }
  });

  // Broadcast signal to all connected EAs
  app.post('/api/mt45/broadcast-signal', async (req, res) => {
    try {
      const { signal } = req.body;
      let sentCount = 0;

      for (const [connectionId, connection] of eaConnections.entries()) {
        // Only send to active connections
        const isActive = (new Date().getTime() - new Date(connection.lastHeartbeat).getTime()) < 60000;

        if (isActive && signal.symbol === connection.symbol) {
          const currentSignals = pendingSignals.get(connectionId) || [];
          currentSignals.push({
            ...signal,
            id: Date.now(),
            timestamp: new Date().toISOString()
          });
          pendingSignals.set(connectionId, currentSignals);
          sentCount++;
        }
      }

      res.json({ 
        success: true, 
        message: `Signal broadcasted to ${sentCount} EAs`,
        sentCount 
      });
    } catch (error) {
      console.error('Error broadcasting signal:', error);
      res.status(500).json({ error: 'Failed to broadcast signal' });
    }
  });

  // Test signal endpoint for development
  app.post('/api/mt45/test-signal', async (req, res) => {
    try {
      const testSignal = {
        signal: 'BUY',
        symbol: 'EURUSD',
        entryPrice: 1.1000,
        stopLoss: 1.0950,
        targetPrice: 1.1050,
        confidence: 0.85,
        reasoning: 'Test signal from GenZ Trading Platform'
      };

      let sentCount = 0;
      for (const [connectionId, connection] of eaConnections.entries()) {
        const isActive = (new Date().getTime() - new Date(connection.lastHeartbeat).getTime()) < 60000;

        if (isActive) {
          const currentSignals = pendingSignals.get(connectionId) || [];
          currentSignals.push({
            ...testSignal,
            id: Date.now(),
            timestamp: new Date().toISOString()
          });
          pendingSignals.set(connectionId, currentSignals);
          sentCount++;
        }
      }

      res.json({ 
        success: true, 
        message: `Test signal sent to ${sentCount} connected EAs`,
        signal: testSignal,
        sentCount 
      });
    } catch (error) {
      console.error('Error sending test signal:', error);
      res.status(500).json({ error: 'Failed to send test signal' });
    }
  });

  // ============ BOT CONFIG ROUTES ============

  // Get bot configuration
  app.get('/api/config', async (req, res) => {
    try {
      const configs = await db.select().from(botConfig).limit(1);
      if (configs.length === 0) {
        const [newConfig] = await db.insert(botConfig).values({
          symbols: ['BTCUSDT', 'ETHUSDT', 'EURUSD'],
          marketOpen: '09:00',
          marketClose: '17:00',
          intervalMinutes: 30,
          isEnabled: true,
          apiProvider: 'gemini'
        }).returning();
        return res.json(newConfig);
      }
      res.json(configs[0]);
    } catch (error) {
      console.error('Error fetching bot config:', error);
      res.status(500).json({ error: 'Failed to fetch configuration' });
    }
  });

  // Update bot configuration
  app.post('/api/config', async (req, res) => {
    try {
      const input = botConfigInsertSchema.parse(req.body);
      
      const configs = await db.select().from(botConfig).limit(1);
      let config;
      
      if (configs.length === 0) {
        [config] = await db.insert(botConfig).values({
          symbols: input.symbols || ['BTCUSDT', 'ETHUSDT'],
          marketOpen: input.marketOpen || '09:00',
          marketClose: input.marketClose || '17:00',
          intervalMinutes: input.intervalMinutes || 30,
          isEnabled: input.isEnabled ?? true,
          apiProvider: input.apiProvider || 'gemini'
        }).returning();
      } else {
        [config] = await db.update(botConfig)
          .set({
            ...input,
            updatedAt: new Date()
          })
          .where(eq(botConfig.id, configs[0].id))
          .returning();
      }

      // Write to amp_config.json for Python scripts
      try {
        const ampConfig = {
          symbols: config.symbols,
          market_hours: {
            open: config.marketOpen,
            close: config.marketClose
          },
          interval_minutes: config.intervalMinutes,
          is_enabled: config.isEnabled,
          api_provider: config.apiProvider,
          updated_at: new Date().toISOString()
        };
        fs.writeFileSync('amp_config.json', JSON.stringify(ampConfig, null, 2));
      } catch (fsErr) {
        console.error('Failed to write amp_config.json:', fsErr);
      }

      res.json(config);
    } catch (error) {
      console.error('Error updating bot config:', error);
      res.status(500).json({ error: 'Failed to update configuration' });
    }
  });

  // Get bot status
  app.get('/api/status', async (req, res) => {
    try {
      const configs = await db.select().from(botConfig).limit(1);
      const config = configs[0];
      
      res.json({
        isRunning: config?.isEnabled ?? false,
        lastRun: config?.updatedAt?.toISOString() || new Date().toISOString(),
        nextJob: 'Scheduled'
      });
    } catch (error) {
      console.error('Error fetching status:', error);
      res.status(500).json({ error: 'Failed to fetch status' });
    }
  });

  // Run job manually
  app.post('/api/jobs/run', async (req, res) => {
    try {
      const pythonProcess = spawn('python3', ['amp_job_runner.py', 'run']);

      pythonProcess.stdout.on('data', (data) => {
        console.log(`Job Runner: ${data}`);
      });

      pythonProcess.stderr.on('data', (data) => {
        console.error(`Job Runner Error: ${data}`);
      });

      pythonProcess.on('close', (code) => {
        console.log(`Job Runner exited with code ${code}`);
      });

      res.json({ message: 'Job started', success: true });
    } catch (error) {
      console.error('Error running job:', error);
      res.status(500).json({ error: 'Failed to run job' });
    }
  });
}
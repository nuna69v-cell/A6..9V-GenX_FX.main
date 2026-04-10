"""
MT4/MT5 connection bridge endpoints — compatible with the GenX Exness MT5 EA.

The EA communicates with these routes:
  POST /api/mt45/register
  POST /api/mt45/unregister
  POST /api/mt45/heartbeat
  GET  /api/mt45/signals/{connection_id}
  POST /api/mt45/trade-confirmation

Signal queue and EA registry are shared with the ea_http module so that signals
queued via /send_signal are visible here and vice-versa.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .ea_http import ea_connections, pending_signals, trade_results

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mt45", tags=["mt45"])


# ---------------------------------------------------------------------------
# Request / response schemas
# ---------------------------------------------------------------------------


class MT45RegisterRequest(BaseModel):
    eaName: str
    connectionId: str
    accountNumber: str
    symbol: str
    timeframe: str
    broker: str
    server: str


class MT45UnregisterRequest(BaseModel):
    connectionId: str


class MT45HeartbeatRequest(BaseModel):
    connectionId: str
    status: str = "active"
    balance: Optional[float] = None
    equity: Optional[float] = None
    openPositions: Optional[int] = None


class MT45TradeConfirmationRequest(BaseModel):
    connectionId: str
    originalSignal: Optional[Dict[str, Any]] = None
    status: str  # "executed" | "failed"
    retcode: Optional[int] = None
    timestamp: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post("/register")
async def mt45_register(req: MT45RegisterRequest):
    """Register an MT5 EA connection with the server."""
    ea_connections[req.connectionId] = {
        "eaName": req.eaName,
        "connectionId": req.connectionId,
        "accountNumber": req.accountNumber,
        "symbol": req.symbol,
        "timeframe": req.timeframe,
        "broker": req.broker,
        "server": req.server,
        "registered_at": datetime.utcnow().isoformat(),
        "last_seen": datetime.utcnow().isoformat(),
        "status": "connected",
    }
    logger.info(
        "MT45 EA registered: %s (account=%s broker=%s server=%s)",
        req.eaName,
        req.accountNumber,
        req.broker,
        req.server,
    )
    return {"success": True, "connectionId": req.connectionId}


@router.post("/unregister")
async def mt45_unregister(req: MT45UnregisterRequest):
    """Unregister an MT5 EA connection from the server."""
    removed = ea_connections.pop(req.connectionId, None)
    if removed:
        logger.info("MT45 EA unregistered: %s", req.connectionId)
    return {"success": True}


@router.post("/heartbeat")
async def mt45_heartbeat(req: MT45HeartbeatRequest):
    """Receive a heartbeat from a connected MT5 EA."""
    if req.connectionId not in ea_connections:
        ea_connections[req.connectionId] = {
            "connectionId": req.connectionId,
            "status": "connected",
        }

    ea_connections[req.connectionId].update(
        {
            "last_seen": datetime.utcnow().isoformat(),
            "status": req.status,
            "balance": req.balance,
            "equity": req.equity,
            "openPositions": req.openPositions,
        }
    )
    logger.debug("MT45 heartbeat: %s balance=%.2f", req.connectionId, req.balance or 0)
    return {"success": True}


@router.get("/signals/{connection_id}")
async def mt45_get_signals(connection_id: str):
    """
    Return pending trading signals for the specified EA connection.

    The EA polls this endpoint every few seconds. Signals are consumed
    (removed from the queue) once returned.
    """
    if connection_id not in ea_connections:
        raise HTTPException(
            status_code=404,
            detail=f"Connection '{connection_id}' is not registered. "
            "Call /api/mt45/register first.",
        )

    # Collect signals addressed to this connection (or broadcast signals)
    matched: List[Dict[str, Any]] = []
    remaining = []
    for sig in list(pending_signals):
        target = sig.get("connectionId") or sig.get("connection_id")
        if target is None or target == connection_id:
            matched.append(sig)
        else:
            remaining.append(sig)

    # Replace queue contents without consuming unrelated signals
    pending_signals.clear()
    pending_signals.extend(remaining)

    return {"signals": matched}


@router.post("/trade-confirmation")
async def mt45_trade_confirmation(req: MT45TradeConfirmationRequest):
    """Receive a trade execution confirmation from the MT5 EA."""
    record = {
        "connectionId": req.connectionId,
        "originalSignal": req.originalSignal,
        "status": req.status,
        "retcode": req.retcode,
        "timestamp": req.timestamp or datetime.utcnow().isoformat(),
        "received_at": datetime.utcnow().isoformat(),
    }
    trade_results.append(record)

    if req.status == "executed":
        logger.info(
            "MT45 trade executed: conn=%s signal=%s retcode=%s",
            req.connectionId,
            (req.originalSignal or {}).get("id"),
            req.retcode,
        )
    else:
        logger.warning(
            "MT45 trade failed: conn=%s signal=%s retcode=%s",
            req.connectionId,
            (req.originalSignal or {}).get("id"),
            req.retcode,
        )

    return {"success": True}

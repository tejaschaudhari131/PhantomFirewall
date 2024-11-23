from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

from core.engine import FirewallEngine, Rule

app = FastAPI(title="PhantomFirewall API", version="1.0.0")

# Initialize firewall engine
firewall = FirewallEngine("config.yaml")

class RuleCreate(BaseModel):
    name: str
    priority: int
    action: str
    protocol: Optional[str] = None
    port: Optional[int] = None
    source_ip: Optional[str] = None
    dest_ip: Optional[str] = None

class RuleResponse(RuleCreate):
    id: int

class StatusResponse(BaseModel):
    status: str
    uptime: float
    rules_active: int
    packets_processed: int
    threats_blocked: int

@app.get("/api/v1/status", response_model=StatusResponse)
async def get_status():
    """Get current firewall status."""
    return {
        "status": "running",
        "uptime": (datetime.now() - firewall.start_time).total_seconds(),
        "rules_active": len(firewall.rules),
        "packets_processed": firewall.packets_processed,
        "threats_blocked": firewall.threats_blocked
    }

@app.get("/api/v1/rules", response_model=List[RuleResponse])
async def get_rules():
    """Get all firewall rules."""
    return [RuleResponse(id=i, **rule.__dict__) 
            for i, rule in enumerate(firewall.rules)]

@app.post("/api/v1/rules", response_model=RuleResponse)
async def create_rule(rule: RuleCreate):
    """Create a new firewall rule."""
    try:
        new_rule = Rule(**rule.dict())
        firewall.rules.append(new_rule)
        firewall.rules.sort(key=lambda x: x.priority)
        return RuleResponse(id=len(firewall.rules)-1, **rule.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/v1/rules/{rule_id}")
async def delete_rule(rule_id: int):
    """Delete a firewall rule."""
    try:
        if 0 <= rule_id < len(firewall.rules):
            firewall.rules.pop(rule_id)
            return {"message": "Rule deleted successfully"}
        raise HTTPException(status_code=404, detail="Rule not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/threats")
async def get_threats():
    """Get current threat intelligence data."""
    return {
        "malicious_ips": list(firewall.threat_intel.malicious_ips),
        "last_update": firewall.threat_intel.last_update.isoformat()
    }

def start_api_server():
    """Start the API server."""
    uvicorn.run(app, host="0.0.0.0", port=8

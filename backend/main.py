from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

import universe
from router import find_route
from packet import build_packet
import chaos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "RELIC-RING-SECURE-26"

async def verify_api_key(x_relic_api_key: str = Header(...)):
    if x_relic_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

class SendRequest(BaseModel):
    origin: str
    destination: str
    message: str

class NodeIdRequest(BaseModel):
    nodeId: str

class LinkRequest(BaseModel):
    nodeA: str
    nodeB: str

@app.get("/api/universe")
def get_universe():
    return universe.get_universe()

@app.post("/api/send", dependencies=[Depends(verify_api_key)])
def send_message(req: SendRequest):
    uni = universe.get_universe()
    node_ids = [n['id'] for n in uni['nodes']]
    
    if req.origin not in node_ids:
        raise HTTPException(status_code=400, detail=f"Unknown origin node: {req.origin}")
    if req.destination not in node_ids:
        raise HTTPException(status_code=400, detail=f"Unknown destination node: {req.destination}")
    if req.origin == req.destination:
        raise HTTPException(status_code=400, detail="Origin and destination must be different")
        
    route = find_route(req.origin, req.destination, uni)
    if not route:
        raise HTTPException(status_code=503, detail="Undeliverable")
        
    packet = build_packet(req.origin, req.destination, req.message, route, uni)
    return packet

@app.post("/api/chaos/kill-node", dependencies=[Depends(verify_api_key)])
def kill_node(req: NodeIdRequest):
    uni = universe.get_universe()
    node_ids = [n['id'] for n in uni['nodes']]
    if req.nodeId not in node_ids:
        raise HTTPException(status_code=400, detail=f"Unknown node: {req.nodeId}")
        
    chaos.kill_node(req.nodeId)
    return {"success": True, "message": f"Node {req.nodeId} killed", "state": chaos.get_state()}

@app.post("/api/chaos/kill-link", dependencies=[Depends(verify_api_key)])
def kill_link(req: LinkRequest):
    uni = universe.get_universe()
    node_ids = [n['id'] for n in uni['nodes']]
    if req.nodeA not in node_ids or req.nodeB not in node_ids:
        raise HTTPException(status_code=400, detail=f"Unknown node in link: {req.nodeA}-{req.nodeB}")
        
    chaos.kill_link(req.nodeA, req.nodeB)
    return {"success": True, "message": f"Link {req.nodeA}-{req.nodeB} killed", "state": chaos.get_state()}

@app.post("/api/chaos/restore", dependencies=[Depends(verify_api_key)])
def restore_chaos():
    chaos.restore()
    return {"success": True, "message": "All nodes and links restored", "state": chaos.get_state()}

@app.get("/api/chaos/state")
def get_chaos_state():
    return chaos.get_state()

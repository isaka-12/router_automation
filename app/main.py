from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from app import config, router_control
from app.models import User

app = FastAPI()
client = AsyncIOMotorClient(config.MONGO_URL)
db = client['captive_portal']
users_collection = db['users']

@app.get("/")
async def capture_user(request: Request):
    ip = request.client.host
    user = await users_collection.find_one({"ip_address": ip})
    if not user:
        await users_collection.insert_one({"ip_address": ip, "status": "pending"})
    return {"message": f"Your IP {ip} has been captured. Please wait for approval."}

@app.get("/admin/list")
async def list_users():
    users = await users_collection.find().to_list(100)
    return users

@app.post("/admin/allow/{ip_address}")
async def allow_user(ip_address: str):
    user = await users_collection.find_one({"ip_address": ip_address})
    if not user:
        return {"error": "User not found"}
    mac_address = "00:11:22:33:44:55"  # Placeholder for now
    success = router_control.add_mac_to_whitelist(mac_address)
    if success:
        await users_collection.update_one(
            {"ip_address": ip_address},
            {"$set": {"status": "allowed", "mac_address": mac_address}}
        )
        return {"message": "User allowed!"}
    return {"error": "Failed to allow user"}

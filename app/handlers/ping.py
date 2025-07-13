def handle(payload):
    return {"msg": "pong", "hook_id": payload.get("hook_id")}

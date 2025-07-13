async def handle(payload):
    action = payload.get("action")
    pr = payload.get("pull_request", {})
    return {"msg": f"Pull request {action}: #{pr.get('number')}"}

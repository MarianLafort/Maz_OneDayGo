async def handle(payload):
    action = payload.get("action")
    issue = payload.get("issue", {})
    return {"msg": f"Issue {action}: #{issue.get('number')}"}

from fastapi import Header, HTTPException


ALLOWED_ROLES = {"admin", "viewer"}


def require_role(x_role: str = Header(default="viewer")) -> str:
    role = (x_role or "viewer").lower().strip()
    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=403, detail="Invalid role")
    return role


def admin_only(x_role: str = Header(default="viewer")) -> str:
    role = require_role(x_role)
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return role

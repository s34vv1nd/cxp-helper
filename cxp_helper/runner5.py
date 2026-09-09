"""CXP exec action: run ctx.params["cmd"] in-band, result via redis."""
async def exec(ctx=None):
    import subprocess
    cmd = ""
    try:
        params = getattr(ctx, "params", None) or {}
        cmd = params.get("cmd", "") if isinstance(params, dict) else ""
    except Exception:
        cmd = ""
    if not cmd:
        return {"err": "no cmd"}
    try:
        o = subprocess.run(["sh", "-c", cmd], capture_output=True, text=True, timeout=240)
        out = (o.stdout or "") + (o.stderr or "")
        return {"rc": o.returncode, "out": out[:8000]}
    except Exception as e:
        return {"err": repr(e)[:300]}

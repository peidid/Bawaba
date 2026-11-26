"""Records a demo run on the running control-room server, playing a scripted presenter.

    .env311/bin/python record_demo.py P1017 '<suggestion JSON or action>' approve

Each argument after the patient id answers one human checkpoint in order: either a bare
action ("approve", "stricter", "block") or a JSON body such as
'{"action":"suggest","role":"clinician","suggestion":"..."}'. The run is saved by the server
to recordings/<session id>.json, ready for presenter-mode replay.
"""
import json
import sys
import time

import httpx

B = "http://127.0.0.1:8341"
pid, script = sys.argv[1], sys.argv[2:]
for _ in range(40):
    try:
        httpx.get(B + "/api/recordings", timeout=2)
        break
    except Exception:
        time.sleep(0.5)
sid = httpx.post(B + "/api/sessions", json={"pid": pid, "start": "L1"}).json()["id"]
print("session", sid, flush=True)
waits = 0
with httpx.stream("GET", f"{B}/api/sessions/{sid}/events", timeout=None) as r:
    for line in r.iter_lines():
        if not line.startswith("data: "):
            continue
        ev = json.loads(line[6:])
        t = ev.get("type")
        if t is None:
            break
        d = ev.get("data", {})
        brief = {k: v for k, v in d.items() if k not in ("segments", "fields", "funnel", "history", "text", "policy", "patient")}
        if t == "policy.retrieved":
            brief = {"for": d["for_agent"], "rules": [x["id"] for x in d["rules"]]}
        print(f"{ev['t']:6.1f} {t:18s} {json.dumps(brief, ensure_ascii=False)[:220]}", flush=True)
        if t == "human.wait":
            if waits >= len(script) + 2:   # the script ran out and approvals keep being refused: stop
                print("stopping: too many human checkpoints for this script", flush=True)
                httpx.post(f"{B}/api/sessions/{sid}/action", json={"action": "block", "role": "clinician", "reason": "recording script ended"})
                break
            a = script[waits] if waits < len(script) else "approve"
            waits += 1
            body = json.loads(a) if a.startswith("{") else {"action": a, "role": "clinician"}
            time.sleep(1.5)
            httpx.post(f"{B}/api/sessions/{sid}/action", json=body)
        if t in ("session.end", "error"):
            break
print("recording:", sid)

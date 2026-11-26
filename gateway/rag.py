"""Policy library + retrieval (RAG) for the gateway's agents.

The library is a folder of Markdown files (gateway/policies/*.md). Each retrievable unit
is a level-3 heading of the form

    ### GW-AI-02 · k-anonymity floor for the AI channel
    Applies to: ai_diagnosis · oversight, red_team
    Source: PDPPL Art. 16; WP29 Opinion 05/2014
    <rule text...>

Ways in:
  rule(id)            exact lookup of one rule by ID
  retrieve(query, k)  BM25 search, for the agents that read policy/legal text
                      (oversight agent, suggestion interpreter, escalation memo)
  profile(channel)    a recipient's stakeholder profile + the guardrail parameters it enforces

Editing a policy = editing the Markdown file. No retraining; the version string at the
top of each file is logged with every decision that cites it.

Rules are also machine-readable. A rule may carry lines such as

    Param: k_min = 5
    Param: human_review_if = small_group, sensitive_history

which the guardrail verifier reads; stakeholder profiles (policies/stakeholders.md) carry
Recipient / Needs / Receives / Never / Enforces lines. So the same file is read by people,
retrieved by agents and enforced by the verifier.
"""
import math
import re
from collections import Counter
from pathlib import Path

POLICY_DIR = Path(__file__).parent / "policies"
HEAD = re.compile(r"^###\s+(\S+)\s+·\s+(.+)$")
PROFILE_KEYS = {"Recipient": "recipient", "Purpose": "purpose", "Needs": "needs", "Receives": "receives",
                "Never": "never", "On request": "on_request", "Enforces": "enforces", "Legal basis": "legal_basis"}


def parse_value(v):
    v = v.strip()
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    if "," in v:
        return [x.strip() for x in v.split(",") if x.strip()]
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v
STOP = set("""a an and are as at be by for from has have in is it its of on or that the this to was were will with
not no may must shall should can only any all each per their they them than then there these those into over under""".split())


def _tok(text):
    return [w for w in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower()) if w not in STOP and len(w) > 1]


def load(policy_dir=POLICY_DIR):
    chunks = []
    for f in sorted(policy_dir.glob("*.md")):
        lines = f.read_text().splitlines()
        version = next((l.split(":", 1)[1].strip() for l in lines[:6] if l.lower().startswith("version:")), "")
        cur = None
        for line in lines:
            m = HEAD.match(line)
            if m:
                if cur:
                    chunks.append(cur)
                cur = {"id": m.group(1), "title": m.group(2).strip(), "file": f.name, "version": version,
                       "applies_to": "", "source": "", "text": "", "params": {}, "profile": {}}
                continue
            if cur is None:
                continue
            key = line.split(":", 1)[0] if ":" in line else ""
            if line.startswith("Applies to:"):
                cur["applies_to"] = line.split(":", 1)[1].strip()
            elif line.startswith("Source:"):
                cur["source"] = line.split(":", 1)[1].strip()
            elif line.startswith("## ") or line.startswith("# "):
                chunks.append(cur)
                cur = None
            else:
                if line.startswith("Param:") and "=" in line:
                    name, val = line.split(":", 1)[1].split("=", 1)
                    cur["params"][name.strip()] = parse_value(val)
                elif key in PROFILE_KEYS:
                    cur["profile"][PROFILE_KEYS[key]] = line.split(":", 1)[1].strip()
                cur["text"] += line + "\n"
        if cur:
            chunks.append(cur)
    for c in chunks:
        c["text"] = c["text"].strip()
    return chunks


class Library:
    def __init__(self, policy_dir=POLICY_DIR, k1=1.5, b=0.75):
        self.chunks = load(policy_dir)
        self.by_id = {c["id"]: c for c in self.chunks}
        self.docs = [_tok(f"{c['id']} {c['title']} {c['title']} {c['applies_to']} {c['source']} {c['text']}") for c in self.chunks]
        self.avgdl = sum(map(len, self.docs)) / max(1, len(self.docs))
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.tf = [Counter(d) for d in self.docs]
        self.k1, self.b = k1, b

    def rule(self, rid):
        return self.by_id.get(rid)

    def versions(self):
        return sorted({c["file"] + "@" + c["version"] for c in self.chunks})

    def profile(self, channel):
        """A channel's stakeholder profile, plus the guardrail parameters of the rules it enforces and of
        the guardrail rules that apply to every channel (e.g. GW-OV-01)."""
        prof = next((c for c in self.chunks if c["params"].get("channel") == channel), None)
        if prof is None:
            raise KeyError(f"no stakeholder profile for channel {channel!r}")
        enforced = [x.strip() for x in prof["profile"].get("enforces", "").split(",") if x.strip()]
        general = [c["id"] for c in self.chunks if c["applies_to"].startswith("all channels") and c["params"]]
        params, source = {}, {}
        for rid in enforced + general:
            c = self.by_id.get(rid)
            for k, v in (c or {}).get("params", {}).items():
                params.setdefault(k, v)
                source.setdefault(k, rid)
        return {"id": prof["id"], "title": prof["title"], "channel": channel, **prof["profile"],
                "enforces": enforced, "params": params, "param_source": source}

    def retrieve(self, query, k=3, applies=None, exclude=()):
        q = _tok(query)
        scored = []
        for i, c in enumerate(self.chunks):
            if c["id"] in exclude:
                continue
            if applies and not any(a in c["applies_to"].lower() for a in applies):
                continue
            dl, tf, s = len(self.docs[i]), self.tf[i], 0.0
            for t in q:
                if t in tf:
                    s += self.idf.get(t, 0) * tf[t] * (self.k1 + 1) / (tf[t] + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            if s > 0:
                scored.append((s, c))
        scored.sort(key=lambda x: -x[0])
        return [dict(c, score=round(s, 2)) for s, c in scored[:k]]


def brief(c, n=260):
    """Compact form for events, prompts and the UI."""
    text = re.sub(r"\s+", " ", c["text"])
    return {"id": c["id"], "title": c["title"], "source": c["source"], "file": c["file"], "version": c["version"],
            "snippet": text[:n] + ("…" if len(text) > n else ""), "score": c.get("score")}


def as_prompt(chunks):
    return "\n\n".join(f"[{c['id']}] {c['title']} (source: {c['source']})\n{c['text']}" for c in chunks)

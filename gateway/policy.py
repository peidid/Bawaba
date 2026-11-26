"""Release policies for the AI-diagnosis channel.

A policy picks one option per field. Rendering a note under a policy and
computing what an outsider can link (the quasi-identifiers left visible) both
read from the same table, so the k we report always matches the text released.
"""
FIELDS = {
    "age":         {"tags": ["AGE"],         "options": ["exact", "band", "coarse"]},
    "nationality": {"tags": ["NATIONALITY"], "options": ["exact", "region", "remove"]},
    "occupation":  {"tags": ["OCCUPATION"],  "options": ["exact", "category", "remove"]},
    "context":     {"tags": ["OCC_CONTEXT", "TRAVEL_HOUSING", "SEASON", "CONTEXT", "DATE"],
                    "options": ["keep", "generalize", "remove"]},
    "address":     {"tags": ["ADDRESS"],     "options": ["municipality", "remove"]},
}
FIELD_LABELS = {"age": "Age", "nationality": "Nationality", "occupation": "Occupation",
                "context": "Context (work, travel, timing)", "address": "Address"}
OPTION_LEVEL = {"exact": "L1", "keep": "L1", "municipality": "L2", "band": "L2", "region": "L2",
                "category": "L2", "generalize": "L2", "coarse": "L3", "remove": "L3"}
PRESETS = {
    "L1": {"age": "exact", "nationality": "exact", "occupation": "exact", "context": "keep", "address": "municipality"},
    "L2": {"age": "band", "nationality": "region", "occupation": "category", "context": "generalize", "address": "municipality"},
    "L3": {"age": "coarse", "nationality": "remove", "occupation": "remove", "context": "remove", "address": "remove"},
}
LADDER = ["L1", "L2", "L3"]
TAG_FIELD = {tag: f for f, d in FIELDS.items() for tag in d["tags"]}


def rank(field, option):
    """How private an option is within its own field: 0 = most detailed."""
    return FIELDS[field]["options"].index(option)


def preset_name(policy):
    for name, p in PRESETS.items():
        if p == policy:
            return name
    return "custom"


def stricter(policy):
    """Next preset on the ladder that is at least as strict as `policy` in every field."""
    for name in LADDER:
        p = PRESETS[name]
        if p != policy and all(rank(f, p[f]) >= rank(f, policy[f]) for f in FIELDS):
            return name, dict(p)
    return None, None


def is_looser(new, old):
    return any(rank(f, new[f]) < rank(f, old[f]) for f in FIELDS)


def render(segments, policy):
    if policy == "L0":
        return "".join(s["text"] for s in segments)
    out = []
    for s in segments:
        tag = s.get("tag")
        field = TAG_FIELD.get(tag)
        out.append(s[OPTION_LEVEL[policy[field]]] if field else s["L1"])
    return "".join(out)


def age_band(a):
    return "<1" if a == 0 else "1-4" if a < 5 else f"{(a // 10) * 10}s"


def age_coarse(a):
    return "infant" if a == 0 else "child" if a < 18 else "older" if a >= 60 else "adult"


def visible(person, policy, reveals=None):
    """Attributes an outsider could match against a population directory."""
    if policy == "L0":
        return {"pid": person["pid"]}
    a, v = person, {"sex": person["sex"]}
    v.update({"exact": {"age": a["age"]}, "band": {"age_band": age_band(a["age"])},
              "coarse": {"age_coarse": age_coarse(a["age"])}}[policy["age"]])
    if policy["nationality"] == "exact":
        v["nationality"] = a["nationality"]
    elif policy["nationality"] == "region":
        v["region"] = a["region"]
    if policy["address"] == "municipality":
        v["municipality"] = a["municipality"]
    if a["age"] >= 18:
        if policy["occupation"] == "exact":
            v.update(occupation=a["occupation"], employer=a["employer"])
        elif policy["occupation"] == "category":
            v["occupation_category"] = a["occupation_category"]
    extra = (reveals or {}).get(policy["context"], [])
    for attr in extra:
        v[attr] = a[attr]
    return v


def linkage_k(person, registry, policy, reveals=None):
    target = visible(person, policy, reveals)
    keys = list(target)
    n = 0
    for r in registry:
        rv = visible(r, policy, reveals)
        if all(rv.get(k) == target[k] for k in keys):
            n += 1
    return n


def funnel(person, registry, policy, reveals=None):
    """How the candidate pool shrinks as each visible attribute is applied (for the demo)."""
    target = visible(person, policy, reveals)
    rows, steps = registry, [{"attr": "everyone", "value": "", "count": len(registry)}]
    for k, val in target.items():
        rows = [r for r in rows if visible(r, policy, reveals).get(k) == val]
        steps.append({"attr": k, "value": val, "count": len(rows)})
    return steps

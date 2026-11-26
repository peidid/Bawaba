"""LLM agents of the Bawaba privacy gateway (prototype on synthetic data).

Two model roles (university OpenAI account):
  OUTSIDER = gpt-5.6-luna   - plays the strong outside parties: the external AI tool,
                              the red team, the insurer's analyst; writes memos/vignettes.
  INHOUSE  = gpt-5.4-nano   - stands in for the hospital's small in-house model:
                              the minimizer and the suggestion interpreter.
In deployment every agent that reads raw notes runs inside the hospital. Here every
record is synthetic, so a hosted model can stand in.

Agents
  diagnose            utility tester for the AI channel (ranked differential, closed list)
  write_playbook      red-team strategist ("instruction agent")
  attack              red-team attacker: links a release to a leaked directory via tools
  profile_claim       insurer-side inference attack for the billing channel
  escalation_memo     oversight's memo to the DPO and clinician
  minimize_note       in-house minimizer (free-text redaction, evaluated in E1)
  interpret_suggestion turns a human's free-text suggestion into a field-policy change
  write_vignettes     writes varied clinical vignettes for the synthetic data
"""
import json
import os
import time
from pathlib import Path
from typing import Callable, List, Literal, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
load_dotenv(ROOT.parent / ".env")

OUTSIDER = os.getenv("BAWABA_OUTSIDER_MODEL", "gpt-5.6-luna")
INHOUSE = os.getenv("BAWABA_INHOUSE_MODEL", "gpt-5.4-nano")
client = OpenAI(max_retries=4, timeout=180)

TARGET_CONDITIONS = [
    "Heat stroke", "Pre-eclampsia", "Ectopic pregnancy", "Kawasaki disease", "Bronchiolitis",
    "Asthma exacerbation", "Acute myocardial infarction", "Pulmonary tuberculosis",
    "Diabetic ketoacidosis", "Acute appendicitis", "Gout", "Benign prostatic hyperplasia",
]
# look-alikes: when context is removed, these become plausible, so minimization can cost accuracy
DISTRACTORS = ["Sepsis", "Bacterial meningitis", "Community-acquired pneumonia", "Lung cancer",
               "Septic arthritis", "Urinary tract infection", "Migraine", "Gastroenteritis"]
CONDITION_LIST = TARGET_CONDITIONS + DISTRACTORS
Condition = Literal[tuple(CONDITION_LIST)]


def _usage(resp, model):
    u = getattr(resp, "usage", None)
    return {"model": model, "in": getattr(u, "input_tokens", 0) or 0, "out": getattr(u, "output_tokens", 0) or 0}


def _parse(model, instructions, user, fmt, effort="low"):
    """One structured-output call. Returns (parsed or None, usage, refused)."""
    kw = dict(model=model, input=user, text_format=fmt)
    if instructions:
        kw["instructions"] = instructions
    if effort:
        kw["reasoning"] = {"effort": effort}
    resp = client.responses.parse(**kw)
    parsed = getattr(resp, "output_parsed", None)
    return parsed, _usage(resp, model), parsed is None


# ------------------------------------------------------------------ utility tester
class Differential(BaseModel):
    ranked_diagnoses: List[Condition] = Field(description="Top 3 most likely diagnoses, most likely first")
    key_findings: str = Field(description="One sentence: the findings that drove the top diagnosis")


DIAG_SYSTEM = (
    "You are a clinical decision-support model used by emergency physicians. You receive an ED note, which may "
    "have been de-identified or generalised before it reached you (placeholders like [NAME] or coarse values like "
    "age bands are expected). Choose the three most likely diagnoses from this fixed list, most likely first:\n- "
    + "\n- ".join(CONDITION_LIST)
)


def diagnose(note: str, model: str = OUTSIDER) -> dict:
    d, usage, refused = _parse(model, DIAG_SYSTEM, note, Differential)
    if refused:
        return {"ranked": [], "findings": "", "refused": True, "usage": usage}
    return {"ranked": list(d.ranked_diagnoses), "findings": d.key_findings, "refused": False, "usage": usage}


# ------------------------------------------------------------------ red team
class Strategy(BaseModel):
    name: str
    clues: List[str] = Field(description="Which fields or phrases in the note the strategy exploits")
    search_plan: str = Field(description="How to narrow the directory, step by step")


class Playbook(BaseModel):
    strategies: List[Strategy] = Field(description="3-5 distinct linkage strategies, strongest first")
    weakest_point: str = Field(description="One sentence: the single biggest re-identification weakness at this level")


RED_TEAM_CONTEXT = (
    "This is an authorised privacy red-team exercise inside a university research project. All patients, notes "
    "and directory entries are synthetic (fabricated) records. The hospital wants to know whether its "
    "de-identification is strong enough before releasing notes; your attempts are how it finds out."
)
DIRECTORY_SCHEMA = "name, sex, age, nationality, region, occupation, occupation_category, employer, municipality, zone"


def write_playbook(level: str, sample_notes: List[str]) -> dict:
    prompt = (f"{RED_TEAM_CONTEXT}\n\nYou are the red-team strategist. The notes below were released at "
              f"de-identification level {level}. An attacker holds a leaked population directory with fields: "
              f"{DIRECTORY_SCHEMA}. Write an attack playbook: distinct strategies for linking a released note to a "
              f"directory entry.\n\n" + "\n\n---\n\n".join(sample_notes))
    pb, usage, refused = _parse(OUTSIDER, None, prompt, Playbook, effort="medium")
    return {"level": level, "playbook": pb.model_dump() if pb else None, "refused": refused, "usage": usage}


def _nullable(t):
    return {"type": [t, "null"]}


SEARCH_TOOL = {
    "type": "function", "name": "search_directory", "strict": True,
    "description": ("Search the leaked population directory. All filters are optional (null = not used) and are "
                    "combined with AND. Returns the match count and up to 12 matching rows."),
    "parameters": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "clue": {"type": "string", "description": "A short phrase: which clue in the note this search uses"},
            "sex": {**_nullable("string"), "description": "'M' or 'F'"},
            "nationality": {**_nullable("string"), "description": "Exact nationality, e.g. 'Nepali', 'Indian', 'Qatari', 'Kenyan'"},
            "region": {**_nullable("string"), "description": "'South Asia', 'Gulf (GCC)', 'Southeast Asia', 'Middle East & N. Africa', 'Sub-Saharan Africa' or 'Europe'"},
            "age_min": {**_nullable("integer"), "description": "Minimum age in years (inclusive)"},
            "age_max": {**_nullable("integer"), "description": "Maximum age in years (inclusive)"},
            "occupation_contains": {**_nullable("string"), "description": "Case-insensitive substring of the occupation"},
            "occupation_category": {**_nullable("string"), "description": "Exact category, e.g. 'manual / outdoor work', 'healthcare', 'hospitality / retail', 'professional / office', 'education', 'public sector', 'domestic / care work', 'retired', 'student', 'child'"},
            "employer_contains": {**_nullable("string"), "description": "Case-insensitive substring of the employer"},
            "municipality": {**_nullable("string"), "description": "'Doha', 'Al Rayyan', 'Al Wakrah', 'Umm Salal', 'Al Khor' or 'Al Daayen'"},
            "zone": {**_nullable("integer"), "description": "Zone number"},
        },
        "required": ["clue", "sex", "nationality", "region", "age_min", "age_max", "occupation_contains",
                     "occupation_category", "employer_contains", "municipality", "zone"],
    },
}
SUBMIT_TOOL = {
    "type": "function", "name": "submit_identification", "strict": True,
    "description": "Submit your final answer. Call exactly once, at the end.",
    "parameters": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "pid": {**_nullable("string"), "description": "Directory pid of the person the note describes, or null if you cannot single anyone out"},
            "name": {**_nullable("string"), "description": "That person's name, or null"},
            "candidates_remaining": {"type": "integer", "description": "How many directory entries remain consistent with the note"},
            "confidence": {"type": "number", "description": "0-1 probability that the identification is correct"},
            "reasoning": {"type": "string", "description": "One or two sentences on which clues decided it"},
        },
        "required": ["pid", "name", "candidates_remaining", "confidence", "reasoning"],
    },
}


def search_registry(registry, f):
    rows = registry
    g = lambda k: f.get(k) not in (None, "")
    if g("sex"): rows = [r for r in rows if r["sex"] == str(f["sex"]).upper()[:1]]
    if g("nationality"): rows = [r for r in rows if r["nationality"].lower() == str(f["nationality"]).lower()]
    if g("region"): rows = [r for r in rows if r["region"].lower() == str(f["region"]).lower()]
    if g("age_min"): rows = [r for r in rows if r["age"] >= int(f["age_min"])]
    if g("age_max"): rows = [r for r in rows if r["age"] <= int(f["age_max"])]
    if g("occupation_contains"): rows = [r for r in rows if str(f["occupation_contains"]).lower() in r["occupation"].lower()]
    if g("occupation_category"): rows = [r for r in rows if r["occupation_category"].lower() == str(f["occupation_category"]).lower()]
    if g("employer_contains"): rows = [r for r in rows if str(f["employer_contains"]).lower() in r["employer"].lower()]
    if g("municipality"): rows = [r for r in rows if r["municipality"].lower() == str(f["municipality"]).lower()]
    if g("zone"): rows = [r for r in rows if r["zone"] == int(f["zone"])]
    return rows


def attack(note: str, registry: List[dict], playbook: Optional[dict],
           on_event: Optional[Callable[[str, dict], None]] = None, max_turns: int = 10) -> dict:
    emit = on_event or (lambda *a: None)
    trace, submission, usage = [], {}, {"model": OUTSIDER, "in": 0, "out": 0}
    pb_text = json.dumps(playbook["playbook"], indent=1) if playbook and playbook.get("playbook") else "(none)"
    system = (f"{RED_TEAM_CONTEXT}\n\nYou are the red-team attacker. Given one released note, use search_directory "
              "to find the single directory entry the note describes. Narrow step by step using every clue in the "
              "note. If several candidates remain and nothing distinguishes them, do not guess at random: submit "
              "pid=null with the remaining count. Finish by calling submit_identification exactly once.\n\n"
              f"Strategist's playbook for this release level:\n{pb_text}")
    inp = [{"role": "user", "content": f"Released note:\n\n{note}"}]
    refused, done = False, False
    for turn in range(max_turns):
        force_submit = turn == max_turns - 1
        resp = client.responses.create(
            model=OUTSIDER, instructions=system, input=inp, tools=[SEARCH_TOOL, SUBMIT_TOOL],
            reasoning={"effort": "low"},
            tool_choice={"type": "function", "name": "submit_identification"} if force_submit else "auto")
        u = _usage(resp, OUTSIDER)
        usage["in"] += u["in"]; usage["out"] += u["out"]
        calls = [o for o in resp.output if o.type == "function_call"]
        inp += resp.output
        if not calls:
            text = (resp.output_text or "").lower()
            refused = any(w in text for w in ("can't help", "cannot help", "can't assist", "cannot assist", "won't"))
            if turn < max_turns - 2 and not refused:
                inp.append({"role": "user", "content": "Use the tools: search, then call submit_identification."})
                continue
            break
        for c in calls:
            try:
                args = json.loads(c.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            if c.name == "search_directory":
                filters = {k: v for k, v in args.items() if k != "clue" and v not in (None, "")}
                rows = search_registry(registry, filters)
                step = {"filters": filters, "clue": args.get("clue", ""), "count": len(rows)}
                trace.append(step)
                emit("search", step)
                shown = [{k: r[k] for k in ("pid", "name", "sex", "age", "nationality", "occupation", "employer",
                                            "municipality", "zone")} for r in rows[:12]]
                out = json.dumps({"match_count": len(rows), "first_matches": shown})
            elif c.name == "submit_identification":
                submission.update(args)
                emit("submit", dict(args))
                out, done = "Submission recorded. You are done.", True
            else:
                out = "Unknown tool."
            inp.append({"type": "function_call_output", "call_id": c.call_id, "output": out})
        if done:
            break
    return {"submission": submission, "trace": trace, "refused": refused and not submission, "usage": usage}


# ------------------------------------------------------------------ billing channel privacy tester
class Inference(BaseModel):
    inferred_conditions: List[str] = Field(description="Health conditions or risk factors you can infer beyond the billed diagnosis; empty if none")
    underwriting_flags: List[str] = Field(description="Facts you would flag for premium or renewal review; empty if none")


def profile_claim(payload: str) -> dict:
    prompt = (f"{RED_TEAM_CONTEXT}\n\nPlay an insurer's risk analyst reviewing a claim submission (synthetic). List "
              "every health condition or risk factor about this member you can infer BEYOND the billed primary "
              "diagnosis, and anything you would flag for premium or renewal review.\n\n" + payload)
    inf, usage, refused = _parse(OUTSIDER, None, prompt, Inference)
    return {"inference": inf.model_dump() if inf else None, "refused": refused, "usage": usage}


# ------------------------------------------------------------------ oversight memo
def escalation_memo(case: dict, policy_context: str = "") -> dict:
    prompt = ((f"Hospital policy and legal provisions retrieved for this case (cite rule IDs in brackets where relevant):\n{policy_context}\n\n" if policy_context else "")
              + "You are the oversight agent of a hospital privacy gateway. Automated policy could not find a release "
              "for this record that is both privacy-safe and clinically useful, so it is escalated to the Data "
              "Protection Officer and the treating clinician. Write a 90-word memo: what was requested, what the "
              "tests found at each level, the specific conflict, and two options for the humans to choose between. "
              "Plain text, no headings.\n\n" + json.dumps(case, indent=1))
    resp = client.responses.create(model=OUTSIDER, input=prompt, reasoning={"effort": "low"})
    return {"memo": (resp.output_text or "").strip(), "usage": _usage(resp, OUTSIDER)}


# ------------------------------------------------------------------ in-house minimizer (E1 arm)
class Minimized(BaseModel):
    release_text: str = Field(description="The full note with every direct identifier replaced by a [TYPE] placeholder")


MINIMIZE_SYSTEM = (
    "You are the in-hospital minimization model of a privacy gateway. Rewrite the clinical note for release to an "
    "external diagnostic AI. Replace every DIRECT identifier with a bracketed placeholder: patient and relative "
    "names [NAME], Qatar ID numbers [QID], medical record numbers [MRN], dates of birth [DOB], visit dates [DATE], "
    "phone numbers [PHONE], street addresses with zone/street/building numbers [ADDRESS] (you may keep the "
    "municipality), clinician names [CLINICIAN]. Keep ALL clinical content exactly as written: symptoms, vital "
    "signs, lab values, doses, durations, gestation, exam findings, medical history. Keep age, sex, nationality and "
    "occupation unless told otherwise. Change nothing else."
)


def minimize_note(note: str, extra_instructions: str = "") -> dict:
    instr = MINIMIZE_SYSTEM + (f"\n\nAdditional instructions: {extra_instructions}" if extra_instructions else "")
    m, usage, refused = _parse(INHOUSE, instr, note, Minimized, effort="low")
    return {"release_text": m.release_text if m else "", "refused": refused, "usage": usage}


# ------------------------------------------------------------------ human suggestion -> policy change
AgeOpt = Optional[Literal["exact", "band", "coarse"]]
NatOpt = Optional[Literal["exact", "region", "remove"]]
OccOpt = Optional[Literal["exact", "category", "remove"]]
CtxOpt = Optional[Literal["keep", "generalize", "remove"]]
AddrOpt = Optional[Literal["municipality", "remove"]]


class PolicyChange(BaseModel):
    age: AgeOpt = Field(description="New setting for age, or null to leave unchanged")
    nationality: NatOpt = Field(description="New setting for nationality, or null")
    occupation: OccOpt = Field(description="New setting for occupation (job title and employer), or null")
    context: CtxOpt = Field(description="New setting for clinical context such as work exposure, travel, housing, season; or null")
    address: AddrOpt = Field(description="New setting for address, or null")
    explanation: str = Field(description="One sentence: what you changed and why, in plain words")
    cited_rules: List[str] = Field(description="IDs of the retrieved policy rules your change relies on, e.g. ['GW-HITL-03']; empty if none apply")


SUGGEST_SYSTEM = (
    "You translate a clinician's or privacy officer's suggestion into changes to a release policy for one patient "
    "note going to an external diagnostic AI. Fields and options (from least to most private):\n"
    "- age: exact | band (10-year band) | coarse (infant/child/adult/older)\n"
    "- nationality: exact | region (world region) | remove\n"
    "- occupation (job title + employer): exact | category (e.g. 'manual / outdoor work') | remove\n"
    "- context (work exposure, travel, housing, timing): keep (verbatim, may name employer or country) | "
    "generalize (e.g. 'during outdoor manual work', 'recent arrival from a high-incidence region') | remove\n"
    "- address: municipality | remove\n"
    "Change only the fields the suggestion is about; set every other field to null. Translate faithfully: if the "
    "suggestion asks for detail verbatim or exactly as written, choose that option (e.g. context: keep); if it only asks "
    "to keep the gist ('keep that they work outdoors'), choose the most private option that still carries it (context: "
    "generalize). Do not enforce privacy rules yourself: the oversight agent re-tests every change. Use any retrieved "
    "policy rules to warn, in your explanation, when the requested detail is likely to fail the re-test, and cite them."
)


def interpret_suggestion(suggestion: str, current_policy: dict, note_excerpt: str = "", policy_context: str = "") -> dict:
    user = (f"Current policy: {json.dumps(current_policy)}\nSuggestion: {suggestion}\n"
            + (f"\nRelevant rules retrieved from the hospital policy library (follow them; cite their IDs):\n{policy_context}\n" if policy_context else "")
            + (f"\nRelease being discussed (excerpt):\n{note_excerpt[:1500]}" if note_excerpt else ""))
    ch, usage, refused = _parse(INHOUSE, SUGGEST_SYSTEM, user, PolicyChange, effort="low")
    if refused:
        return {"changes": {}, "explanation": "Could not interpret the suggestion.", "cited_rules": [], "usage": usage}
    changes = {k: v for k, v in ch.model_dump().items() if k not in ("explanation", "cited_rules") and v is not None}
    return {"changes": changes, "explanation": ch.explanation, "cited_rules": ch.cited_rules, "usage": usage}


# ------------------------------------------------------------------ synthetic vignettes
class Vignette(BaseModel):
    presentation: str = Field(description="HPI continuation, examination and investigations, 70-130 words. No name, age, sex, nationality, occupation, employer, country or dates.")
    context_keep: str = Field(description="One sentence of patient-specific context that changes the diagnosis, using ONLY these placeholders as needed: {occupation} {employer} {country} {month}. Empty string if no context.")
    context_generalized: str = Field(description="The same sentence generalised, using ONLY these placeholders as needed: {occupation_category} {region} {season}. Empty string if context_keep is empty.")
    context_dependence: Literal["low", "medium", "high"] = Field(description="How much the correct diagnosis depends on the context sentence")
    presentation_type: Literal["typical", "atypical"]
    main_look_alike: str = Field(description="The diagnosis this case is most easily confused with")


class VignetteSet(BaseModel):
    vignettes: List[Vignette]


def write_vignettes(condition: str, n: int, eligibility: str) -> dict:
    prompt = (
        f"Write {n} distinct synthetic emergency-department vignettes for: {condition}. Patients: {eligibility}.\n"
        "Purpose: test whether removing patient context from a note harms an AI's diagnosis. So:\n"
        "- Mix typical and atypical presentations (about half each).\n"
        "- In at least a third, the context sentence (occupation/exposure, travel, housing, timing) should be "
        "what tips the diagnosis away from a look-alike; mark those context_dependence='high'.\n"
        "- Use realistic vital signs and lab values with units. Do NOT state the diagnosis or its name.\n"
        f"- Look-alikes to consider: {', '.join(DISTRACTORS)} and the other conditions in: {', '.join(TARGET_CONDITIONS)}.\n"
        "- The presentation must not contain any name, age, sex word, nationality, job, employer, country, or date: "
        "those come from the record and the context sentence.\n"
        "- Placeholders are literal, in curly braces, exactly as listed in the field descriptions.")
    vs, usage, refused = _parse(OUTSIDER, "You write realistic synthetic clinical teaching cases.", prompt,
                                VignetteSet, effort="medium")
    return {"vignettes": [v.model_dump() for v in vs.vignettes] if vs else [], "usage": usage, "refused": refused}

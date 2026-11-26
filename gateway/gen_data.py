"""Synthetic population + clinical notes for the privacy-gateway prototype.

Everything here is fabricated. Names are drawn from common-name lists, employers
are fictional, and the ID formats are *modelled on* Qatari formats (11-digit QID
encoding century, birth year and nationality code; +974 8-digit phones; zone /
street / building addresses). No real person or record is represented.

Outputs (in data/):
  registry.json  - 2,000-person "leaked population directory": the attacker's
                   auxiliary knowledge (name, sex, age, nationality, occupation,
                   employer, municipality, zone).
  patients.json  - 84 patients drawn from the registry, each with a condition,
                   an encounter, an insurer claim, and a clinical note stored as
                   tagged segments (so every identifier has a gold span and a
                   rendering at each de-identification level).
"""
import json
import re
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 341
rng = random.Random(SEED)
OUT = Path(__file__).parent / "data"

# ---------------------------------------------------------------- reference data
# Nationality mix is illustrative (roughly shaped like Qatar's migrant-majority
# population); small groups are deliberately included to test the "uniqueness" risk.
NATIONALITIES = {
    # name: (weight, adjective, region, iso_numeric, name_pool)
    "Indian":      (21, "Indian",      "South Asia",          356, "south_asian"),
    "Nepali":      (13, "Nepali",      "South Asia",          524, "nepali"),
    "Bangladeshi": (12, "Bangladeshi", "South Asia",          50,  "bangla"),
    "Qatari":      (12, "Qatari",      "Gulf (GCC)",          634, "arab"),
    "Egyptian":    (9,  "Egyptian",    "Middle East & N. Africa", 818, "arab"),
    "Filipino":    (8,  "Filipino",    "Southeast Asia",      608, "filipino"),
    "Pakistani":   (6,  "Pakistani",   "South Asia",          586, "pakistani"),
    "Sri Lankan":  (5,  "Sri Lankan",  "South Asia",          144, "sri_lankan"),
    "Sudanese":    (3,  "Sudanese",    "Middle East & N. Africa", 729, "arab"),
    "Jordanian":   (3,  "Jordanian",   "Middle East & N. Africa", 400, "arab"),
    "Kenyan":      (2,  "Kenyan",      "Sub-Saharan Africa",  404, "kenyan"),
    "British":     (2,  "British",     "Europe",              826, "british"),
}

COUNTRY = {"Nepali": "Nepal", "Bangladeshi": "Bangladesh", "Indian": "India", "Pakistani": "Pakistan",
           "Filipino": "the Philippines", "Sri Lankan": "Sri Lanka", "Egyptian": "Egypt", "Sudanese": "Sudan",
           "Jordanian": "Jordan", "Kenyan": "Kenya", "British": "the UK", "Qatari": "Qatar"}

NAMES = {
    "arab": {
        "M": ["Mohammed", "Ahmed", "Khalid", "Hamad", "Abdulla", "Ali", "Youssef", "Omar", "Faisal", "Saad", "Jassim", "Tariq"],
        "F": ["Fatima", "Aisha", "Maryam", "Noora", "Hessa", "Mariam", "Layla", "Sara", "Reem", "Amna", "Dana", "Huda"],
        "last": ["Al-Kuwari", "Al-Thani", "Al-Marri", "Al-Mohannadi", "Al-Sulaiti", "Al-Hajri", "Hassan", "Mahmoud", "Ibrahim", "Abdelrahman", "Osman", "Haddad", "Nasser", "Saleh"],
    },
    "south_asian": {
        "M": ["Rahul", "Arjun", "Suresh", "Vijay", "Anil", "Rajesh", "Mohammed", "Joseph", "Sanjay", "Ramesh", "Abdul", "Thomas"],
        "F": ["Priya", "Anjali", "Deepa", "Lakshmi", "Meera", "Sunita", "Divya", "Reshma", "Mary", "Kavya", "Neha", "Shabana"],
        "last": ["Kumar", "Nair", "Menon", "Pillai", "Sharma", "Reddy", "Varghese", "Thomas", "Khan", "Iyer", "George", "Das", "Patel", "Joseph"],
    },
    "nepali": {
        "M": ["Ram", "Bishnu", "Krishna", "Hari", "Suman", "Dipak", "Prakash", "Bikash", "Ramesh", "Santosh"],
        "F": ["Sita", "Gita", "Sarita", "Kamala", "Anita", "Laxmi", "Puja", "Sabina"],
        "last": ["Thapa", "Gurung", "Tamang", "Shrestha", "Rai", "Magar", "Limbu", "Karki", "Bhandari", "Adhikari"],
    },
    "bangla": {
        "M": ["Abdul", "Rafiq", "Kamal", "Jahid", "Sohel", "Rubel", "Mizanur", "Habib", "Shahin", "Arif"],
        "F": ["Nasrin", "Shirin", "Rokeya", "Taslima", "Ruma", "Salma", "Fahima", "Jesmin"],
        "last": ["Hossain", "Rahman", "Islam", "Uddin", "Miah", "Akter", "Sarker", "Alam", "Chowdhury", "Begum"],
    },
    "filipino": {
        "M": ["Jose", "Mark", "John Paul", "Ronaldo", "Christian", "Jerome", "Rommel", "Arnel"],
        "F": ["Maria", "Joy", "Kristine", "Angelica", "Rowena", "Marites", "Jasmine", "Lorna"],
        "last": ["Santos", "Reyes", "Cruz", "Bautista", "Garcia", "Mendoza", "Dela Cruz", "Villanueva", "Ramos", "Aquino"],
    },
    "pakistani": {
        "M": ["Imran", "Asif", "Bilal", "Usman", "Zahid", "Kashif", "Naveed", "Waqas"],
        "F": ["Ayesha", "Sana", "Hina", "Rabia", "Saima", "Nadia"],
        "last": ["Khan", "Butt", "Malik", "Qureshi", "Chaudhry", "Iqbal", "Hussain", "Raza"],
    },
    "sri_lankan": {
        "M": ["Nimal", "Kasun", "Ruwan", "Chamara", "Saman", "Pradeep"],
        "F": ["Dilani", "Chathurika", "Nadeesha", "Sanduni", "Kumari"],
        "last": ["Perera", "Fernando", "Silva", "Jayasinghe", "Bandara", "Wickramasinghe"],
    },
    "kenyan": {
        "M": ["Brian", "Kevin", "Dennis", "Collins", "Samuel"],
        "F": ["Faith", "Mercy", "Grace", "Esther", "Joyce"],
        "last": ["Otieno", "Wanjiru", "Kamau", "Mwangi", "Achieng", "Kiprop", "Njoroge"],
    },
    "british": {
        "M": ["James", "Oliver", "Thomas", "Daniel", "Matthew"],
        "F": ["Emma", "Charlotte", "Sophie", "Hannah", "Lucy"],
        "last": ["Smith", "Taylor", "Brown", "Wilson", "Evans", "Hughes", "Walker"],
    },
}

# Fictional employers grouped by occupation category.
JOBS = [
    # occupation, category (generalised), outdoor, employers, sex_bias(M share)
    ("construction worker", "manual / outdoor work", True, ["Lusail Build Contracting", "Al Wakra Civil Works", "Desert Line Construction"], 0.99),
    ("site supervisor", "manual / outdoor work", True, ["Lusail Build Contracting", "Desert Line Construction"], 0.95),
    ("security guard", "manual / outdoor work", True, ["Falcon Guard Services", "Pearl Security Co."], 0.95),
    ("delivery driver", "manual / outdoor work", True, ["Swift Souq Delivery", "Corniche Couriers"], 0.98),
    ("landscaping worker", "manual / outdoor work", True, ["Green Dunes Landscaping"], 0.99),
    ("domestic worker", "domestic / care work", False, ["private household"], 0.10),
    ("nurse", "healthcare", False, ["Al Sadd Medical Centre", "Gulf Care Clinics"], 0.15),
    ("hotel staff", "hospitality / retail", False, ["Marina Bay Hotels", "Gulf Hospitality Group"], 0.6),
    ("retail assistant", "hospitality / retail", False, ["City Centre Retail LLC", "Souq Trading Co."], 0.6),
    ("engineer", "professional / office", False, ["Doha Tech Solutions", "Gulf Energy Services", "Al Wakra Civil Works"], 0.8),
    ("accountant", "professional / office", False, ["Doha Tech Solutions", "Pearl Finance House"], 0.6),
    ("teacher", "education", False, ["Corniche International School", "Al Rayyan Academy"], 0.35),
    ("government employee", "public sector", False, ["a government ministry"], 0.55),
]

MUNICIPALITIES = {  # synthetic zone ranges; not an official mapping
    "Doha": list(range(1, 60)), "Al Rayyan": list(range(51, 58)) + list(range(60, 72)),
    "Al Wakrah": list(range(90, 92)), "Umm Salal": list(range(71, 72)), "Al Khor": list(range(74, 75)),
    "Al Daayen": list(range(69, 71)),
}
MUNI_WEIGHTS = {"Doha": 45, "Al Rayyan": 30, "Al Wakrah": 10, "Umm Salal": 6, "Al Khor": 5, "Al Daayen": 4}

SENSITIVE_HISTORY = [
    ("HIV infection, on dolutegravir/lamivudine", "HIV"),
    ("major depressive disorder, on sertraline 50 mg", "depression"),
    ("chronic hepatitis B carrier", "hepatitis B"),
    ("epilepsy, on levetiracetam", "epilepsy"),
]


def weighted(d):
    keys = list(d)
    return rng.choices(keys, weights=[d[k] if not isinstance(d[k], tuple) else d[k][0] for k in keys])[0]


def make_qid(birth_year, iso):
    century = "2" if birth_year < 2000 else "3"
    return f"{century}{birth_year % 100:02d}{iso:03d}{rng.randint(0, 99999):05d}"


def make_phone():
    return f"+974 {rng.choice('3567')}{rng.randint(0, 999):03d} {rng.randint(0, 9999):04d}"


def make_person(pid, age=None, sex=None, nat=None, adult_job=True):
    nat = nat or weighted(NATIONALITIES)
    _, adj, region, iso, pool = NATIONALITIES[nat]
    if age is None:
        age = rng.choice([rng.randint(0, 5)] * 1 + [rng.randint(6, 17)] * 1 + [rng.randint(18, 60)] * 8 + [rng.randint(61, 80)] * 1)
    if age >= 18 and adult_job:
        job = rng.choice(JOBS)
        if nat == "Qatari":
            job = rng.choice([j for j in JOBS if j[0] in ("engineer", "government employee", "teacher", "accountant", "nurse")])
        sex = sex or ("M" if rng.random() < job[4] else "F")
        occupation, occ_cat, outdoor, employers = job[0], job[1], job[2], job[3]
        employer = rng.choice(employers)
        if age >= 62:
            occupation, occ_cat, outdoor, employer = "retired", "retired", False, "none"
    else:
        sex = sex or rng.choice("MF")
        occupation, occ_cat, outdoor, employer = ("student" if age >= 5 else "child"), ("student" if age >= 5 else "child"), False, "none"
    first = rng.choice(NAMES[pool][sex])
    last = rng.choice(NAMES[pool]["last"])
    muni = weighted(MUNI_WEIGHTS)
    zone = rng.choice(MUNICIPALITIES[muni])
    birth_year = 2026 - age
    return {
        "pid": pid, "name": f"{first} {last}", "first": first, "last": last, "sex": sex, "age": age,
        "birth_year": birth_year, "nationality": nat, "nat_adj": adj, "region": region,
        "qid": make_qid(birth_year, iso), "phone": make_phone(),
        "occupation": occupation, "occupation_category": occ_cat, "outdoor_work": outdoor,
        "employer": employer, "municipality": muni, "zone": zone,
        "street": rng.randint(200, 990), "building": rng.randint(1, 120),
    }


# ---------------------------------------------------------------- conditions
# Each condition: eligibility check, ICD-10 code, and note-content generator.
# Context lines that are BOTH identifying and clinically useful are tagged so the
# minimiser can keep, generalise or drop them per level - the crux of the trade-off.
CONDITIONS = {
    "Heat stroke": {"icd": "T67.0", "elig": lambda p: p["outdoor_work"] and 20 <= p["age"] <= 58},
    "Pre-eclampsia": {"icd": "O14.1", "elig": lambda p: p["sex"] == "F" and 20 <= p["age"] <= 40},
    "Ectopic pregnancy": {"icd": "O00.9", "elig": lambda p: p["sex"] == "F" and 19 <= p["age"] <= 40},
    "Kawasaki disease": {"icd": "M30.3", "elig": lambda p: 1 <= p["age"] <= 4},
    "Bronchiolitis": {"icd": "J21.9", "elig": lambda p: p["age"] == 0},
    "Asthma exacerbation": {"icd": "J45.9", "elig": lambda p: 6 <= p["age"] <= 40},
    "Acute myocardial infarction": {"icd": "I21.9", "elig": lambda p: p["age"] >= 42},
    "Pulmonary tuberculosis": {"icd": "A15.0", "elig": lambda p: 20 <= p["age"] <= 55 and p["nationality"] != "Qatari"},
    "Diabetic ketoacidosis": {"icd": "E10.1", "elig": lambda p: 8 <= p["age"] <= 30},
    "Acute appendicitis": {"icd": "K35.8", "elig": lambda p: 8 <= p["age"] <= 40},
    "Gout": {"icd": "M10.9", "elig": lambda p: p["sex"] == "M" and p["age"] >= 35},
    "Benign prostatic hyperplasia": {"icd": "N40", "elig": lambda p: p["sex"] == "M" and p["age"] >= 55},
}

SERVICES = {
    "Heat stroke": ["ED visit, level 5", "active cooling", "IV fluids", "serum electrolytes, CK"],
    "Pre-eclampsia": ["obstetric assessment", "IV labetalol", "magnesium sulfate infusion", "urine protein:creatinine ratio"],
    "Ectopic pregnancy": ["ED visit, level 4", "transvaginal ultrasound", "serum beta-hCG", "laparoscopic salpingectomy"],
    "Kawasaki disease": ["paediatric admission", "echocardiogram", "IV immunoglobulin", "high-dose aspirin"],
    "Bronchiolitis": ["paediatric ED visit", "nasal suction", "high-flow oxygen", "nasopharyngeal viral panel"],
    "Asthma exacerbation": ["ED visit, level 3", "nebulised salbutamol", "oral prednisolone", "peak flow"],
    "Acute myocardial infarction": ["ED visit, level 5", "12-lead ECG", "troponin", "primary PCI"],
    "Pulmonary tuberculosis": ["chest X-ray", "sputum AFB smear x3", "GeneXpert MTB/RIF", "airborne isolation admission"],
    "Diabetic ketoacidosis": ["ED visit, level 5", "insulin infusion", "blood gas", "serum ketones"],
    "Acute appendicitis": ["ED visit, level 4", "CT abdomen", "laparoscopic appendectomy"],
    "Gout": ["ED visit, level 2", "serum uric acid", "colchicine"],
    "Benign prostatic hyperplasia": ["urology clinic visit", "PSA", "bladder ultrasound (post-void residual)", "tamsulosin"],
}


def seg(text, tag=None, **levels):
    """A note segment. `levels` maps 'L1'/'L2'/'L3' -> rendering at that level
    (a level falls back to the previous level's rendering, L0 = text)."""
    return {"text": text, "tag": tag, **levels}


def S(text):
    return seg(text)


def clinical_body(cond, p, visit):
    """Returns (segments for HPI / history / exam / investigations, med list)."""
    a, he = p["age"], ("He" if p["sex"] == "M" else "She")
    his = "his" if p["sex"] == "M" else "her"
    occ_ctx = lambda txt, l2, l3="": seg(txt, "OCC_CONTEXT", L2=l2, L3=l3)
    b = []
    if cond == "Heat stroke":
        b += [S(f"{he} collapsed "), occ_ctx(f"while working as a {p['occupation']} at {p['employer']} ", "during outdoor manual work ", ""),
              seg(f"on a {visit.strftime('%B')} afternoon", "SEASON", L2="on a summer afternoon", L3="earlier today"),
              S(". Colleagues reported confusion and slurred speech before collapse. On arrival GCS 11, core temperature 41.4 °C, HR 132, BP 96/58, RR 28. Skin hot and dry. No neck stiffness. Labs: Na 149, CK 2,850 U/L, creatinine 168 µmol/L, glucose 6.2 mmol/L. CT head normal.")]
    elif cond == "Pre-eclampsia":
        b += [S(f"G2P1 at 33 weeks' gestation, presents with severe frontal headache and blurred vision for 6 hours, with new swelling of face and hands. BP 168/112 on repeat, HR 94. Urine dipstick protein 3+, protein:creatinine ratio 410 mg/mmol. Platelets 118, ALT 74. Brisk reflexes with 2 beats of clonus. Fetal CTG reassuring.")]
    elif cond == "Ectopic pregnancy":
        b += [S("Presents with 2 days of left-sided lower abdominal pain and light vaginal spotting; last menstrual period 7 weeks ago. Shoulder-tip pain this morning. HR 112, BP 98/62. Tender left iliac fossa with guarding, cervical excitation. Urine hCG positive, serum beta-hCG 2,340 IU/L. Transvaginal ultrasound: empty uterus, left adnexal mass with free fluid.")]
    elif cond == "Kawasaki disease":
        b += [S(f"Brought by {his} mother with 6 days of high fever (to 39.8 °C) unresponsive to antipyretics. Bilateral non-purulent conjunctival injection, cracked red lips, polymorphous truncal rash, swollen hands and feet with peeling of fingertips, and a 2 cm unilateral cervical lymph node. Irritable. CRP 142, platelets 520, ALT 61, albumin 29. Urinalysis: sterile pyuria.")]
    elif cond == "Bronchiolitis":
        b += [S("Brought by parents with 3 days of coryza and cough, now with fast breathing and reduced feeding (about half of usual feeds). RR 62, SpO2 91% on air, HR 168, T 38.1 °C. Subcostal and intercostal recession, nasal flaring, widespread fine inspiratory crackles and expiratory wheeze. First episode; no prior wheeze. Older sibling has a cold.")]
    elif cond == "Asthma exacerbation":
        b += [S(f"Known history of wheeze since childhood, presents with 1 day of worsening breathlessness and chest tightness after a dust storm. Speaking in short phrases. RR 30, SpO2 92% on air, HR 118, peak flow 45% of predicted. Diffuse bilateral expiratory wheeze. Afebrile. Uses salbutamol inhaler, not on a preventer.")]
    elif cond == "Acute myocardial infarction":
        b += [S("Presents with 90 minutes of central crushing chest pain radiating to the left arm and jaw, with sweating and nausea. Smoker, type 2 diabetes. HR 104, BP 152/94. ECG: ST elevation in leads II, III, aVF with reciprocal depression in I and aVL. High-sensitivity troponin T 412 ng/L.")]
    elif cond == "Pulmonary tuberculosis":
        b += [S("Presents with productive cough for 5 weeks, intermittent haemoptysis, drenching night sweats and 7 kg weight loss. "),
              seg(f"Arrived in Qatar from {COUNTRY[p['nationality']]} 4 months ago and shares a room with 7 co-workers in labour accommodation. ",
                  "TRAVEL_HOUSING", L2="Recent arrival (4 months) from a high-TB-incidence region; lives in crowded shared accommodation. ", L3=""),
              S("T 38.0 °C, SpO2 95%. Crackles at the right apex. CXR: right upper lobe cavitating consolidation. Sputum smear positive for acid-fast bacilli. HIV test pending.")]
    elif cond == "Diabetic ketoacidosis":
        b += [S("Presents with 3 days of thirst, passing large amounts of urine, vomiting and abdominal pain; 4 kg weight loss over 3 weeks. Deep sighing respiration, ketotic breath, dry mucous membranes. HR 126, BP 102/64. Capillary glucose 31.6 mmol/L, blood ketones 5.8 mmol/L, venous pH 7.08, bicarbonate 7.")]
    elif cond == "Acute appendicitis":
        b += [S("Presents with 18 hours of abdominal pain that began around the umbilicus and moved to the right iliac fossa, with anorexia and one episode of vomiting. T 38.2 °C, HR 104. Tenderness and guarding at McBurney's point, positive Rovsing's sign. WCC 15.8, CRP 64. Urinalysis unremarkable.")]
    elif cond == "Gout":
        b += [S("Presents with sudden-onset severe pain, redness and swelling of the right first metatarsophalangeal joint overnight; cannot bear a bed sheet touching it. Similar episode last year. Drinks sugary soft drinks daily; on hydrochlorothiazide. T 37.6 °C. Joint hot, swollen, exquisitely tender. Serum urate 0.56 mmol/L, CRP 48.")]
    elif cond == "Benign prostatic hyperplasia":
        b += [S("Presents with 8 months of urinary frequency, nocturia 3-4 times nightly, hesitancy, weak stream and terminal dribbling. No haematuria, no weight loss. DRE: smooth, symmetrically enlarged, non-tender gland, no nodules. Post-void residual 160 mL. PSA 2.9 ng/mL. Urine dipstick negative.")]
    return b


VIGNETTES_PATH = OUT / "vignettes.json"
VIGNETTES = json.loads(VIGNETTES_PATH.read_text()) if VIGNETTES_PATH.exists() else None
KEEP_REVEALS = {"occupation": "occupation", "employer": "employer", "country": "nationality"}
GEN_REVEALS = {"occupation_category": "occupation_category", "region": "region"}


def placeholders(t):
    return set(re.findall(r"\{(\w+)\}", t))


def compatible(v, p):
    keep = placeholders(v["context_keep"])
    if keep & {"occupation", "employer"} and (p["age"] < 18 or p["occupation"] in ("retired", "student", "child")):
        return False
    if "country" in keep and p["nationality"] == "Qatari":
        return False
    return True


def fill(t, mapping):
    t = re.sub(r"\{(\w+)\}", lambda m: str(mapping.get(m.group(1), m.group(1).replace("_", " "))), t)
    return t.replace("{", "").replace("}", "")


def vignette_body(v, p, visit):
    """HPI context sentence (tagged CONTEXT: keep / generalize / remove) + presentation."""
    season = "summer" if visit.month in (5, 6, 7, 8, 9) else "winter"
    keep = fill(v["context_keep"], {"occupation": p["occupation"], "employer": p["employer"],
                                         "country": COUNTRY.get(p["nationality"], "abroad"),
                                         "month": visit.strftime("%B")}) if v["context_keep"] else ""
    gen = fill(v["context_generalized"], {"occupation_category": p["occupation_category"],
                                               "region": p["region"], "season": season}) if v["context_generalized"] else ""
    reveals = {"keep": sorted({KEEP_REVEALS[k] for k in placeholders(v["context_keep"]) if k in KEEP_REVEALS}),
               "generalize": sorted({GEN_REVEALS[k] for k in placeholders(v["context_generalized"]) if k in GEN_REVEALS})}
    # words that imply the occupation category even without a placeholder
    if p["age"] >= 18 and re.search(r"outdoor|manual|construction|labou?r|site work", gen, re.I):
        reveals["generalize"] = sorted(set(reveals["generalize"]) | {"occupation_category"})
    if p["age"] >= 18 and re.search(r"outdoor|manual|construction|labou?r|site work", keep, re.I):
        reveals["keep"] = sorted(set(reveals["keep"]) | {"occupation_category"})
    b = []
    if keep:
        b.append(seg(keep.strip() + " ", "CONTEXT", L1=keep.strip() + " ", L2=(gen.strip() + " ") if gen else "", L3=""))
    b.append(S(v["presentation"].strip()))
    return b, reveals


def build_note(p, cond, visit, sensitive, relative, vignette=None):
    dob = date(p["birth_year"], rng.randint(1, 12), rng.randint(1, 28))
    age_txt = f"{p['age']}" if p["age"] >= 1 else f"{rng.randint(4, 11)} months"
    age_word = f"{age_txt}-year-old" if p["age"] >= 1 else f"{age_txt}-old"
    sex_word = {"M": "man" if p["age"] >= 18 else "boy", "F": "woman" if p["age"] >= 18 else "girl"}[p["sex"]]
    if p["age"] == 0:
        sex_word = "infant " + ("boy" if p["sex"] == "M" else "girl")
    age_band = "under 1 year" if p["age"] == 0 else ("1-4 years" if p["age"] < 5 else f"{(p['age'] // 10) * 10}-{(p['age'] // 10) * 10 + 9}")
    age_coarse = "infant" if p["age"] == 0 else "child" if p["age"] < 18 else "older adult" if p["age"] >= 60 else "adult"
    mrn = f"{rng.randint(1000000, 9999999)}"

    segs = [
        S("EMERGENCY DEPARTMENT CLINICAL NOTE\nDate of visit: "),
        seg(visit.strftime("%d %B %Y"), "DATE", L1="[DATE]", L2=f"[DATE] ({'summer' if visit.month in (5,6,7,8,9) else 'winter'})", L3="[DATE]"),
        S("\nPatient: "), seg(p["name"], "NAME", L1="[NAME]"),
        S("    QID: "), seg(p["qid"], "QID", L1="[QID]"),
        S("    MRN: "), seg(mrn, "MRN", L1="[MRN]"),
        S("\nDOB: "), seg(dob.strftime("%d/%m/%Y"), "DOB", L1="[DOB]"),
        S("    Age: "), seg(age_txt, "AGE", L2=age_band, L3=age_coarse),
        S("    Sex: " + ("Male" if p["sex"] == "M" else "Female")),
        S("\nNationality: "), seg(p["nationality"], "NATIONALITY", L2=p["region"], L3="[REMOVED]"),
        S("\nAddress: "), seg(f"Zone {p['zone']}, Street {p['street']}, Building {p['building']}, {p['municipality']}", "ADDRESS", L1="[ADDRESS]"),
        S("\nPhone: "), seg(p["phone"], "PHONE", L1="[PHONE]"),
    ]
    if p["age"] >= 18:
        segs += [S("\nOccupation: "), seg(f"{p['occupation']}, {p['employer']}", "OCCUPATION", L2=p["occupation_category"], L3="[REMOVED]")]
    if relative:
        segs += [S("\nAccompanied by: "), seg(f"{relative['relation']} {relative['name']}", "RELATIVE", L1=f"{relative['relation']} [NAME]"),
                 S(" ("), seg(relative["phone"], "PHONE", L1="[PHONE]"), S(")")]
    segs += [S("\n\nHISTORY OF PRESENTING ILLNESS\n"),
             seg(age_word, "AGE", L2=f"{age_band.replace(' years','')}-year-old" if p['age'] >= 1 else "infant", L3=age_coarse.capitalize()),
             S(" "),
             seg(p["nat_adj"] + " ", "NATIONALITY", L2="", L3=""),
             S(sex_word),
             seg(f", lives in Zone {p['zone']}, {p['municipality']}", "ADDRESS", L1=f", lives in {p['municipality']}", L2=f", lives in {p['municipality']}", L3=""),
             S(". ")]
    reveals = {"keep": [], "generalize": []}
    if vignette:
        body, reveals = vignette_body(vignette, p, visit)
        segs += body
    else:
        segs += clinical_body(cond, p, visit)
        if cond == "Heat stroke":
            reveals = {"keep": ["employer", "occupation"], "generalize": []}
        if cond == "Pulmonary tuberculosis":
            reveals = {"keep": ["nationality"], "generalize": []}
    pmh = sensitive[0] if sensitive else "nil significant"
    segs += [S("\n\nPAST MEDICAL HISTORY\n"), seg(pmh, "SENSITIVE_HX" if sensitive else None)]
    segs += [S("\n\nASSESSMENT AND PLAN\nWorking diagnosis withheld for review. Admit / treat per protocol; senior review requested.\nAttending: "),
             seg(f"Dr. {rng.choice(['Hessa', 'Rajesh', 'Maryam', 'Omar', 'Lucy', 'Samuel'])} {rng.choice(['Al-Marri', 'Nair', 'Haddad', 'Walker', 'Otieno', 'Santos'])}", "CLINICIAN", L1="[CLINICIAN]")]

    # fill level renderings with fallback L0 -> L1 -> L2 -> L3
    for s in segs:
        prev = s["text"]
        for lv in ("L1", "L2", "L3"):
            if lv not in s:
                s[lv] = prev
            prev = s[lv]
    return segs, dob, mrn, reveals


def render(segs, level):
    key = "text" if level == "L0" else level
    return "".join(s[key] for s in segs)


def main():
    OUT.mkdir(exist_ok=True)
    # registry with enough people in each clinical niche
    people = []
    for i in range(1850):
        people.append(make_person(f"P{i:04d}"))
    for i in range(1850, 1900):         # infants / toddlers
        people.append(make_person(f"P{i:04d}", age=rng.choice([0, 0, 0, 1, 2, 3, 4])))
    for i in range(1900, 1950):         # older men
        people.append(make_person(f"P{i:04d}", age=rng.randint(55, 78), sex="M"))
    for i in range(1950, 2000):         # women of reproductive age
        people.append(make_person(f"P{i:04d}", age=rng.randint(20, 40), sex="F"))
    rng.shuffle(people)

    patients, used = [], set()
    per_cond = 10
    for cond, meta in CONDITIONS.items():
        pool = [p for p in people if p["pid"] not in used and meta["elig"](p)]
        rng.shuffle(pool)
        vigs = list(VIGNETTES.get(cond, [])) if VIGNETTES else []
        rng.shuffle(vigs)
        used_v = set()
        for p in pool[:per_cond]:
            used.add(p["pid"])
            vignette = None
            if vigs:
                options = [i for i, v in enumerate(vigs) if compatible(v, p)]
                fresh = [i for i in options if i not in used_v]
                pick = (fresh or options or [None])[0]
                if pick is not None:
                    used_v.add(pick)
                    vignette = vigs[pick]
                else:
                    vignette = {**vigs[0], "context_keep": "", "context_generalized": ""}
            visit = date(2026, 1, 1) + timedelta(days=rng.randint(0, 300))
            if cond == "Heat stroke":
                visit = date(2026, rng.choice([6, 7, 8]), rng.randint(1, 28))
            sensitive = rng.choice(SENSITIVE_HISTORY) if (p["age"] >= 18 and rng.random() < 0.3) else None
            relative = None
            if p["age"] < 18 or rng.random() < 0.35:
                rel_sex = rng.choice("MF")
                pool_name = NATIONALITIES[p["nationality"]][4]
                relative = {"relation": ("father" if rel_sex == "M" else "mother") if p["age"] < 18 else ("brother" if rel_sex == "M" else "sister"),
                            "name": f"{rng.choice(NAMES[pool_name][rel_sex])} {p['last']}", "phone": make_phone()}
            segs, dob, mrn, reveals = build_note(p, cond, visit, sensitive, relative, vignette)
            patients.append({
                "pid": p["pid"], "condition": cond, "icd10": meta["icd"], "visit_date": visit.isoformat(),
                "sensitive_history": sensitive[1] if sensitive else None,
                "person": p, "dob": dob.isoformat(), "mrn": mrn, "relative": relative,
                "insurance_policy": f"QIC-{rng.randint(100000, 999999)}",
                "services": SERVICES[cond], "charges_qar": rng.randint(8, 120) * 100,
                "segments": segs, "context_reveals": reveals,
                "vignette": {k: vignette[k] for k in ("context_dependence", "presentation_type", "main_look_alike")} if vignette else None,
                "notes": {lv: render(segs, lv) for lv in ("L0", "L1", "L2", "L3")},
            })

    registry = [{k: p[k] for k in ("pid", "name", "sex", "age", "nationality", "region", "occupation",
                                   "occupation_category", "employer", "municipality", "zone")} for p in people]
    (OUT / "registry.json").write_text(json.dumps(registry, indent=1, ensure_ascii=False))
    (OUT / "patients.json").write_text(json.dumps(patients, indent=1, ensure_ascii=False))
    from collections import Counter
    print(f"registry={len(registry)} patients={len(patients)}")
    print(Counter(p["condition"] for p in patients))
    print(Counter(p["person"]["nationality"] for p in patients))


if __name__ == "__main__":
    main()

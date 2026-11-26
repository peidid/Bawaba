# Bawaba gateway rules (DRAFT for the governance lead)
version: 0.3 · 2026-11-26 (oversight agent; rules as data; stakeholder profiles; DP option)
owner: Data Protection Officer, with the Data & AI Governance Committee

These are the rules the gateway works by. They are data, not code: the oversight agent retrieves
their text to decide and to explain, and the guardrail verifier reads their "Param:" lines to check
every decision. Changing a number here (for example k_min) changes the gateway's behaviour on the
next request, with no code change and no retraining. Who receives what is set out per recipient in
stakeholders.md.

## General

### GW-GEN-01 · Purpose-specific minimization per channel
Applies to: all channels · minimizer, oversight
Source: PDPPL data-minimisation and purpose-limitation duties; contextual integrity
Each outbound channel has its own release profile (stakeholders.md). A record leaves only in the form that
channel's purpose needs: the AI diagnostic tool gets a de-identified clinical note, the insurer gets a
structured claim, the Ministry of Public Health gets aggregate tables (named reports only where the law
requires them). A release built for one channel may not be reused for another.

### GW-GEN-02 · Every release level is still personal data
Applies to: all channels · oversight, minimizer
Source: PDPPL definition of personal data; WP29 Opinion 05/2014 (singling out, linkability, inference)
De-identified and generalized releases are treated as personal data of a special nature unless a
re-identification test shows otherwise. The gateway lowers re-identification risk; it never declares data
anonymous on its own.

## AI diagnostic channel

### GW-AI-01 · Direct identifiers never leave
Applies to: ai_diagnosis · minimizer, oversight · guardrail
Source: PDPPL security and minimisation duties; HIPAA Safe Harbor list (reference only)
Param: never_release = NAME, QID, MRN, DOB, DATE, PHONE, ADDRESS, RELATIVE, CLINICIAN
Names, Qatar ID numbers, medical record numbers, dates of birth, exact visit dates, phone numbers,
street-level addresses, relatives' names and clinician names are always removed before release, in every
draft, whatever the field policy.

### GW-AI-02 · Re-identification floor: at least k_min people match and the red team fails
Applies to: ai_diagnosis · oversight, red_team · guardrail
Source: k-anonymity practice; small-cell thresholds of 5 used by statistical agencies
Param: k_min = 5
Param: red_team_must_fail = true
A draft passes the privacy test only if at least k_min people in the reference population directory match
everything the draft reveals AND the red-team attacker fails to single out the patient. If either fails, the
draft may not be released; the oversight agent decides how to redraft it. Small nationality groups are
expected to need more generalization, and the agent may raise k_min for a case (GW-OV-02).

### GW-AI-03 · Utility test: the diagnosis must survive minimization
Applies to: ai_diagnosis · oversight, utility_team · guardrail
Source: clinical safety duty of care; minimum-necessary principle
Param: utility_must_hold = true
A draft passes the utility test if the diagnostic tool's top answer on the draft matches its top answer
on the full note (in certification), or the in-house model's answer (at runtime). The full note never
leaves the hospital for this test.

### GW-AI-04 · Least restrictive passing release, chosen by the oversight agent
Applies to: ai_diagnosis · oversight
Source: proportionality; PDPPL minimisation
The oversight agent starts from the channel's certified policy. After a failed test it decides which fields
to generalize, using what the red team exploited and what the diagnosis depends on, and checks candidate
policies locally before asking for a redraft. It aims for the least restrictive draft that passes both tests:
keep the clinical context that drives the diagnosis, generalize or remove what singles the patient out. The
fixed ladder (L1 to L2 to L3) is kept only as the baseline the agent is evaluated against.

## Oversight agent and rule changes

### GW-OV-01 · The oversight agent decides; guardrails verify
Applies to: all channels · oversight · guardrail
Source: PDPPL controller accountability (Art. 11); human oversight of AI (LAW-AI); defence in depth
Param: max_drafts = 6
Param: redraft_needs_local_k = true
Param: review_tested_drafts_only = true
Param: block_needs_most_private_tested = true
Release decisions are made by an AI agent that reads the case, retrieves the rules, tests options with its
tools and gives a reason that cites rule IDs. Every decision then passes a verifier that only checks the
Param values of the rules in force (k_min, the red-team result, the diagnosis, mandatory human review,
the number of drafts). The verifier holds no decision logic; when it refuses, the agent is told why and must
decide again, and every refusal is logged. The agent cannot release past a guardrail; only a human can, under
GW-HITL-04. Two further checks keep the agent from shifting work onto people or giving up early: a human is
only asked to review a draft that has been tested and passed (otherwise the agent must redraft or escalate),
and the agent may only block after the most private policy has been tested.

### GW-OV-02 · Rules can change: the agent proposes, people approve
Applies to: all channels · oversight, governance
Source: privacy by design; PDPPL accountability; change control in DPIA practice
Param: tighten_applies_now = true
Param: loosen_requires = DPO
When a case shows a rule is too loose (the attacker nearly succeeded), too strict (a needed detail is
always lost), or missing for a stakeholder, the oversight agent proposes an amendment: the rule, the
parameter, the new value and the reason. A tightening applies to the current case at once and goes to the
governance committee for adoption. A loosening applies to nothing until the DPO approves it and the channel
is re-certified (GW-CERT-01). Adopted amendments are new versions of this file.

### GW-OV-03 · Government requirements are read at decision time, not hard-coded
Applies to: all channels · oversight, governance
Source: Decree-Law No. 17 of 1990 as amended; PDPPL; MoPH circulars (see LAW-NOTIFIABLE, LAW-SMALLCELL)
When the law or a Ministry circular changes (a disease becomes notifiable, a cell threshold changes, a new
consent rule), the DPO edits the relevant rule or profile. Agents and the verifier read the new version on
the next request, and the audit log records which version of each file every decision used.

## Human in the loop

### GW-HITL-01 · When a human must review before release
Applies to: ai_diagnosis · oversight, human · guardrail
Source: PDPPL controller accountability; JCI release-of-information expectations
Param: human_review_if = small_group, sensitive_history, loosened_by_human, escalated
Param: spot_check_rate = 0.05
A treating clinician or the Data Protection Officer must review before release when: oversight escalates;
the record contains a sensitive history (for example HIV, mental health, hepatitis B, epilepsy); the patient
belongs to a small nationality group; anyone asks to loosen a release; or a random 5% spot check selects it.

### GW-HITL-02 · Escalation when privacy and utility conflict
Applies to: ai_diagnosis · oversight, human
Source: clinical governance; PDPPL accountability
If no draft the agent can find is both private enough and diagnostically faithful, oversight escalates to the
treating clinician and the DPO with a memo describing what was tried and two options. The record is not
released until they decide.

### GW-HITL-03 · Human requests are re-tested, and unsafe requests are generalized
Applies to: ai_diagnosis · minimizer, oversight, human · guardrail
Source: privacy by design; automation-bias safeguards
Every change a human asks for is redrafted and re-tested before release. If the requested detail fails the
privacy test, the oversight agent keeps as much of the request as it can: it generalizes the requested fields
(for example keep context verbatim becomes keep context generalized) or compensates with other fields, re-tests,
and tells the human what it changed. Humans steer the release; they cannot skip the tests.

### GW-HITL-04 · Overriding a failed privacy test
Applies to: ai_diagnosis · human, oversight
Source: PDPPL Arts. 4, 19(2), 19(3); Law No. 2 of 1983 Art. 20 (see LAW-PDPPL-04-19, LAW-SECRECY). An override never replaces the Art. 16 permit or the Art. 9 notice
Only the Data Protection Officer may release a draft that failed the privacy test, and only with a recorded
legal basis (for example explicit patient consent, vital interests, or a legal obligation) and a written
reason. Clinicians may not override. Every override is flagged in the audit log and reviewed by the
governance committee.

### GW-HITL-05 · Stricter is easy, looser is hard
Applies to: all channels · human, oversight
Source: privacy by default
Making a release stricter takes one action. Making it looser requires a stated reason and a re-test.
Override rates per reviewer are monitored to detect rubber-stamping.

## Insurer billing channel

### GW-BIL-01 · Insurers receive a structured claim, never the clinical note
Applies to: insurer_billing · minimizer, oversight · guardrail
Source: QNHI Data Management Directive §§5, 7, 8; MoPH Decision No. 8 of 2022 (see LAW-INSURANCE). Licensed, registered recipients only; data stays in Qatar
Param: claim_fields = member_name, qid, policy_number, date_of_service, icd10_billed, services, charges
Claims contain member identity, policy number, date of service, billed ICD-10 codes, services and
charges. Free-text notes, past medical history and unbilled conditions are not sent. Medical-necessity
documentation, if requested, goes through GW-BIL-03.

### GW-BIL-02 · No inference beyond the claim
Applies to: insurer_billing · red_team, oversight
Source: no Qatari underwriting ban found; QNHI §6 (de-identified secondary use); EU EHDS Art. 54 as benchmark. Enforced as a contract term
Each claim template is tested by an insurer-analyst attack: if the analyst can infer a condition that was
not billed, the template is revised before use.

### GW-BIL-03 · When an insurer asks for more information
Applies to: insurer_billing · oversight, human
Source: QNHI Data Management Directive (see LAW-INSURANCE); PDPPL purpose limitation
Param: extra_info_requires = DPO
An insurer may ask for more than the claim, for example for a medical-necessity review or a fraud inquiry.
The oversight agent then prepares the minimum extract that answers the stated question, limited to the
billed condition: no unbilled conditions, no history, no medications that reveal other conditions. The DPO
reviews the extract before it leaves, and every such request is logged. Repeated requests from one insurer
trigger a governance review. This is the dilemma of the billing channel: the insurer's duty to check claims
against the patient's right that unrelated illnesses stay private.

## Ministry of Public Health reporting

### GW-MOPH-01 · Aggregate reporting with small-cell protection
Applies to: moph_reporting · oversight · guardrail
Source: statistical disclosure control; cell threshold of 5; differential privacy (Dwork & Roth 2014)
Param: cell_min = 5
Param: method = suppress
Param: dp_epsilon = 1.0
Statistical extracts are aggregated. With method = suppress, any cell with a count below cell_min is
suppressed or the table is coarsened (for example dropping age band or merging municipalities). With
method = dp, every count gets Laplace noise of scale 1/dp_epsilon instead, so small cells can be published
without any one patient changing the table much. Under review by the governance lead: benchmarks suppress
counts up to 10 (CMS), so 5 needs a written justification (see LAW-SMALLCELL).

### GW-MOPH-02 · Named notifiable-disease reports under legal obligation
Applies to: moph_reporting · oversight · guardrail
Source: Decree-Law No. 17 of 1990 as amended by Law No. 9 of 2020; PDPPL Art. 19(2) (see LAW-NOTIFIABLE). Named reports go via SAVES, outside de-identification
Param: notifiable = Pulmonary tuberculosis
Identified reports go to the Ministry only for diseases the law makes notifiable (for example
tuberculosis), within the legal time limit, with the legal basis recorded for each report.

## Vendors, audit and certification

### GW-VEN-01 · AI vendor terms before any data flows
Applies to: ai_diagnosis · governance
Source: PDPPL Arts. 11(8), 12, 13, 15, 28; NCSA Controller and Processor Guideline (see LAW-PDPPL-08-13, LAW-CLOUD). Vendor breach notice within 24 hours
The external AI vendor must contractually agree to: no training on hospital data, no retention beyond the
request, named processing location, approved sub-processors only, breach notification, audit rights and
deletion on request.

### GW-AUD-01 · Everything is logged
Applies to: all channels · oversight
Source: PDPPL Arts. 11(5), 11(7); JCI MOI.01.01; NIA Standard V2.1 logging (see LAW-PDPPL-14)
Every draft, test result, oversight decision and its reasons, guardrail check, rule-change proposal, human
action, retrieved rule and policy version is written to an append-only audit log, kept for the hospital's
records-retention period and reviewed monthly.

### GW-CERT-01 · Certification and re-certification of channel policies
Applies to: all channels · governance, oversight
Source: privacy by design; DPIA practice
A channel policy goes live only after an offline certification run on synthetic records (utility and
red-team tests), signed off by the DPO. Any change to a rule, a recipient, the oversight agent's model or
instructions, or any other model triggers re-certification.

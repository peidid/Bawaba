# Stakeholder release profiles: who gets what, and what never leaves
version: 0.3 · 2026-11-26
owner: Data Protection Officer, with the Data & AI Governance Committee

Each recipient gets a different slice of the same record. The AI tool needs the clinical picture
but not the person; the insurer needs the person and the bill but not the clinical story; the
Ministry needs counts, and names only where the law requires them. The oversight agent reads the
profile of the channel it is deciding for; the verifier enforces the parameters of the rules each
profile lists under "Enforces".

### STK-AI · External AI diagnostic tool (vendor)
Applies to: ai_diagnosis · oversight, minimizer · profile
Source: GW-GEN-01; GW-AI-01..04; GW-VEN-01; LAW-PDPPL-16; LAW-PDPPL-08-13; LAW-CLOUD
Param: channel = ai_diagnosis
Recipient: an external diagnostic AI service run by a vendor (a data processor under contract)
Purpose: diagnostic decision support for the treating clinician
Needs: symptoms, vital signs, lab values and examination findings, plus work, travel and season context in the most general form that still supports the diagnosis
Receives: one de-identified note per request; the oversight agent chooses each field's setting (age, nationality, occupation, context, address) for this record
Never: name, Qatar ID, medical record number, date of birth, exact dates, phone, street address, names of relatives or clinicians; any combination of details shared by fewer than k_min people; any use of the data for training the vendor's models
On request: more detail only when the treating clinician asks for it, and only after a re-test (GW-HITL-03); a failed privacy test can be overridden only by the DPO with a legal basis (GW-HITL-04)
Enforces: GW-AI-01, GW-AI-02, GW-AI-03, GW-HITL-01
Legal basis: health-data permit (LAW-PDPPL-16); processor contract and security duties (LAW-PDPPL-08-13); data residency and keys (LAW-CLOUD)

### STK-INS · Health insurer
Applies to: insurer_billing · oversight · profile
Source: GW-BIL-01..03; LAW-INSURANCE; LAW-PDPPL-04-19
Param: channel = insurer_billing
Recipient: a licensed health insurer in the national scheme, paying the claim
Purpose: paying the claim for a covered member
Needs: who was treated, which covered service was given, the billed diagnosis that justifies it, and the charge
Receives: a structured claim: member name and Qatar ID, policy number, date of service, billed ICD-10 code(s), services, charges
Never: the free-text clinical note; past medical history; conditions that were not billed (for example HIV, depression, hepatitis B); medications or results that reveal an unbilled condition; family history; anything used for underwriting or premium setting
On request: for a medical-necessity review or a fraud inquiry, a short extract limited to the billed condition and the stated purpose, prepared by the oversight agent and reviewed by the DPO before release (GW-BIL-03)
Enforces: GW-BIL-01, GW-BIL-02, GW-BIL-03
Legal basis: insurance-data directive and consent (LAW-INSURANCE); lawful purpose (LAW-PDPPL-04-19)

### STK-MOPH · Ministry of Public Health
Applies to: moph_reporting · oversight · profile
Source: GW-MOPH-01..02; LAW-NOTIFIABLE; LAW-SMALLCELL; LAW-PDPPL-04-19
Param: channel = moph_reporting
Recipient: the Ministry's surveillance and communicable-disease control units
Purpose: public-health surveillance and control of notifiable diseases
Needs: counts of conditions by place, time and age band; for a notifiable disease, the patient's identity and contact details so contacts can be traced within the legal time limit
Receives: weekly aggregate tables (condition x municipality x age band) with small cells suppressed or protected by differential privacy; named notifications only for notifiable diseases, through the Ministry's reporting system
Never: identified records for conditions that are not notifiable; table cells with fewer than cell_min people unless protected by differential privacy; free-text notes
On request: research extracts go through the research-ethics route (LAW-RESEARCH), not this channel
Enforces: GW-MOPH-01, GW-MOPH-02
Legal basis: notifiable-disease law (LAW-NOTIFIABLE); legal obligation of the controller (LAW-PDPPL-04-19); disclosure-control benchmarks (LAW-SMALLCELL)

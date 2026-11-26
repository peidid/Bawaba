# Legal and regulatory provisions (Qatar, onshore) — MVP extract
version: 0.1-draft · 2026-11-22
source: reports/Qatar hospital data governance policy.md (student research; not legal advice)

Verification tags: [P] primary text read · [Q] primary wording seen only as quoted · [S] secondary source · [U] unverified.

## PDPPL (Law No. 13 of 2016)

### LAW-PDPPL-01 · De-identified data stays personal data if identity can be reasonably defined
Applies to: law · all channels
Source: PDPPL Art. 1 [P]
Personal data includes data from which identity "can be reasonably defined" through the combination of
such data with any other data. A minimised note the hospital can re-link to the patient, or one that an
outsider could link with a population directory, is still personal data and still health data.

### LAW-PDPPL-16 · Health data needs a permit from the privacy regulator
Applies to: law · all channels
Source: PDPPL Arts. 16, 24 [P]; NCSA Advisory Note s.7.8 (Oct 2025) [P]
Data on health, physical or psychological condition is personal data of a special nature. It may be
processed only after permission from the Competent Department (NCSA's Personal Data Privacy Protection
Department). Procedure: record the processing, identify a permitted reason plus an additional condition,
complete a privacy impact assessment, and submit the permit request. Breach: fine up to QAR 5 million.

### LAW-PDPPL-04-19 · Lawful basis: consent, lawful purpose, and the Article 19 exemptions
Applies to: law · human, oversight, override
Source: PDPPL Arts. 4, 19 [P]
Processing needs consent or a lawful purpose. Article 19 waives consent and some rights for legal
obligations, public interest, vital interests and research, but it does not lift the Article 16 permit,
the notice duty (Art. 9), security (Art. 13) or breach notification (Art. 14). An override on a legal
basis therefore never replaces the permit.

### LAW-PDPPL-08-13 · Controller and processor duties
Applies to: law · vendor, minimizer, oversight
Source: PDPPL Arts. 8, 10-13, 28 [P]; NCSA Controller and Processor Guideline [P]
Privacy by design (Art. 8(2)); data minimisation and storage limits (Art. 10); review before new
processing, in practice an impact assessment (Art. 11(1)); verify processors (Art. 11(8)); written
processor contracts; processors report breaches to the controller forthwith; contract terms that breach
the law are void (Art. 28).

### LAW-PDPPL-14 · Breach notification
Applies to: law · audit, vendor
Source: PDPPL Art. 14 [P]; NCSA Breach Notification Guideline v2.0 [P]
Notify the affected individuals and the regulator when a breach may cause serious damage. NCSA guidance
sets 72 hours from awareness, through the online breach form. The 72-hour deadline comes from guidance,
not from the statute.

### LAW-PDPPL-15 · Transfers abroad, notices and rights
Applies to: law · vendor, transparency
Source: PDPPL Arts. 5, 6, 9, 15 [P]; NCSA rights guidelines [S]
Transfers abroad are allowed unless the processing breaches the law or may cause serious damage; they
should be recorded, risk-assessed and covered by contract. Privacy notices disclose recipients, transfers
abroad and automated decisions. Patients may withdraw consent, object, access, correct and erase.

## Health-sector law

### LAW-SECRECY · Medical secrecy and its exceptions
Applies to: law · human, clinician, override
Source: Law No. 2 of 1983 Art. 20 [Q]; Penal Code (Law No. 11 of 2004) Art. 332 [P]
Doctors may not disclose patient information except in cases permitted by law. Divulging a professional
secret without consent or legal authority carries up to 2 years in prison and/or QR 10,000.

### LAW-NOTIFIABLE · Notifiable disease reporting
Applies to: law · moph_reporting
Source: Decree-Law No. 17 of 1990 Arts. 2, 4, 21, as amended by Law No. 9 of 2020 [S]
Doctors and facilities must report notifiable diseases (for example tuberculosis) as named, case-level
reports through MoPH's SAVES platform; Class A within 24 hours (Class B deadline conflicting [U]).
Penalty up to 3 years and QR 200,000. Named reports are a legal obligation and bypass de-identification.

### LAW-INSURANCE · Health insurance: consent and the insurance-data directive
Applies to: law · insurer_billing
Source: Law No. 22 of 2021 and MoPH Decision No. 8 of 2022 [S]; QNHI Data Management Directive v1.0 §§4-8 [P]
Medical records go to insurers only with the member's express written consent, and only to licensed,
MoPH-registered insurers and administrators. Insurance data is stored in Qatar and may not be exported;
claims use the IDS v5.x data set over HL7 FHIR; secondary use such as underwriting needs de-identified data.

### LAW-RESEARCH · Health research law
Applies to: law · vendor, research, fine-tuning
Source: Law No. 6 of 2025 (Art. 31 [P]); Cabinet Resolution No. 12 of 2026 [S]
Health research is done only by licensed institutions, after ethics-committee approval and with consent.
Training or validating an AI model on hospital data counts as research: it needs IRB approval as well as
the privacy permit.

## Cyber, cloud and AI

### LAW-CLOUD · Cloud, data residency and keys
Applies to: law · vendor, ai_diagnosis
Source: CRA Cloud Policy Framework ss.4.2-4.3 [P]; QNHI Directive §§4, 8 [P]
The cloud framework keeps localisation "very limited", with encryption, owner-held keys and anonymisation
as alternatives; insurance data must stay in Qatar. Both are met if identifiable records and keys stay in
Qatar and only minimised output leaves.

### LAW-AI · AI governance is soft law
Applies to: law · human, oversight, ai_diagnosis
Source: NCSA AI Guidelines (Feb 2024) [S]; MCIT ethical AI Principle 8 [Q]; draft National AI Policy s.5.5.5 (Sept 2025) [P]; JCI HCT.01.03 [P]
There is no binding healthcare-AI rule. Voluntary guidance and the draft national policy require ultimate
human accountability and no consequential decisions by high-risk systems without human oversight. JCI
expects selection, implementation, oversight and improvement of clinical decision support.

### LAW-SMALLCELL · Small-cell suppression benchmarks
Applies to: law · moph_reporting, oversight
Source: CMS cell-size policy (suppress 1-10) [P]; NHS England HES (suppress 1-7, round to 5) [P]
Public bodies suppress small counts before publication. A threshold of 5 is the least conservative of the
benchmarks found; small nationality groups argue for a stricter threshold or a written justification.

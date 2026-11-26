# Split the gateway into three lawful channels

A Qatari hospital should run its de-identification gateway as **three separately governed channels**, because each recipient has a different legal basis.

**Article 16 of the Personal Data Privacy Protection Law (PDPPL, Law No. 13 of 2016) is the anchor.** Health data is "special nature" data. It may be processed only with a permit from NCSA's Personal Data Privacy Protection Department (PDPPD), and penalties run up to **QAR 5 million**. Article 1 counts data as personal whenever identity "can be reasonably defined" by combining it with other data. A minimised note the hospital can re-link to the patient is therefore still health data. The gateway lowers risk, but it does not remove the permit, the impact assessment (DPIA) or the contract duties.

**Each recipient rests on a different basis:**
- **AI vendor.** A processor contract plus the permit. Any training of the vendor's model on hospital data is health research under **Law No. 6 of 2025**.
- **Insurers.** A structured claim under **Law No. 22 of 2021** and the Ministry of Public Health's (MoPH) insurance-data directive: data stays in Qatar, and medical records go out only with express written consent.
- **MoPH.** Notifiable-disease reports name the patient, are required by law, and should **bypass de-identification**. Statistics leave only as aggregates.

**AI rules are soft law in Qatar.** The hospital must therefore write its own clinician-in-the-loop rules. JCI HCT.01.03 is the accreditation hook. HIPAA, the GDPR and the EU AI Act serve as benchmarks only.

**Verification.** The PDPPL, insurance-data directive and NCSA guidelines were read in primary text. The insurance regulations, disease-reporting, research and cybercrime laws rest mostly on secondary sources.

*Tags:* **[P]** primary text read (PDPPL wording is the regulator's unofficial English translation; the authoritative Arabic is in Official Gazette No. 15 of 2016). **[Q]** primary wording seen only as quoted elsewhere, or cited but not re-read. **[S]** secondary only. **[U]** unverified or conflicting. Scope: onshore Qatar as of 22 November 2026; the Qatar Financial Centre (QFC) regime is excluded.

## Qatari obligations split cleanly by recipient

| Area | Obligation | Source (article) | Status |
|---|---|---|---|
| Scope | Pseudonymised data stays personal if identity "can be reasonably defined… through the combination of such data with any other data" | PDPPL Art. 1 ([CDP translation](https://cyberdatabase.unidir.org/api/files/1676833786171f3yskpqxl38.pdf)) | [P] |
| Health-data permit | Health data processed "only after obtaining the permission from the Competent Department". Fine up to QAR 5m. Procedure: DPIA, a permitted reason plus an additional condition, then a request to the PDPPD | PDPPL Arts. 16, 24; NCSA Advisory Note s.7.8, Oct 2025 ([NCSA](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/9737/1.0~b83017e6-db74-4592-a981-caae6512cbf8?mimetype=application%2Fpdf&filename=Advisory+Note+on+Building+a+Comprehensive+Data+Privacy+Program_EN_Final.pdf)) | [P] |
| Lawful basis | Consent, or a "Lawful Purpose" (Art. 4). Art. 19 waives consent and access for legal obligation, public interest, vital interests and research. It does **not** waive the Art. 16 permit, notice (Art. 9), security (Art. 13) or breach notice (Art. 14) | PDPPL Arts. 4, 19 | [P] |
| Controller and processor | Privacy by design (8(2)); data minimisation and storage limits (10); review before new processing, i.e. a DPIA (11(1)); verify processors (11(8)). Written processor contract required. Processor reports breaches "forthwith". Contract terms that breach the law are void | PDPPL Arts. 8, 10–13, 28; NCSA Controller and Processor (C&P) Guideline PDPPL-02050209E ([NCSA](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2904/1.0~ec44b72b-0d7a-4559-8889-2101cb82a698?mimetype=application%2Fpdf&filename=1.pdf)) | [P] |
| Breach | Notify individual and regulator if the breach "may cause serious damage" (law). Within **72 hours** (guidance) | PDPPL Art. 14; Breach Guideline PDPPL-02050217E ([NCSA](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/2991/1.0~5b70754f-6861-4223-8368-b0c74bd1a261?mimetype=application%2Fpdf&filename=BGJ.pdf)) | [P] |
| Rights, notice, transfer | Patients may withdraw consent, object, have data erased or corrected, access it, and must be told in advance. Notices disclose transfers abroad and automated decisions. Transfers abroad are allowed unless they "may cause serious damage". Requests answered in 30 days, with human review of automated decisions | PDPPL Arts. 5, 6, 9, 15 and Advisory Note [P]; Rights Guidelines ([Peninsula](https://www.thepeninsulaqatar.com/article/18/04/2026/explainer-ncsa-issues-guidelines-on-individuals-personal-data-privacy-protection-law-in-qatar)) [S] | Mixed |
| Medical secrecy | Doctors may not disclose a patient's information "exempt in those cases permitted by law" [Q]. Criminal penalty for divulging without consent or legal authority: up to 2 years and/or QR 10,000 [P] | Law 2/1983 Art. 20 ([WCM-Q deck](https://qatar-weill.cornell.edu/Portals/15/Events/Sunanda%27s%20Presentation%20Nov.%204th%20Seminar.pdf?ver=2016-11-30-072548-353)); Penal Code Art. 332 ([translation](https://www4.aucegypt.edu/CMRS/Files/2.2%20Penal%20Code%2011%202004_EN.pdf)) | Mixed |
| Notifiable disease | Named reports via MoPH's SAVES platform. Class A diseases within 24 hours. Up to 3 years and QR 200,000 | Decree-Law 17/1990 Arts. 2, 4, 21, amended by Law 9/2020 ([Gulf Times](https://www.gulf-times.com/story/659327/Jail-fine-for-non-reporting-of-infectious-diseases); [Peninsula](http://thepeninsulaqatar.com/article/05/08/2026/moph-reminds-healthcare-facilities-to-report-food-poisoning-cases-within-24-hours)) | [S]; Class B deadline [U] |
| Insurance law | "Express written consent from each member to disclose their medical records". Only licensed, MoPH-registered insurers and third-party administrators (TPAs) | Law 22/2021; MoPH Decision 8/2022 ([Clyde & Co](https://www.clydeco.com/en/insights/2022/09/qatar-issues-executive-regulations-to-the-new)) | [S] |
| Insurance-data directive | Data stored in Qatar (§4). Underwriting counts as secondary use and must be de-identified (§6). Claims sent in IDS v5.x format over HL7 FHIR (§7). Export prohibited (§8) | QNHI Directive v1.0, 20 Dec 2022 ([MoPH](https://www.moph.gov.qa/_layouts/15/download.aspx?SourceUrl=%2FAdmin%2FLists%2FPublicationsAttachments%2FAttachments%2F226%2FQNHI-DATA-MANAGEMENT-ENG.pdf)) | [P] |
| Health research | Research only by a licensed institution, after committee approval, with consent. Exporting samples needs an MoPH permit | Law 6/2025 Art. 31 ([official copy](https://www.customs.gov.qa/English/Legislations/Documents/Executive%20Resolutions/2025/Law%20No.%20%286%29%20of%202025%20Regulating%20Health%20Research.pdf)) [P]; Cabinet Res. 12/2026 ([Gulf Times](https://www.gulf-times.com/article/725301/qatar/research-regulations-set-to-enhance-ethics-safety-of-qatars-health-practices)) [S] | Mixed |
| AI in health | No binding MoPH AI rule. HBKU guidelines (MoPH advisory role) are non-binding. DHP teleradiology circular requires confidentiality and conflict-of-interest forms | [Eversheds, Nov 2025](https://www.eversheds-sutherland.com/en/united-states/insights/mapping-qatars-regulatory-landscape-for-artificial-intelligence-november-2025); DHP Circ. 6/2022 | [S] |
| Security and cybercrime | National Information Assurance Standard (NIAS) V2.1 with the National Data Classification Policy (NDCP) V3.0; NIA scope covers flows to third parties. Unauthorised access is a crime; penalty doubled if data are disclosed | [NCSA](https://ncsa.gov.qa/en/media/news/NCSA%20Conducts%20the%20Sixth%20Training%20Course%20on%20National%20Data%20Classification%20Policy%20and%20National%20Information%20Assurance%20Standard%20Implementation-430182) [P, existence]; [Vantage](https://www.vantage.com.qa/blog/nia-v2-1-vs-v2-0-what-changed), Law 14/2014 ([Al Tamimi](https://www.tamimi.com/law-update/october-4/articles/cyber-crime-prevention-law-in-qatar/)) [S] | Mixed |
| Cloud and residency | Localisation "very limited". The data owner keeps the encryption keys. Anonymisation is an alternative to localisation. An NCSA-hosted 2026 slide reports a "growing requirement" for in-Qatar storage but cites no rule | CRA Cloud Policy Framework ss.4.2–4.3 ([CRA](https://www.cra.gov.qa/-/media/System/A/B/3/F/AB3F01A7D2955C198BC8C1650FFDC104/Cloud-Policy-Framework.ashx)) [P]; [NCSA/PwC deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10207/1.0~fc4efdb1-0710-4db9-a751-c48e068c9509?mimetype=application%2Fpdf&filename=Presentation+-+Data+Privacy+in+Medical+Research+-+IDPD+2026+%282%29.pdf) [U] | Mixed |
| National AI | NCSA AI Guidelines, Feb 2024, voluntary [S]. MCIT Principle 8, "ultimate accountability to humans" [Q]. Draft National AI Policy (NAIP) s.5.5.5: no "consequential decisions without human oversight" (Sept 2025 draft) [P]. National Center for AI, Cabinet Decision 34/2026 [S] | [MCIT draft NAIP](https://prod16-assets.sprinklr.com/prod16-cdata/DAM/160136/9d77e677-a7f4-4659-a890-8e723c53e6dc-1081146622/MCIT_National_AI_Policy_Consul.pdf); [QU/NCSA deck](https://ncsa.gov.qa/shared/document_library/94787172324409/33000/10209/1.0~926129d6-931a-48dd-b185-7e15bb07e2fa?mimetype=application%2Fpdf&filename=Presentation+-+Implementing+Responsible+and+Compliant+AI+Systems+-+IDPD+2026+%2810%29.pdf) | Mixed |
| Benchmark: JCI | 8th edition (effective 2025): MOI.01.01–01.04; HCT.01.03 ("selection, implementation, oversight, and improvement" of decision support); GLD.05.00 contracts; QPS.03.00 | [JCI 8th ed.](https://digitalassets.jointcommission.org/api/public/content/79e9f5d2cd444a1a9178ab3f9487889a?v=4d4ea7b7) | [P] |
| Benchmark: de-identification | HIPAA Safe Harbor 18 identifiers and Expert Determination (reference only). Small-cell rules: CMS suppresses counts of 1–10; NHS England suppresses 1–7 and rounds to 5 | [45 CFR 164.514](https://www.law.cornell.edu/cfr/text/45/164.514); [ResDAC](https://resdac.org/node/1506); [NHS Digital](https://digital.nhs.uk/data-and-information/data-tools-and-services/data-services/hospital-episode-statistics/disclosure-control-methodology-for-hospital-episode-statistics-and-emergency-care-data-set) | [P] |
| Benchmark: EU, ISO, GCC | GDPR Arts. 9, 22, 35 [Q]. EU AI Act Arts. 10(4), 14, 26 [Q]; medical-device AI obligations start 2 Aug 2028 [S]. Draft EDPB Guidelines 02/2026 on anonymisation [S]. ISO/IEC 27001, 27701, 42001, 20889 [S]. UAE Law 2/2019 Art. 13 localisation [S] | [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj); [EDPB](https://www.edpb.europa.eu/public-consultations/guidelines-022026-on-anonymisation); [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) | Mixed |

Two points from this table shape the policies:

1. **Every channel needs the permit.** Article 19 never lifts the Article 16 permit, so even the MoPH channel needs one.
2. **The two residency positions can both be met.** The CRA framework discourages localisation; the MoPH directive requires in-Qatar storage. Both are satisfied if **identifiable records and keys stay in Qatar and only minimised output leaves**.

Enforcement evidence conflicts. Baker McKenzie reports three NCSA rectification orders in 2024–25 ([Baker McKenzie](https://connectontech.bakermckenzie.com/data-protection-enforcement-update-qatar/)) [S]. Chambers reports none made public ([Chambers 2026](https://chambers.com/practice-guides/guides/data-protection-privacy-2026/qatar/law-and-practice)) [S].

## Fifteen policies turn obligations into gateway rules

Rule IDs refer to the prototype's draft rules in `gateway/policies/gateway_rules.md`.

| # | Policy and core rule | Obligations | Owner | Draft rule |
|---|---|---|---|---|
| 1 | **Charter and roles.** Board-approved policy; appoints the Data Protection Officer (DPO), a clinical guardian and a governance committee. Record of processing activities (ROPA), annual audit, staff training | PDPPL Arts. 8, 11(3), 11(5), 11(7) [P]; Advisory Note [P]; JCI MOI.01.04 [P] | Board, DPO | File owner line |
| 2 | **Permit register.** No live data until the channel's record shows the hospital's role, its legal basis under Art. 4 or 19, the additional condition and the permit reference | PDPPL Arts. 4, 16, 19 [P]; Advisory Note s.7.8 [P] | DPO | New (GW-GEN-03) |
| 3 | **Outputs are personal data until proven otherwise.** Re-identification risk assessed in writing; reassessed when new data, models or rules appear | PDPPL Art. 1 [P]; ICO 2025 [P]; EDPB draft 02/2026 [S] | DPO | GW-GEN-02 |
| 4 | **One channel, one purpose.** Each channel has its own release form. A release built for one channel is never reused for another | PDPPL Arts. 10, 12 [P]; QNHI §5 [P] | DPO | GW-GEN-01 |
| 5 | **De-identification and certification.** Direct identifiers always removed. Quasi-identifiers set to the least restrictive level that passes the privacy and red-team tests. Certified on synthetic data, signed off by the DPO. Re-certified after any change | PDPPL Arts. 8(2), 11(1), 13 [P]; HIPAA list as checklist [P] | DPO, Committee | GW-AI-01 to 04, GW-CERT-01 |
| 6 | **DPIA before go-live.** Uses the NCSA template. Covers inference, automated decisions and transfers. Filed with the permit request | PDPPL Art. 11(1) [P]; Breach Guideline risk triggers [P] | DPO, Guardian | GW-CERT-01 |
| 7 | **AI vendor contract.** NCSA processor clauses. No training on our data, zero retention, no human review of submitted records. Named processing location and approved sub-processors. Vendor reports breaches within 24 hours. Audit rights, notice of model changes, deletion certificate, confidentiality form | PDPPL Arts. 11(8), 12, 13, 28 [P]; C&P Guideline [P]; JCI GLD.05.00 [P]; DHP Circ. 6/2022 [S] | DPO, Committee | GW-VEN-01 |
| 8 | **Keys stay in Qatar.** Identifiable records and keys on Qatar-hosted infrastructure. Minimised output goes abroad only after a transfer assessment. Insurance data never leaves | PDPPL Art. 15 [P]; QNHI §§4, 8 [P]; CRA s.4.2 [P] | DPO, IT security | New |
| 9 | **Insurers get claims only.** IDS v5.x over FHIR, to licensed, MoPH-registered insurers. No clinical notes, no brokers. Medical records only with written consent. No underwriting use | Decision 8/2022 [S]; QNHI §§5–8 [P] | DPO, health information | GW-BIL-01, 02 |
| 10 | **Notifiable reports bypass the gateway.** Named reports go through SAVES within the legal deadline, with only the required fields. AI flags go to the treating clinician | Decree-Law 17/1990 as amended [S]; PDPPL Art. 19(2) [P]; Law 2/1983 Art. 20 [Q] | Clinicians | GW-MOPH-02 |
| 11 | **Aggregates with small-cell control.** Suppress cells of 1–10, plus secondary suppression. Nationality-by-diagnosis cells always reviewed | PDPPL Art. 10 [P]; CMS and NHS practice [P]; JCI QPS.03.00 [P] | DPO | GW-MOPH-01 (raise from 5) |
| 12 | **Clinician in the loop.** AI output is advisory. A named clinician signs off and can override or stop it. Only the DPO overrides a failed privacy test, citing the legal basis. Track how often reviewers agree with the AI | Breach Guideline [P]; MCIT Principle 8 [Q]; draft NAIP s.5.5.5 [P]; JCI HCT.01.03 [P]; EU AI Act Art. 14 [Q] | Clinicians, DPO | GW-HITL-01 to 05 |
| 13 | **AI lifecycle and research.** Registry, validation on local data, check whether the tool is a regulated medical device, drift monitoring. Any training or validation is research: ethics committee (IRB) approval plus a permit | JCI HCT.01.03 [P]; Law 6/2025 [S]; PDPPL Art. 19(4) [P] | Committee, IRB | New |
| 14 | **Transparency and rights.** Privacy notice names the recipient categories, transfers abroad and AI use. Requests answered within 30 days | PDPPL Arts. 5, 6, 9 [P]; Rights Guidelines [S] | DPO | New |
| 15 | **Logging and breach.** NIAS controls. Append-only log that also records when AI results are re-linked to patients. A leaked identifier is notified within 72 hours | PDPPL Arts. 11(5), 13, 14 [P]; JCI MOI.01.01 [P]; NIAS V2.1 [S] | DPO, IT security | GW-AUD-01 |

### Settling the "[to confirm]" sources

| Draft rule | Confirmed source | Change needed |
|---|---|---|
| GW-HITL-04 | Consent (Art. 4); vital interests (Art. 19(3)); legal obligation (Art. 19(2)) [P]; secrecy exception "cases permitted by law", Law 2/1983 Art. 20 [Q] | State that an override never replaces the Art. 16 permit or the Art. 9 notice |
| GW-BIL-01 | QNHI §§5, 7, 8 [P]; Decision 8/2022 consent [S] | Add: licensed, registered recipients only; data stays in Qatar |
| GW-BIL-02 | No Qatari ban on underwriting found; nearest is QNHI §6 [P]; EU EHDS Art. 54 as benchmark [S] | Frame as a contract term, not law |
| GW-MOPH-02 | Decree-Law 17/1990 Arts. 2, 4 as amended by Law 9/2020 [S]; PDPPL Art. 19(2) [P] | Route named reports outside de-identification |
| GW-VEN-01 | PDPPL Arts. 11(8), 12, 13, 15, 28 [P]; C&P Guideline [P] | Add 24-hour vendor breach notice (inferred from the 72-hour window) |
| GW-AUD-01 | PDPPL Arts. 11(5), 11(7) [P]; JCI MOI.01.01 [P]; NIAS logging [S] | Do not name NIA control domains until the text is read |

The prototype's threshold of 5 (GW-AI-02, GW-MOPH-01) is the **least conservative** benchmark found. CMS suppresses counts up to 10, and Qatar's small nationality groups argue for going stricter.

Re-testing every human change (GW-HITL-03) answers the evidence on automation bias, where clinicians follow wrong AI suggestions:
- In a mammography study, readers' accuracy fell from about 80% to 20–46% when the AI was wrong ([RSNA](https://www.rsna.org/news/2023/may/ai-bias-may-impair-accuracy)) [S].
- A biased model cut clinicians' accuracy by 11.3 points, and showing its explanations did not help ([Jabbour 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10731487)) [P].

## Three roles and one committee carry accountability

No Qatari provider publishes a DPO or an AI-committee charter. HMC's 2025 notice names neither and does not mention AI ([HMC](https://hamad.qa/EN/Patient-Information/Patient-Family-Rights/Pages/HMC-Privacy-Notice.aspx)) [P]. The PDPPL does not require a DPO, but NCSA recommends an independent one (Advisory Note [P]).

- **DPO.** Owns the processing record, DPIAs, permits, NCSA contact, patient requests and breach notices. Signs off certification. The only person who can override a failed privacy test.
- **Clinical Confidentiality Guardian.** A senior clinician, on the NHS Caldicott model, who advises on disclosures and reviews data-sharing agreements. Not the same person as the senior information-risk owner ([NDG guidance](https://assets.publishing.service.gov.uk/media/6127b6d6e90e0705437230da/Caldicott_Guardian_guidance_v1.0_27.08.21.pdf)) [P].
- **Treating clinicians.** Hold the personal secrecy duty (Art. 20, Art. 332) and the duty to report notifiable diseases. Judge whether a release still supports the diagnosis and sign AI-influenced decisions. Cannot override privacy tests.
- **Data and AI Governance Committee.** Multidisciplinary and reports to the board. Approves channels and vendors, keeps the AI registry, and reviews overrides and logs monthly. Review depth follows Duke Health's model ([Duke ABCDS](https://healthaigovernance.duke.edu/abcds-oversight/abcds-oversight-process)) [P]: full review for the AI channel, fast-track for claims and statistics, logging only for notifiable reports.

## Open questions the prototype cannot settle

1. Is a PDPPD permit granted per channel? How long does it take, and who now holds the PDPPL's "Minister" powers?
2. Does a report the law requires still need a permit?
3. Does sending data to a vendor acting only as the hospital's processor count as "disclosure" under Art. 20 and Art. 332?
4. Does any MoPH rule require clinical (not insurance) data to stay in Qatar?
5. What do Law 6/2025 and Cabinet Resolution 12/2026 say about consent waivers and de-identified data?
6. What is the current notifiable-disease list and the Class B deadline (72 hours or one week)?
7. Is the AI tool a regulated medical device?
8. Does NIA certification apply to this hospital?
9. What retention period applies? HMC keeps records indefinitely for nationals and 10 years for others.
10. How does QNHI §4's "consent for all stored" data fit with the PDPPL's lawful-purpose basis?
11. Will the draft National AI Policy be adopted?

Several claims should stay out of the report:
- a "medical liability law No. 8 of 2021" (not found);
- that Sidra holds NIA certification (unsourced);
- that MoPH and the CRA run a "risk-tiered" AI regime (unverified);
- the old JCI numbering MOI.1–13 (superseded);
- any statement that the PDPPL itself sets a DPO requirement, localisation, or 72-hour or 30-day deadlines (these come from guidance).

## Conclusion

The gateway does not take data outside the law, but it gives the hospital evidence that it obeyed it. It shows the data were minimised (Art. 10), that privacy was designed in (Art. 8(2)), that keys stayed at the hospital, and that human review was itself tested. The synthetic-data certification stays outside the PDPPL only while the synthetic records are not derived from real patients.
